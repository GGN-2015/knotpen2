@echo off
cd /d %~dp0
echo %~dp0

cd ../knotpen2

rem �����ǰĿ¼������֤
echo ��ǰĿ¼: %CD%

rem ɾ����һ�ι���ʱ�Ļ����ļ�
rmdir /s /q build
rmdir /s /q dist

..\emb_python\Scripts\pyinstaller.exe -i logo.ico -F --add-data font\SourceHanSansSC-VF.ttf:font\ --add-data logo.ico:. test_main.py -n main.exe

rem ����ѹ���ļ�
mkdir dist\knotpen2
copy dist\main.exe dist\knotpen2\main.exe
copy ..\README.md dist\knotpen2\README.md
..\emb_python\python.exe ..\scripts\pyzip.py dist\knotpen2
