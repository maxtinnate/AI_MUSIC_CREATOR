@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 免费分享 · 禁止售卖 · 禁止以任何名义收费(CC BY-NC-SA 4.0，创作者 reaesteve)
echo Shared free · Not for sale · No paid access of any kind (CC BY-NC-SA 4.0, creator: reaesteve)
echo.
set SONG=%~1
if "%SONG%"=="" set SONG=example_song.py
set SF2=..\sound_library\GeneralUser-GS\GeneralUser-GS.sf2
if not exist "%SF2%" (pushd ..\sound_library\GeneralUser-GS & copy /b "GeneralUser-GS.sf2.part_00"+"GeneralUser-GS.sf2.part_01"+"GeneralUser-GS.sf2.part_02"+"GeneralUser-GS.sf2.part_03" "GeneralUser-GS.sf2" >nul & popd)
where python >nul 2>nul || (echo 需要 Python 3.10+：https://www.python.org/downloads/ & pause & exit /b 1)
python -c "import numpy, scipy" 2>nul || python -m pip install -r requirements.txt
if not exist render.exe (
  where gcc >nul 2>nul && gcc -O2 -o render.exe render.c
  if not exist render.exe ( where cl >nul 2>nul && cl /nologo /O2 render.c /Fe:render.exe )
  if not exist render.exe ( echo 需要 C 编译器：安装 w64devkit 或 MinGW（gcc），或在 Visual Studio 的 Developer Command Prompt 中运行。 & pause & exit /b 1 )
)
del /q events_ch*.txt 2>nul
python "%SONG%" || (pause & exit /b 1)
if not exist stems mkdir stems
del /q stems\*.raw 2>nul
for /f "usebackq" %%T in (`python -c "import json;print(json.load(open('mix.json'))['total'])"`) do set TOT=%%T
for %%F in (events_ch*.txt) do call :one %%F
python mix_kit.py || (pause & exit /b 1)
echo 完成：song.wav
pause
exit /b 0
:one
set F=%1
set C=%F:~10,2%
render.exe "%SF2%" %F% stems\ch%C%.raw %TOT%
exit /b 0
