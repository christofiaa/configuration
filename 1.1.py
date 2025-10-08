
import tkinter as tk
from tkinter import scrolledtext, font
import re

class TerminalEmulator:
    VFS_name = "MyVFS"
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{self.VFS_name} Terminal Emulator")
        self.root.geometry("800x600")
        
        self.current_dir = "/home/user"
        self.command_history = []
        self.history_index = -1
        
        self.terminal_font = font.Font(family="Courier New", size=12)
        
        self.create_widgets()
        
        self.print_welcome()
        self.show_prompt()
        
        self.output_area.focus_set()
        self.ensure_cursor_position()
        
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
        self.output_area.bind("<KeyRelease>", self.on_key_release)
        self.output_area.bind("<Up>", self.on_arrow_up)
        self.output_area.bind("<Down>", self.on_arrow_down)
        self.output_area.bind("<Button-1>", self.on_click)
        self.output_area.bind("<FocusIn>", self.on_focus)

    def ensure_cursor_position(self):
        """Гарантирует, что курсор находится после промпта на последней строке"""
        last_line = int(self.output_area.index(tk.END).split('.')[0]) - 1
        prompt = f"user@{self.current_dir}$ "
        prompt_length = len(prompt)
        
        current_pos = self.output_area.index(tk.INSERT)
        current_line = int(current_pos.split('.')[0])
        current_col = int(current_pos.split('.')[1])
        
        if current_line < last_line:
            self.output_area.mark_set(tk.INSERT, f"{last_line}.{prompt_length}")
            return True
        
        if current_col < prompt_length:
            self.output_area.mark_set(tk.INSERT, f"{last_line}.{prompt_length}")
            return True
            
        return False

    def on_focus(self, event):
        """При получении фокуса гарантируем правильную позицию курсора"""
        self.ensure_cursor_position()
        
    def on_key_release(self, event):
        """После отпускания клавиши проверяем позицию курсора"""
        self.ensure_cursor_position()
        
    def on_click(self, event):
        current_line = int(self.output_area.index(tk.INSERT).split('.')[0])
        last_line = int(self.output_area.index(tk.END).split('.')[0]) - 1
        
        if current_line < last_line:
            self.output_area.mark_set(tk.INSERT, f"{last_line}.0")
            return "break"
        
    def on_key_press(self, event):
        cursor_moved = self.ensure_cursor_position()
        if cursor_moved:
            return "break"

        current_pos = self.output_area.index(tk.INSERT)
        current_line = int(current_pos.split('.')[0])
        last_line = int(self.output_area.index(tk.END).split('.')[0]) - 1

        if current_line < last_line:
            return "break"

        prompt = f"user@{self.current_dir}$ "
        prompt_length = len(prompt)
        current_col = int(current_pos.split('.')[1])
        
        if event.keysym in ["BackSpace", "Delete"]:
            if current_col <= prompt_length:
                return "break"
                
        if current_col < prompt_length and event.keysym not in ["Left", "Right", "Up", "Down"]:
            return "break"

        if len(event.keysym) == 1 and not event.keysym.isprintable():
            return "break"
        
    def on_arrow_up(self, event):
        if self.command_history:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
            self.replace_current_line(self.command_history[self.history_index])
        return "break"
        
    def on_arrow_down(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.replace_current_line(self.command_history[self.history_index])
        elif self.history_index == 0:
            self.history_index = -1
            self.replace_current_line("")
        return "break"
        
    def replace_current_line(self, text):
        last_line = int(self.output_area.index(tk.END).split('.')[0]) - 1
        prompt = f"user@{self.current_dir}$ "
        self.output_area.delete(f"{last_line}.0", f"{last_line}.end")
        self.output_area.insert(f"{last_line}.0", f"{prompt}{text}")
        self.output_area.mark_set(tk.INSERT, f"{last_line}.end")
        
    def print_welcome(self):
        welcome_text = """Добро пожаловать в VFS Terminal Emulator v1.0
Доступные команды: ls, cd, exit
Для выхода введите 'exit'

"""
        self.output_area.insert(tk.END, welcome_text)
        self.output_area.see(tk.END)
        
    def print_output(self, text):
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.ensure_cursor_position()
        
    def show_prompt(self):
        prompt = f"user@{self.current_dir}$ "
        self.print_output(prompt)
        self.ensure_cursor_position()
        
    def get_current_command(self):
        last_line = int(self.output_area.index(tk.END).split('.')[0]) - 1
        line_content = self.output_area.get(f"{last_line}.0", f"{last_line}.end").strip()
        
        prompt = f"user@{self.current_dir}$ "
        if line_content.startswith(prompt):
            return line_content[len(prompt):].strip()
        return line_content.strip()
        
    def execute_command(self, event):
        if event.state == 0 and event.keysym == "Return":
            command_line = self.get_current_command()
            
            self.print_output("\n")
            
            if command_line:
                self.command_history.insert(0, command_line)
                self.history_index = -1
                
                self.process_command(command_line)
            
            self.show_prompt()
            self.ensure_cursor_position()
            
            return "break"
        
    def process_command(self, command_line):
        if not command_line:
            return
            
        try:
            args = self.parse_arguments(command_line)
            command = args[0]
            arguments = args[1:]
            
            if command == "exit":
                self.handle_exit()
            elif command == "ls":
                self.handle_ls(arguments)
            elif command == "cd":
                self.handle_cd(arguments)
            else:
                self.print_output(f"Команда '{command}' не найдена\n")
                
        except Exception as e:
            self.print_output(f"Ошибка разбора команды: {str(e)}\n")
        
    def parse_arguments(self, command_line):
        """Парсер аргументов с поддержкой кавычек"""
        if not command_line.strip():
            return []
            
        pattern = r'\"([^\"]*)\"|\'([^\']*)\'|(\S+)'
        matches = re.findall(pattern, command_line)
        
        args = []
        for match in matches:
            arg = match[0] or match[1] or match[2]
            if arg:  
                args.append(arg)
        
        return args
        
    def handle_exit(self):
        self.print_output("Завершение работы терминала...\n")
        self.root.after(1000, self.root.destroy)
        
    def handle_ls(self, arguments):
        """Обработка команды ls без вывода конкретных файлов"""
        output = "Команда: ls\n"
        
        if arguments:
            output += f"Параметры: {arguments}\n"

        '''output += "Команда ls выполнена успешно\n"
        output += "Содержимое директории отображено\n"'''
        
        self.print_output(output)
        
    def handle_cd(self, arguments):
        """Обработка команды cd"""
        output = "Команда: cd\n"
        
        if arguments:
            output += f"Параметры: {arguments}\n"
        
        if len(arguments) == 0:
            self.current_dir = "/home/user"
            output += "Переход в домашнюю директорию\n"
        elif len(arguments) == 1:
            new_dir = arguments[0]
            if new_dir == "..":
                if self.current_dir != "/":
                    parts = self.current_dir.split("/")
                    self.current_dir = "/".join(parts[:-1]) or "/"
                    output += "Переход на уровень выше\n"
                else:
                    output += "Уже в корневой директории\n"
            elif new_dir.startswith("/"):
                self.current_dir = new_dir
                output += f"Переход по абсолютному пути: {new_dir}\n"
            else:
                if self.current_dir == "/":
                    self.current_dir = f"/{new_dir}"
                else:
                    self.current_dir = f"{self.current_dir}/{new_dir}"
                output += f"Переход по относительному пути: {new_dir}\n"
        else:
            output += "cd: слишком много аргументов\n"
            
        output += f"Текущая директория: {self.current_dir}\n"
        self.print_output(output)

def main():
    root = tk.Tk()
    app = TerminalEmulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

