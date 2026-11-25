@echo off
rem Run the launcher's make-pack with the MSVC environment. Usage: make-pack.cmd <version>
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
cd /d "%~dp0..\..\..\launcher"
npm run make-pack -- "%~dp0..\pack\pack.config.json" --game-dir "D:\SteamLibrary\steamapps\common\Avatar The Last Airbender - Quest for Balance" --out "%~dp0..\work\out\avatar-qfb-he-%1.zip"
