@echo off
echo This batchfile will download a Java 16 JRE (64bit) from https://www.sql-workbench.eu
echo to be used with SQL Workbench/J
echo.

if exist "%~dp0jre" (
  echo "A JRE directory already exists."
  echo "Please remove (or rename) this directory before running this batch file"
  goto :eof
)
set /P continue="Do you want to continue? (Y/N) "

if /I "%continue%"=="y" goto make_jre
if /I "%continue%"=="yes" goto make_jre

goto :eof

:make_jre
@powershell.exe -noprofile -executionpolicy bypass -file download_jre.ps1

setlocal

set zipfile=OpenJDK.zip

FOR /F " usebackq delims==" %%i IN (`dir /ad /b jdk*`) DO set jdkdir=%%i
rem echo %jdkdir%

ren %jdkdir% jre

echo.
echo JRE created in %~dp0jre
echo You can delete the ZIP archive %zipfile% now
echo.

