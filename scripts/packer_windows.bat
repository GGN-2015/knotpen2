@echo off
cd /d %~dp0
echo %~dp0

cd ../knotpen2

rem 输出当前目录进行验证
echo 当前目录: %CD%

..\emb_python\Scripts\pyinstaller.exe -i logo.ico -F --add-data font\SourceHanSansSC-VF.ttf:font\ test_main.py
