@echo off

set env_path=.\\env\\
set env_name=seimei

echo ^# Make an new python environment: %env_name%
echo.
python -m venv %env_path%%env_name%
if not exist activate.bat (
	echo ^@echo off > activate.bat
        echo call %env_path%%env_name%\\Scripts\\activate.bat >> activate.bat
)
echo done.
echo.
echo ^#
echo ^# To activate the %env_name% environment:
echo ^# ^> source activate
echo ^#
echo ^# To install packages:
echo ^# ^> source activate
echo ^# (%env_name%) ^> pip install -r requirements_cp932.txt
echo ^#
