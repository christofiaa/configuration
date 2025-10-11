
#!/usr/bin/env python3
"""
Тестовый скрипт для команд Этапа 4
"""

def test_vfs_structure():
    """Тест структуры VFS"""
    print("=== Тестирование структуры VFS ===")
    
    # Создаем тестовую VFS структуру
    test_vfs_content = """<?xml version='1.0' encoding='utf-8'?>
<vfs>
    <directory name="home">
        <directory name="user">
            <file name="document.txt" type="text">
                <content>VGhpcyBpcyBhIHRlc3QgZG9jdW1lbnQKTGluZSAyCkxpbmUgMwpMaW5lIDQKTGluZSA1CkxpbmUgNgpMaW5lIDcKTGluZSA4CkxpbmUgOQpMaW5lIDEw</content>
            </file>
            <file name="data.log" type="text">
                <content>TG9nIGVudHJ5IDEKbG9nIGVudHJ5IDIKbG9nIGVudHJ5IDMKbG9nIGVudHJ5IDQKbG9nIGVudHJ5IDUKbG9nIGVudHJ5IDYKbG9nIGVudHJ5IDcKbG9nIGVudHJ5IDgKbG9nIGVntHJ5IDkKbG9nIGVudHJ5IDEw</content>
            </file>
        </directory>
    </directory>
    <directory name="var">
        <directory name="log">
            <file name="system.log" type="text">
                <content>U3lzdGVtIGJvb3QKTmV0d29yayBpbml0aWFsaXplZApTZXJ2aWNlcyBzdGFydGVkClVzZXIgbG9naW4K</content>
            </file>
        </directory>
    </directory>
    <file name="readme.txt" type="text">
        <content>VGhpcyBpcyBhIHJlYWRt
