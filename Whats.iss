; -------------------------------
; Whats 1.0 3995 Hz
; -------------------------------
[Setup]
AppName=Whats
AppVersion=1.0.1
DefaultDirName={pf}\Whats
DefaultGroupName=Whats
OutputBaseFilename=Whats_Setup

[Files]
; 把主程序放进安装目录
Source: "dist\Whats.exe";      DestDir: "{app}"; Flags: ignoreversion
; —— 新增：把 CREDITS 文档一并安装，就像给盒子里多放一本说明书
Source: "dist\CREDITS.txt";        DestDir: "{app}"; Flags: ignoreversion
; 资源图片和音效
Source: "images\*";            DestDir: "{app}\images"; Flags: recursesubdirs createallsubdirs
Source: "sounds\*";            DestDir: "{app}\sounds"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Whats";         Filename: "{app}\Whats.exe"
Name: "{commondesktop}\Whats"; Filename: "{app}\Whats.exe"

[Run]
Filename: "{app}\Whats.exe";   Description: "Launch Whats"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs;          Name: "{app}"
