@echo off
cd /d %~dp0
echo %~dp0

cd ../knotpen2

rem �����ǰĿ¼������֤
echo ��ǰĿ¼: %CD%

..\emb_python\Scripts\pyinstaller.exe -i logo.ico -F --add-data font\SourceHanSansSC-VF.ttf:font\ test_main.py
