# -*- coding: utf-8 -*-
import sys
import os
import random
import traceback
import pygame

# ——————— 资源定位（resource_path） ———————
def resource_path(relative_path):
    """
    获取资源的绝对路径。
    打包后，PyInstaller 会把所有文件解压到临时文件夹 sys._MEIPASS，
    resource_path 就像快递单，把我们要找的文件快速定位到。
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ——————— Pygame 初始化 ———————
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()
pygame.mixer.set_num_channels(32)

# ——————— 常量配置 ———————
WIDTH, HEIGHT = 800, 600
FPS = 60

DIFFICULTY = {
    "easy":   {"times": [1000,1200,1500], "escape": 0.1},
    "medium": {"times": [800,1000,1300],  "escape": 0.3},
    "hard":   {"times": [600,800,1000],   "escape": 0.5},
}
ESCAPE_ACTIONS = {
    "easy":   ["slide","hop"],
    "medium": ["slide","hop","spin"],
    "hard":   ["slide","hop","spin","drift"],
}

MENU_BOARD_RATIO = 0.11
MENU_SPACING     = 20
MENU_OFFSET_Y    = HEIGHT * 0.07
MOLE_SLEEP_MIN   = 1000
MOLE_SLEEP_MAX   = 3000
HAMMER_HOLD_TIME = 200
SPAWN_MARGIN     = 50
BACK_HOLD_TIME   = 1500
STEP_COUNT       = 3
STEP_DURATION    = BACK_HOLD_TIME // STEP_COUNT

SHAKE_PROBABILITY = 0.5
SHAKE_DURATION    = 200
SHAKE_INTENSITY   = 5

# ——————— 窗口与时钟 ———————
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whats")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# ——————— 工具函数 ———————
def load_and_scale(rel_path, w):
    """先找到资源，再加载并等比缩放。"""
    path = resource_path(rel_path)
    img = pygame.image.load(path).convert_alpha()
    h = int(img.get_height() * w / img.get_width())
    return pygame.transform.scale(img, (int(w), h))

def load_frames(rel_dir):
    """加载指定文件夹下所有 .png 帧图片，用于动画。"""
    full_dir = resource_path(rel_dir)
    return [pygame.image.load(os.path.join(full_dir, f)).convert_alpha()
            for f in sorted(os.listdir(full_dir)) if f.endswith('.png')]

def load_sounds(prefix, n):
    """
    加载 sounds/ 目录下 prefix1.mp3 ~ prefixN.mp3。
    没找到就跳过，就像自动过滤空包裹。
    """
    out = []
    for i in range(1, n+1):
        rel = f"sounds/{prefix}{i}.mp3"
        path = resource_path(rel)
        if os.path.exists(path):
            out.append(pygame.mixer.Sound(path))
    return out

# ——————— 资源加载 ———————
maus_frames   = load_frames('images/maus')
hit_sounds    = load_sounds('hit', 4)
miss_sounds   = load_sounds('miss', 4)
appear_sounds = load_sounds('appear', 5)
coin_sounds   = load_sounds('coin', 4)
run_sounds    = load_sounds('run', 4)
hammer_sounds = load_sounds('hammer', 7)
choice_sounds = load_sounds('choice', 1)

# 锤子帧
hammer_raw    = load_frames('images/hammer')
hw            = WIDTH * 0.1
hammer_frames = [
    pygame.transform.scale(img, (int(hw), int(img.get_height() * hw / img.get_width())))
    for img in hammer_raw
]

# 背景图
bg_images = {
    k: pygame.transform.scale(
        pygame.image.load(resource_path(f'images/bg/{k}.png')).convert(),
        (WIDTH, HEIGHT)
    ) for k in ('start','easy','medium','hard')
}

# 难度按钮
wood_imgs = {}
bw = WIDTH * MENU_BOARD_RATIO
for k in ('easy','medium','hard'):
    wood_imgs[k] = load_and_scale(f'images/ui/wood_{k}.png', bw)
board_h = wood_imgs['easy'].get_height()
total   = 3 * board_h + 2 * MENU_SPACING
start_y = (HEIGHT - total) / 2 + MENU_OFFSET_Y
BUTTONS = {
    k: pygame.Rect(
        int((WIDTH - wood_imgs[k].get_width()) / 2),
        int(start_y + i * (board_h + MENU_SPACING)),
        wood_imgs[k].get_width(), board_h
    ) for i, k in enumerate(('easy','medium','hard'))
}

# 字体与文本
COLOR_WOOD  = (160,82,45)
DARK_WALNUT = (75, 50, 30)
font_btn    = pygame.font.SysFont('Comic Sans MS', 48, bold=True)
font_info   = pygame.font.SysFont('Comic Sans MS', 20, bold=True)
font_score  = pygame.font.SysFont('Comic Sans MS', 48, bold=True)

exit_txt    = font_btn.render('Exit', True, COLOR_WOOD)
exit_rect   = exit_txt.get_rect(bottomright=(WIDTH-10, HEIGHT-10))

# 信息文字
version_txt = font_info.render('v1.0.1', True, DARK_WALNUT)
brand_txt   = font_info.render('Musimanda', True, DARK_WALNUT)
design_txt  = font_info.render('Design by 3995 Hz', True, DARK_WALNUT)
design_rect   = design_txt.get_rect(bottomleft=(10, exit_rect.bottom))
brand_rect    = brand_txt.get_rect(bottomleft=(10, design_rect.top - 5))
version_rect  = version_txt.get_rect(bottomleft=(10, brand_rect.top - 5))

back_txt    = font_btn.render('Back', True, COLOR_WOOD)
back_rect   = back_txt.get_rect(bottomright=(WIDTH-10, HEIGHT-10))

# 音乐路径
ui_music  = resource_path('sounds/ui_music.mp3')
bg_music  = resource_path('sounds/bg_music.mp3')
win_sound = resource_path('sounds/100_win.mp3')

def play_music(path, loop=-1, vol=0.5):
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(loop)

# ——————— Mole 类 ———————
class Mole:
    def __init__(self, mode):
        cfg        = DIFFICULTY[mode]
        self.times = cfg['times']
        self.esc   = cfg['escape']
        self.actions = ESCAPE_ACTIONS[mode]
        self.mode  = mode
        self.visible = False
        self.escaping= False
        self.hits  = 0
        self.misses= 0
        self.next  = 0
        self.action()

    def action(self):
        now = pygame.time.get_ticks()
        if self.visible:
            self.visible = False
            self.escaping= False
            self.next    = now + random.randint(MOLE_SLEEP_MIN, MOLE_SLEEP_MAX)
            return
        img = maus_frames[0]
        self.scale = 0.144
        w = int(img.get_width()*self.scale)
        h = int(img.get_height()*self.scale)
        self.path = [(
            random.randint(SPAWN_MARGIN, WIDTH-w-SPAWN_MARGIN),
            random.randint(SPAWN_MARGIN, HEIGHT-h-SPAWN_MARGIN)
        ) for _ in range(4)]
        self.path_idx = 0
        self.pos      = list(self.path[0])
        self.visible  = True
        if self.mode=='hard' and self.misses>=3:
            life = 1200
            self.misses = 0
        else:
            life = random.choice(self.times)
            if self.hits>=2:
                life = max(min(self.times), life-50)
            if random.random()<self.esc:
                self.escaping = True
                self.et       = random.choice(self.actions)
                if run_sounds: random.choice(run_sounds).play()
            else:
                self.escaping = False
        self.life = life
        self.next = now + life
        self.frame = random.choice(maus_frames)
        if appear_sounds: random.choice(appear_sounds).play()

    def update(self):
        now = pygame.time.get_ticks()
        if now>=self.next:
            self.action()
        if self.escaping and self.visible and self.path_idx < len(self.path)-1:
            x1,y1 = self.path[self.path_idx]
            x2,y2 = self.path[self.path_idx+1]
            self.pos[0] += (x2-x1)/10
            self.pos[1] += (y2-y1)/10
            if abs(self.pos[0]-x2)<2 and abs(self.pos[1]-y2)<2:
                self.path_idx += 1

    def draw(self):
        if not self.visible:
            return
        surf = pygame.transform.scale(
            self.frame,
            (int(self.frame.get_width()*self.scale),
             int(self.frame.get_height()*self.scale)))
        screen.blit(surf, self.pos)

    def hit(self, x, y):
        if not self.visible:
            return 0
        rect = pygame.Rect(
            *self.pos,
            int(maus_frames[0].get_width()*self.scale),
            int(maus_frames[0].get_height()*self.scale)
        )
        if rect.collidepoint(x, y):
            self.visible=False
            self.hits += 1
            self.misses= 0
            pts = 1 if self.hits==1 else 5
            global shake_end
            if random.random()<SHAKE_PROBABILITY:
                shake_end = pygame.time.get_ticks() + SHAKE_DURATION
            random.choice(hit_sounds).play() if hit_sounds else None
            random.choice(coin_sounds).play() if coin_sounds else None
            return pts
        self.hits = 0
        self.misses += 1
        random.choice(miss_sounds).play() if miss_sounds else None
        return 0

# ——————— 主菜单 ———————
def menu_loop():
    play_music(ui_music)
    hammer_down  = False
    hammer_timer = 0
    hammer_held  = False
    hover        = None
    click_choice = None
    global shake_end; shake_end = 0

    while True:
        now = pygame.time.get_ticks()
        mx, my = pygame.mouse.get_pos()
        screen.blit(bg_images['start'], (0,0))

        # 按钮 hover 效果
        curr = None
        for k, r in BUTTONS.items():
            if r.collidepoint(mx, my):
                curr = k
                break
        if curr != hover:
            hover = curr
            if hover and choice_sounds:
                choice_sounds[0].play()
        for k, r in BUTTONS.items():
            if k == hover:
                img = pygame.transform.scale(
                    wood_imgs[k],
                    (int(wood_imgs[k].get_width()*1.1),
                     int(wood_imgs[k].get_height()*1.1))
                )
                nx = r.centerx - img.get_width()//2
                ny = r.centery - img.get_height()//2
                screen.blit(img, (nx, ny))
            else:
                screen.blit(wood_imgs[k], r.topleft)

        # 绘制文字
        screen.blit(exit_txt,    exit_rect.topleft)
        screen.blit(version_txt, version_rect.topleft)
        screen.blit(brand_txt,   brand_rect.topleft)
        screen.blit(design_txt,  design_rect.topleft)

        # 锤子自动抬起
        if hammer_down and now - hammer_timer >= HAMMER_HOLD_TIME:
            if not pygame.mouse.get_pressed()[0]:
                hammer_down = False
            else:
                hammer_held = True

        hm = hammer_frames[1] if hammer_down else hammer_frames[0]
        screen.blit(hm, hm.get_rect(center=(mx, my)))

        pygame.display.flip()
        clock.tick(FPS)

        # 点击反馈
        if click_choice and not hammer_down:
            if click_choice == 'exit':
                pygame.quit()
                sys.exit()
            return click_choice

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                hammer_down  = True
                hammer_timer = now
                hammer_held  = False
                if hammer_sounds:
                    random.choice(hammer_sounds).play()
                if exit_rect.collidepoint(e.pos):
                    click_choice = 'exit'
                else:
                    for k, r in BUTTONS.items():
                        if r.collidepoint(e.pos):
                            click_choice = k
                            break

# ——————— 游戏主循环 ———————
def game_loop(mode):
    play_music(bg_music)
    mole = Mole(mode)
    score = 0
    hammer_down  = False
    hammer_timer = 0
    hammer_held  = False
    back_hold_start = None
    win = False
    global shake_end; shake_end = 0
    win_bg = resource_path(
        f"images/bg/100_win{['easy','medium','hard'].index(mode)+1}.png"
    )

    while True:
        now = pygame.time.get_ticks()
        mx, my = pygame.mouse.get_pos()

        if back_hold_start and now - back_hold_start >= BACK_HOLD_TIME:
            return

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if win:
                    return
                hammer_down  = True
                hammer_timer = now
                hammer_held  = False
                if hammer_sounds:
                    random.choice(hammer_sounds).play()
                if back_rect.collidepoint(e.pos):
                    back_hold_start = now
                else:
                    score += mole.hit(mx, my)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if hammer_held:
                    hammer_down  = False
                    hammer_held  = False
                back_hold_start = None

        # 锤子抬起判断
        if hammer_down and now - hammer_timer >= HAMMER_HOLD_TIME:
            if not pygame.mouse.get_pressed()[0]:
                hammer_down = False
            else:
                hammer_held = True

        # 胜利检测
        if not win and score >= 100:
            win = True
            play_music(win_sound, 0)

        # 震动效果
        offset_x = offset_y = 0
        if now < shake_end:
            offset_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
            offset_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)

        # 绘制场景
        if win:
            bg = pygame.image.load(win_bg).convert()
            screen.blit(pygame.transform.scale(bg, (WIDTH,HEIGHT)), (offset_x, offset_y))
        else:
            screen.blit(bg_images[mode], (offset_x, offset_y))
            mole.update()
            mole.draw()
            screen.blit(back_txt, (back_rect.x+offset_x, back_rect.y+offset_y))
            if back_hold_start and back_rect.collidepoint(mx, my):
                elapsed = now - back_hold_start
                step    = max(1, STEP_COUNT - int(elapsed//STEP_DURATION))
                tip     = font_info.render(str(step), True, (255,255,255))
                screen.blit(
                    tip,
                    tip.get_rect(midbottom=(back_rect.centerx+offset_x,
                                            back_rect.top-5+offset_y))
                )
            hm = hammer_frames[1] if hammer_down else hammer_frames[0]
            screen.blit(hm, hm.get_rect(center=(mx+offset_x, my+offset_y)))
            scr = font_score.render(f"Punkte: {score}", True, COLOR_WOOD)
            screen.blit(scr, (10+offset_x, 10+offset_y))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        mode = menu_loop()
        game_loop(mode)
