chcp 1251
@ECHO OFF

set bat_dir=%2


rem ping ya.ru
set dd=%DATE%
set tt=%TIME%

set /a ddd=%dd:~0,2%
IF %ddd% LSS 10 (
  SET day=0%ddd%) else (
  SET day=%ddd%)
set month=%dd:~3,2%
set year=%dd:~6,4%

set /a ttt=%tt:~0,2%

IF %ttt% LSS 10 (
  SET hour=0%ttt%) else (
  SET hour=%ttt%)
 
SET minute=%tt:~3,2%
SET sec=%tt:~6,2%

SET FileName=%day%-%month%-%year%_%hour%_%minute%_%sec%_%1.txt

@ECHO ON
echo %FileName% > logs\%FileName%

rem copy nul %FileName%

l:
set project_dir="l:\_Важное\6 Работа\Python\PyCharm\Parsing3"
cd %project_dir%\Universal_scrapy_app
echo открыт каталог %cd% >> %bat_dir%\logs\%FileName%
echo открыт каталог %cd% 
rem %project_dir%\venv\Scripts\activate.bat >> %bat_dir%\logs\%FileName%
 
scrapy crawl Universal_spider --loglevel WARNING -a settings_file=%1 >> %bat_dir%\logs\%FileName%
rem pause
echo скрипт завершен >> %Init_dir%\logs\%FileName%
