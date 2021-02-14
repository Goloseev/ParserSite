chcp 1251
rem @echo off

set project_dir="l:\_Важное\6 Работа\Python\PyCharm\Parsing3\"
rem cd %project_dir
rem echo открыт каталог %cd% 
rem %project_dir%\venv\Scripts\activate.bat 
rem "l:\_Важное\6 Работа\Python\PyCharm\Parsing3\venv\Scripts\activate.bat" 
rem scrapy crawl Universal_spider --loglevel WARNING -a settings_file=---settings_centrsantehniki_com.json >> %Init_dir%\logs\%FileName%

python -m venv parsing_venv

d:
cd d:\_PythonProjects\ParserSite\
echo каталог %cd%

parsing_venv\Scripts\activate.bat
rem scrapy crawl Universal_spider --loglevel WARNING -a settings_file=---settings_centrsantehniki_com.json >> %Init_dir%\logs\%FileName%

echo скрипт завершен 
pause