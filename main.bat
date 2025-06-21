@echo off
cd /d %~dp0
echo %~dp0

start emb_python\python.exe -c "import sys; sys.path=['.'] + sys.path; print(sys.path); import knotpen2; knotpen2.test_main.test_main()"
