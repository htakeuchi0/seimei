@echo off

if not exist env (
    call makeenv.bat
    call activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements_cp932.txt
    cls
)

call activate.bat
python seimei.py --gui
call deactivate
