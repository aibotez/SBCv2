@echo off
mode con lines=30 cols=60
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
rem 下面可以写你的bat代码了
python manage.py runserver [2408:8244:520:1db0:1e02::577]:90 --insecure