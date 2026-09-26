#define MyAppName "Valhalla"
#define MyAppVersion "0.4.6"
#define MyAppPublisher "Valhalla"
#define MyAppExeName "ValhallaLauncher.exe"
[Setup]
AppId={{A20F06CB-4F88-4F57-BD8A-VALHALLA0400}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Valhalla
DefaultGroupName=Valhalla
DisableProgramGroupPage=yes
OutputDir=..\..\release
OutputBaseFilename=Valhalla-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupLogging=yes
[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
[Files]
Source: "..\..\publish\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{autoprograms}\Valhalla"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Valhalla"; Filename: "{app}\{#MyAppExeName}"
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Lancer Valhalla"; Flags: nowait postinstall skipifsilent
