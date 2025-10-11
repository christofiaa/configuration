@echo off
echo ===============================================
echo VFS Terminal Emulator - Полное тестирование
echo ===============================================

echo.
echo 1. Запуск с тестовой VFS и стартовым скриптом...
python task_4.py --vfs-path sample_vfs.xml --startup-script startup_script.txt

echo.
echo Тестирование завершено!
pause

