@ECHO off

REM Operate in Desktop folder
cd %USERPROFILE%\Desktop

REM Download zip file from github
curl -Lo pygame.zip "https://github.com/georgeneokq/PygameForBeginners/archive/refs/heads/main.zip"

REM Unzip folder
tar -xf pygame.zip

REM Rename folder to pygame
rename PygameForBeginners-main pygame

REM Delete zip file
del pygame.zip

REM Operate in pygame folder
cd pygame

REM Install dependencies
pip install -r requirements.txt

REM Open the folder in file explorer
start .