@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist GeneralUser-GS.sf2 (echo 已存在 GeneralUser-GS.sf2 & pause & exit /b 0)
copy /b "GeneralUser-GS.sf2.part_00"+"GeneralUser-GS.sf2.part_01"+"GeneralUser-GS.sf2.part_02"+"GeneralUser-GS.sf2.part_03" "GeneralUser-GS.sf2" >nul
echo 已合并：GeneralUser-GS.sf2
pause
