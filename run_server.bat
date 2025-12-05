@echo off

REM venv идэвхжүүлэх
cd /d D:\pythonProject
call venv\Scripts\activate

REM Django project folder руу орох
cd /d D:\pythonProject\stats_project

REM Server асаах
python manage.py runserver 0.0.0.0:8000
