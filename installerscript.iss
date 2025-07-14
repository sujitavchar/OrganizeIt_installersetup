[Setup]
AppName=Organize It
AppVersion=2.0
DefaultDirName={pf}\Organize It
DefaultGroupName=Organize It
OutputDir=userdocs:Inno Setup Output
OutputBaseFilename=OrganizeItInstallerV2
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\shri\Desktop\OrganizeIt\icon2.ico

[Files]
Source: "C:\Users\shri\Desktop\OrganizeIt\dist\OrganizeItV2.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Organize It"; Filename: "{app}\OrganizeItV2.exe"; IconFilename: "{app}\icon2.ico"
Name: "{commondesktop}\Organize It"; Filename: "{app}\OrganizeItV2.exe"; IconFilename: "{app}\icon2.ico"; Flags: createonlyiffileexists

[Run]
Filename: "{app}\OrganizeItV2.exe"; Description: "Launch Organize It"; Flags: nowait postinstall skipifsilent
