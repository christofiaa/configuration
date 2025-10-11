import tkinter as tk
from tkinter import scrolledtext, font, messagebox
import re
import sys
import os
import subprocess
import xml.etree.ElementTree as ET
import base64
from datetime import datetime
import fnmatch

class VFS:
    """Виртуальная файловая система"""
    def __init__(self):
        self.root = {"type": "directory", "children": {}}
        self.current_vfs_path = None
        self.modified = False
    
    def create_simple_structure(self):
        """Создание простой тестовой структуры"""
        self.root = {
            "type": "directory", 
            "children": {
                "home": {
                    "type": "directory",
                    "children": {
                        "user": {
                            "type": "directory",
                            "children": {
                                "test.txt": {
                                    "type": "file",
                                    "content": "Это тестовый файл\nВторая строка\nТретья строка\nЧетвертая строка\nПятая строка\nШестая строка\nСедьмая строка\nВосьмая строка\nДевятая строка\nДесятая строка",
                                    "file_type": "text"
                                },
                                "data.log": {
                                    "type": "file",
                                    "content": "Лог запись 1\nЛог запись 2\nЛог запись 3\nЛог запись 4\nЛог запись 5",
                                    "file_type": "text"
                                },
                                "config.conf": {
                                    "type": "file", 
                                    "content": "# Конфигурационный файл\nhost=localhost\nport=8080\ndebug=true",
                                    "file_type": "text"
                                },
                                "documents": {
                                    "type": "directory",
                                    "children": {
                                        "readme.md": {
                                            "type": "file",
                                            "content": "# Документация\n\nЭто файл документации\nс несколькими строками\nтекста для тестирования\nкоманды tail",
                                            "file_type": "text"
                                        },
                                        "notes.txt": {
                                            "type": "file", 
                                            "content": "Важные заметки:\n- Первый пункт\n- Второй пункт\n- Третий пункт",
                                            "file_type": "text"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "var": {
                    "type": "directory",
                    "children": {
                        "log": {
                            "type": "directory",
                            "children": {
                                "system.log": {
                                    "type": "file",
                                    "content": "Система загружена\nСеть инициализирована\nПользователь вошел\nОшибка подключения\nСервис запущен",
                                    "file_type": "text"
                                },
                                "app.log": {
                                    "type": "file",
                                    "content": "2024-01-01 10:00:00 INFO: Приложение запущено\n2024-01-01 10:01:00 DEBUG: Инициализация модулей\n2024-01-01 10:02:00 ERROR: Ошибка в модуле А\n2024-01-01 10:03:00 WARN: Предупреждение системы\n2024-01-01 10:04:00 INFO: Работа восстановлена",
                                    "file_type": "text"
                                }
                            }
                        }
                    }
                },
                "etc": {
                    "type": "directory",
                    "children": {
                        "config": {
                            "type": "directory", 
                            "children": {
                                "system.conf": {
                                    "type": "file",
                                    "content": "system.name=VFS Terminal\nsystem.version=1.0\nsystem.admin=root",
                                    "file_type": "text"
                                }
                            }
                        }
                    }
                },
                "readme.txt": {
                    "type": "file",
                    "content": "Добро пожаловать в VFS Terminal\nЭто тестовая файловая система\nСоздана для демонстрации команд\nls, cd, tail, find\nУдачи в использовании!",
                    "file_type": "text"
                },
                "temp": {
                    "type": "directory",
                    "children": {
                        "cache": {
                            "type": "directory",
                            "children": {
                                "temp1.tmp": {
                                    "type": "file",
                                    "content": "Временные данные 1",
                                    "file_type": "text"
                                },
                                "temp2.tmp": {
                                    "type": "file",
                                    "content": "Временные данные 2",
                                    "file_type": "text"
                                }
                            }
                        }
                    }
                }
            }
        }
        return True, "Создана простая структура VFS"
    
    def load_from_xml(self, xml_path):
        """Загрузка VFS из XML файла"""
        try:
            if not os.path.exists(xml_path):
                return self.create_simple_structure()
            
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Очищаем текущую VFS
            self.root = {"type": "directory", "children": {}}
            self.current_vfs_path = xml_path
            self.modified = False
            
            # Рекурсивно строим структуру
            self._parse_xml_element(root, self.root["children"])
            return True, f"VFS успешно загружена из {xml_path}"
            
        except Exception as e:
            return self.create_simple_structure()
    
    def _parse_xml_element(self, element, current_dir):
        """Рекурсивный парсинг XML элемента"""
        for child in element:
            if child.tag == "file":
                name = child.get("name", "unnamed")
                content_elem = child.find("content")
                content = content_elem.text if content_elem is not None else ""
                
                # Декодируем base64 если нужно
                if content:
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        pass
                
                current_dir[name] = {
                    "type": "file",
                    "content": content,
                    "file_type": "text"
                }
                
            elif child.tag == "directory":
                name = child.get("name", "unnamed")
                current_dir[name] = {
                    "type": "directory", 
                    "children": {}
                }
                self._parse_xml_element(child, current_dir[name]["children"])
    
    def save_to_xml(self, xml_path):
        """Сохранение VFS в XML файл"""
        try:
            root = ET.Element("vfs")
            self._build_xml_element(self.root["children"], root)
            
            tree = ET.ElementTree(root)
            tree.write(xml_path, encoding="utf-8", xml_declaration=True)
            
            self.current_vfs_path = xml_path
            self.modified = False
            return True, f"VFS сохранена в {xml_path}"
            
        except Exception as e:
            return False, f"Ошибка сохранения VFS: {str(e)}"
    
    def _build_xml_element(self, current_dir, parent_element):
        """Рекурсивное построение XML структуры"""
        for name, item in current_dir.items():
            if item["type"] == "file":
                file_elem = ET.SubElement(parent_element, "file")
                file_elem.set("name", name)
                file_elem.set("type", item.get("file_type", "text"))
                
                content_elem = ET.SubElement(file_elem, "content")
                content = item.get("content", "")
                if content:
                    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                    content_elem.text = encoded
                    
            elif item["type"] == "directory":
                dir_elem = ET.SubElement(parent_element, "directory")
                dir_elem.set("name", name)
                self._build_xml_element(item["children"], dir_elem)
    
    def get_path_info(self, path):
        """Получение информации о пути в VFS"""
        if path == "/":
            return self.root, ""
        
        parts = [p for p in path.split("/") if p]
        current = self.root
        
        for part in parts:
            if current.get("type") != "directory":
                return None, "Not a directory"
            
            children = current.get("children", {})
            if part in children:
                current = children[part]
            else:
                return None, "Path not found"
                
        return current, ""
    
    def list_directory(self, path):
        """Список содержимого директории"""
        try:
            item, error = self.get_path_info(path)
            if error:
                return None, error
            
            if item["type"] != "directory":
                return None, "Not a directory"
            
            children = item.get("children", {})
            return list(children.keys()), None
            
        except Exception as e:
            return None, f"Error: {str(e)}"

    def get_file_content(self, path):
        """Получение содержимого файла"""
        item, error = self.get_path_info(path)
        if error:
            return None, error
        if item["type"] != "file":
            return None, "Not a file"
        return item.get("content", ""), None

    def find_files(self, start_path, pattern, search_type="name"):
        """
        Поиск файлов и директорий
        search_type: "name" - по имени, "content" - по содержимому
        """
        results = []
        
        def search_recursive(current_path, current_item):
            if current_item["type"] == "file":
                if search_type == "name":
                    if fnmatch.fnmatch(os.path.basename(current_path), pattern):
                        results.append(current_path)
                elif search_type == "content":
                    content = current_item.get("content", "")
                    if pattern in content:
                        results.append(current_path)
            elif current_item["type"] == "directory":
                if search_type == "name" and fnmatch.fnmatch(os.path.basename(current_path), pattern):
                    results.append(current_path + "/")
                
                children = current_item.get("children", {})
                for name, child in children.items():
                    child_path = f"{current_path}/{name}" if current_path != "/" else f"/{name}"
                    search_recursive(child_path, child)
        
        start_item, error = self.get_path_info(start_path)
        if error:
            return None, error
        
        search_recursive(start_path, start_item)
        return results, None

    def get_file_lines(self, path, num_lines=10):
        """Получение последних N строк файла"""
        content, error = self.get_file_content(path)
        if error:
            return None, error
        
        lines = content.split('\n')
        if len(lines) <= num_lines:
            return lines, None
        else:
            return lines[-num_lines:], None


class TerminalEmulator:
    def __init__(self, root, vfs_path=None, startup_script=None):
        self.root = root
        self.VFS_name = "MyVFS"
        
        self.vfs_path = vfs_path
        self.startup_script = startup_script
        
        # Инициализация VFS
        self.vfs = VFS()
        self.vfs_loaded = False
        
        self.root.title(f"{self.VFS_name} Terminal Emulator")
        self.root.geometry("800x600")
        
        self.current_dir = "/"
        self.command_history = []
        self.history_index = -1
        self.script_mode = False
        self.script_commands = []
        self.script_index = 0
        
        self.terminal_font = font.Font(family="Courier New", size=12)
        
        self.create_widgets()
        
        # Загрузка VFS
        success, message = self.vfs.load_from_xml(self.vfs_path or "nonexistent.xml")
        if success:
            self.vfs_loaded = True
            self.print_output(f"✅ {message}\n")
        
        self.print_welcome()
        
        # Запуск стартового скрипта если указан
        if self.startup_script and os.path.exists(self.startup_script):
            self.load_and_execute_script()
        else:
            self.show_prompt()
        
        self.output_area.focus_set()

    def load_and_execute_script(self):
        """Загрузка и выполнение стартового скрипта"""
        try:
            with open(self.startup_script, 'r', encoding='utf-8') as f:
                self.script_commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            
            self.print_output(f"=== Запуск скрипта: {self.startup_script} ===\n")
            self.script_mode = True
            self.script_index = 0
            self.execute_next_script_command()
            
        except Exception as e:
            self.print_output(f"Ошибка загрузки скрипта: {str(e)}\n")
            self.show_prompt()

    def execute_next_script_command(self):
        """Выполнение следующей команды из скрипта"""
        if self.script_index >= len(self.script_commands):
            self.script_mode = False
            self.print_output("=== Скрипт завершен ===\n")
            self.show_prompt()
            return
            
        command = self.script_commands[self.script_index]
        self.script_index += 1
        
        self.print_output(f"user@{self.current_dir}$ {command}\n")
        self.process_command(command, from_script=True)
        
        # Запускаем следующую команду после небольшой задержки
        if self.script_mode:
            self.root.after(100, self.execute_next_script_command)

    def create_widgets(self):
        self.output_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            font=self.terminal_font,
            bg="black",
            fg="white",
            insertbackground="white",
            state="normal"
        )
        self.output_area.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.output_area.bind("<Return>", self.execute_command)
        self.output_area.bind("<KeyPress>", self.on_key_press)

    def on_key_press(self, event):
        """Обработка нажатия клавиш"""
        if self.script_mode:
            return "break"
        if event.keysym == "Return":
            return "break"
        return None

    def print_welcome(self):
        welcome_text = f"""Добро пожаловать в VFS Terminal Emulator
VFS Location: {self.vfs_path or 'default'}
VFS Loaded: {self.vfs_loaded}
Startup Script: {self.startup_script or 'None'}
Доступные команды: ls, cd, pwd, cat, tail, find, vfs-load, vfs-save, debug, exit
Для выхода введите 'exit'

"""
        self.output_area.insert(tk.END, welcome_text)
        self.output_area.see(tk.END)
        
    def print_output(self, text):
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        
    def show_prompt(self):
        if not self.script_mode:
            prompt = f"user@{self.current_dir}$ "
            self.print_output(prompt)
        
    def get_current_command(self):
        """Получение текущей команды из последней строки"""
        last_line = self.output_area.get("end-1l", "end").strip()
        prompt = f"user@{self.current_dir}$ "
        if last_line.startswith(prompt):
            return last_line[len(prompt):].strip()
        return last_line.strip()
        
    def execute_command(self, event):
        """Выполнение команды"""
        if self.script_mode:
            return "break"
            
        command_line = self.get_current_command()
        self.print_output("\n")
        
        if command_line:
            self.command_history.insert(0, command_line)
            self.process_command(command_line)
        
        self.show_prompt()
        return "break"
        
    def process_command(self, command_line, from_script=False):
        """Обработка команды"""
        if not command_line:
            return
            
        try:
            args = command_line.split()
            command = args[0]
            arguments = args[1:]
            
            if command == "exit":
                self.handle_exit()
            elif command == "ls":
                self.handle_ls(arguments)
            elif command == "cd":
                self.handle_cd(arguments)
            elif command == "pwd":
                self.handle_pwd(arguments)
            elif command == "cat":
                self.handle_cat(arguments)
            elif command == "tail":
                self.handle_tail(arguments)
            elif command == "find":
                self.handle_find(arguments)
            elif command == "vfs-load":
                self.handle_vfs_load(arguments)
            elif command == "vfs-save":
                self.handle_vfs_save(arguments)
            elif command == "debug":
                self.handle_debug(arguments)
            else:
                self.print_output(f"Команда '{command}' не найдена\n")
                
        except Exception as e:
            self.print_output(f"Ошибка: {str(e)}\n")
        
    def handle_exit(self):
        self.print_output("Завершение работы...\n")
        self.root.after(1000, self.root.destroy)
        
    def handle_ls(self, arguments):
        """Обработка команды ls"""
        target_path = arguments[0] if arguments else self.current_dir
        
        items, error = self.vfs.list_directory(target_path)
        if error:
            self.print_output(f"ls: {error}\n")
            return
            
        if not items:
            self.print_output("Директория пуста\n")
            return
            
        output = "\n".join(items) + "\n"
        self.print_output(output)
        
    def handle_cd(self, arguments):
        """Обработка команды cd"""
        if not arguments:
            self.current_dir = "/"
            self.print_output("Переход в корень\n")
            return
            
        target_path = arguments[0]
        
        # Абсолютный или относительный путь
        if target_path.startswith("/"):
            new_path = target_path
        else:
            if self.current_dir == "/":
                new_path = f"/{target_path}"
            else:
                new_path = f"{self.current_dir}/{target_path}"
        
        # Нормализация пути
        parts = [p for p in new_path.split("/") if p and p != "."]
        normalized_parts = []
        for part in parts:
            if part == "..":
                if normalized_parts:
                    normalized_parts.pop()
            else:
                normalized_parts.append(part)
                
        new_path = "/" + "/".join(normalized_parts)
        if new_path == "":
            new_path = "/"
        
        # Проверка существования
        item, error = self.vfs.get_path_info(new_path)
        if error or item["type"] != "directory":
            self.print_output(f"cd: {target_path}: No such directory\n")
            return
            
        self.current_dir = new_path
        
    def handle_pwd(self, arguments):
        """Обработка команды pwd"""
        self.print_output(f"{self.current_dir}\n")

    def handle_cat(self, arguments):
        """Просмотр содержимого файла"""
        if not arguments:
            self.print_output("Ошибка: укажите файл\n")
            return
            
        filename = arguments[0]
        file_path = f"{self.current_dir.rstrip('/')}/{filename}" if self.current_dir != "/" else f"/{filename}"
        
        content, error = self.vfs.get_file_content(file_path)
        if error:
            self.print_output(f"cat: {error}\n")
            return
            
        self.print_output(f"{content}\n")

    def handle_tail(self, arguments):
        """Обработка команды tail - вывод последних строк файла"""
        if not arguments:
            self.print_output("Ошибка: укажите файл\n")
            return
        
        # Парсинг аргументов
        num_lines = 10  # значение по умолчанию
        filename = None
        
        i = 0
        while i < len(arguments):
            if arguments[i] == "-n" and i + 1 < len(arguments):
                try:
                    num_lines = int(arguments[i + 1])
                    i += 2
                except ValueError:
                    self.print_output("Ошибка: неверное количество строк\n")
                    return
            else:
                filename = arguments[i]
                i += 1
        
        if not filename:
            self.print_output("Ошибка: укажите файл\n")
            return
        
        file_path = f"{self.current_dir.rstrip('/')}/{filename}" if self.current_dir != "/" else f"/{filename}"
        
        lines, error = self.vfs.get_file_lines(file_path, num_lines)
        if error:
            self.print_output(f"tail: {error}\n")
            return
        
        output = "\n".join(lines) + "\n"
        self.print_output(output)

    def handle_find(self, arguments):
        """Обработка команды find - поиск файлов и директорий"""
        if not arguments:
            self.print_output("Ошибка: укажите параметры поиска\n")
            return
        
        # Парсинг аргументов
        start_path = self.current_dir
        pattern = None
        search_type = "name"
        search_content = None
        
        i = 0
        while i < len(arguments):
            if arguments[i] == "-name" and i + 1 < len(arguments):
                pattern = arguments[i + 1]
                search_type = "name"
                i += 2
            elif arguments[i] == "-type" and i + 1 < len(arguments):
                # Для простоты игнорируем тип, т.к. VFS различает файлы и директории автоматически
                i += 2
            elif arguments[i] == "-content" and i + 1 < len(arguments):
                search_content = arguments[i + 1]
                search_type = "content"
                i += 2
            elif arguments[i].startswith("/"):
                start_path = arguments[i]
                i += 1
            else:
                # Если не указаны флаги, считаем что это шаблон имени
                if pattern is None:
                    pattern = arguments[i]
                i += 1
        
        # Если указан контент для поиска, используем его как шаблон
        if search_content:
            pattern = search_content
        
        if not pattern:
            self.print_output("Ошибка: укажите шаблон для поиска\n")
            return
        
        results, error = self.vfs.find_files(start_path, pattern, search_type)
        if error:
            self.print_output(f"find: {error}\n")
            return
        
        if not results:
            self.print_output("Ничего не найдено\n")
        else:
            output = "\n".join(results) + "\n"
            self.print_output(output)

    def handle_vfs_load(self, arguments):
        """Загрузка VFS из XML файла"""
        if not arguments:
            self.print_output("Ошибка: укажите путь к XML файлу\n")
            return
            
        xml_path = arguments[0]
        success, message = self.vfs.load_from_xml(xml_path)
        
        if success:
            self.vfs_loaded = True
            self.vfs_path = xml_path
            self.current_dir = "/"
            self.print_output(f"✅ {message}\n")
        else:
            self.print_output(f"❌ {message}\n")

    def handle_vfs_save(self, arguments):
        """Сохранение VFS в XML файл"""
        if not arguments:
            self.print_output("Ошибка: укажите путь для сохранения\n")
            return
            
        xml_path = arguments[0]
        success, message = self.vfs.save_to_xml(xml_path)
        
        if success:
            self.print_output(f"✅ {message}\n")
        else:
            self.print_output(f"❌ {message}\n")

    def handle_debug(self, arguments):
        """Отладочная информация"""
        debug_info = f"""
=== DEBUG ===
Current Directory: {self.current_dir}
VFS Loaded: {self.vfs_loaded}
VFS Path: {self.vfs_path or 'None'}
Startup Script: {self.startup_script or 'None'}
Script Mode: {self.script_mode}
Commands in History: {len(self.command_history)}
=====
"""
        self.print_output(debug_info)


def parse_arguments():
    """Парсинг аргументов командной строки"""
    vfs_path = None
    startup_script = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--vfs-path" and i + 1 < len(args):
            vfs_path = args[i + 1]
            i += 2
        elif args[i] == "--startup-script" and i + 1 < len(args):
            startup_script = args[i + 1]
            i += 2
        else:
            if vfs_path is None:
                vfs_path = args[i]
            elif startup_script is None:
                startup_script = args[i]
            i += 1
            
    return vfs_path, startup_script


def main():
    vfs_path, startup_script = parse_arguments()
    root = tk.Tk()
    app = TerminalEmulator(root, vfs_path, startup_script)
    root.mainloop()


if __name__ == "__main__":
    main()
