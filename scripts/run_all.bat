@echo off
setlocal EnableDelayedExpansion
set BASE=%~dp0..
set JM="e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\tools\apache-jmeter-5.6.3\bin\jmeter.bat"
set SID=23127153
set DATE=20260830

powershell -ExecutionPolicy Bypass -File "e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\scripts\reset-eshop-api.ps1" -Port 3010
python "%BASE%\scripts\generate_jmx.py"

call :jmeter_one Load load
call :jmeter_one Stress stress
call :jmeter_one Spike spike
call :jmeter_one Endurance endurance

python "%BASE%\scripts\summarize_jtl.py"
echo Done.
exit /b 0

:jmeter_one
set NAME=%~1
set FOLDER=%~2
echo === Running %NAME% ===
if exist "%BASE%\results\%FOLDER%\%SID%_%NAME%_%DATE%.jtl" del /f /q "%BASE%\results\%FOLDER%\%SID%_%NAME%_%DATE%.jtl"
if exist "%BASE%\results\%FOLDER%\html-report" rmdir /s /q "%BASE%\results\%FOLDER%\html-report"
mkdir "%BASE%\results\%FOLDER%" 2>nul
%JM% -n -t "%BASE%\test-plans\%SID%_%NAME%_%DATE%.jmx" -l "%BASE%\results\%FOLDER%\%SID%_%NAME%_%DATE%.jtl" -e -o "%BASE%\results\%FOLDER%\html-report"
exit /b 0
