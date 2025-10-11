@echo off
echo ===============================================
echo VFS Terminal - Тестирование Этапа 5
echo Дополнительные команды: touch, mkdir
echo ===============================================

echo.
echo Создание тестовой VFS...
python create_test_vfs.py

echo.
echo Запуск тестирования команды touch...
python task_5.py --startup-script stage5_startup_script.txt

echo.
echo Тестирование завершено!
pause