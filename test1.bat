@echo off
echo Тест 1: Запуск с VFS путем и скриптом
python terminal_emulator.py --vfs-path ".\my_vfs" --startup-script "script1.txt"

echo Тест 2: Запуск только с VFS путем  
python terminal_emulator.py --vfs-path ".\test_vfs"

echo Тест 3: Запуск со скриптом, который содержит ошибку
python terminal_emulator.py --vfs-path ".\error_vfs" --startup-script "script2.txt"

echo Все тесты завершены
pause