@REM echo off
cls
set original_dir = %CD%
set root_dir = "D:\dev\unreal\ToolsTest\Plugins\WebHook\Content\Python"

cd %root_dir%

call .\.venv\Scripts\activate.bat

@REM python your_python_script.py <arg1> <arg2> <arg3>
python .\server\server.py
@REM pause

call .\.venv\Scripts\deactivate.bat

cd %original_dir%

exit /B 1