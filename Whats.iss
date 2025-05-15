; -------------------------------
; Whats 游戏 安装脚本（默认英文）
; -------------------------------
[Setup]
AppName=Whats
AppVersion=1.0.1
DefaultDirName={pf}\Whats
DefaultGroupName=Whats
OutputBaseFilename=Whats_Setup

[Files]
Source: "dist\Whats.exe";   DestDir: "{app}"; Flags: ignoreversion
Source: "images\*";         DestDir: "{app}\images"; Flags: recursesubdirs createallsubdirs
Source: "sounds\*";         DestDir: "{app}\sounds"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Whats";        Filename: "{app}\Whats.exe"
Name: "{commondesktop}\Whats"; Filename: "{app}\Whats.exe"

[Run]
Filename: "{app}\Whats.exe";   Description: "Launch Whats"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs;         Name: "{app}"
