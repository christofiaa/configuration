@echo off
chcp 65001 > nul
echo ====================================
echo    ТЕСТИРОВАНИЕ VFS ЭМУЛЯТОРА
echo ====================================
echo.

echo Тест 1: Простая VFS
python terminal_emulator.py --vfs-path "simple_vfs.xml" --startup-script "test_simple.txt"
echo.

echo Тест 2: Средняя VFS
python terminal_emulator.py --vfs-path "medium_vfs.xml" --startup-script "test_medium.txt"
echo.

echo Тест 3: Сложная VFS
python terminal_emulator.py --vfs-path "complex_vfs.xml" --startup-script "test_complex.txt"
echo.

echo Тест 4: Ошибка загрузки VFS
python terminal_emulator.py --vfs-path "nonexistent.xml" --startup-script "test_error.txt"
echo.

echo ====================================
echo    ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ
echo ====================================
pause