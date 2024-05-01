@ECHO off

REM Operate in Desktop folder
cd %USERPROFILE%\Desktop

REM Download zip file from github
curl -Lko pygame.zip "https://github.com/georgeneokq/PygameForBeginners/archive/refs/heads/main.zip" --proxy http://10.5.4.6:8080

REM Unzip folder
tar -xf pygame.zip

REM Rename folder to pygame
rename PygameForBeginners-main pygame

REM Delete zip file
del pygame.zip

REM Operate in pygame folder
cd pygame

REM Install dependencies
py -m pip install -r requirements.txt --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --proxy http://10.5.4.6:8080

REM Open the folder in file explorer
start .