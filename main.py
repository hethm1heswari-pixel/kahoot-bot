#!/usr/bin/env python3
import os
import sys
import time
import platform
import subprocess
from pathlib import Path
from datetime import datetime

# Terminal Control Constants
class TermCtrl:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright Foreground Colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background Colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Clear Screen
    CLEAR = "\033[2J\033[H"
    
    # Cursor Movement
    @staticmethod
    def pos(x, y):
        return f"\033[{y};{x}H"

class SystemManager:
    @staticmethod
    def detect_platform():
        system = platform.system().lower()
        
        if system == 'windows':
            return "windows"
        elif system == 'linux':
            if os.path.exists("/data/data/com.termux"):
                return "android"
            return "linux"
        elif system == 'darwin':
            return "macos"
        else:
            return "unknown"
    
    @staticmethod
    def clear_screen():
        system = SystemManager.detect_platform()
        
        try:
            if system == "windows":
                os.system('cls')
            elif system in ["linux", "macos", "android"]:
                os.system('clear')
            else:
                print("\033[2J\033[H", end="")
        except Exception:
            print("\n" * 100)
            
    @staticmethod
    def detect_terminal_size():
        try:
            columns, lines = os.get_terminal_size()
            return columns, lines
        except:
            return 80, 24
    
    @staticmethod
    def is_dependency_installed(command):
        try:
            devnull = open(os.devnull, 'w')
            subprocess.check_call([command, "--version"], stdout=devnull, stderr=devnull)
            return True
        except:
            return False

class DependencyChecker:
    @staticmethod
    def check_python_version():
        if sys.version_info < (3, 6):
            print(f"{TermCtrl.BRIGHT_RED}Error: Python 3.6 or higher is required.{TermCtrl.RESET}")
            return False
        return True
    
    @staticmethod
    def install_missing_packages():
        packages_to_check = ['colorama', 'pystyle']
        missing_packages = []
        
        for package in packages_to_check:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            for package in missing_packages:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                except subprocess.CalledProcessError:
                    pass
        return True

class MenuManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.join(self.base_dir, "src")
        self.gui_dir = os.path.join(self.base_dir, "src", "client")
        self.kitty_dir = os.path.join(self.base_dir, "Kitty")
        
        self.is_src_available = os.path.isdir(self.src_dir)
        self.term_width, self.term_height = SystemManager.detect_terminal_size()
        
        self.exit_requested = False
        self.current_selection = 0
        self.menu_items = [
            {"id": "howto", "label": "How to Use", "description": "Interactive guide on using these tools            "},
            {"id": "flood", "label": "Game Flooder", "description": "Advanced game flooding utility                  "},
            {"id": "answers", "label": "Answer Hack", "description": "Obtain answers for quizzes                       "},
            {"id": "graphical", "label": "GUI", "description": "Graphical user interface                         "},
            {"id": "exit", "label": "Exit", "description": "Exit the application                              "}
        ]
    
    def render_menu(self):
        print(f" {TermCtrl.BRIGHT_CYAN}╭{'─' * (self.term_width - 4)}╮{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {TermCtrl.BOLD}Tools Menu{TermCtrl.RESET}{' ' * (self.term_width - 15)}{TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}├{'─' * (self.term_width - 4)}┤{TermCtrl.RESET}")
        
        for idx, item in enumerate(self.menu_items):
            if idx == self.current_selection:
                selector = f"{TermCtrl.BRIGHT_GREEN}▶{TermCtrl.RESET}"
                label = f"{TermCtrl.BRIGHT_WHITE}{TermCtrl.BOLD}{item['label']}{TermCtrl.RESET}"
                desc = f"{TermCtrl.BRIGHT_WHITE}{item['description']}{TermCtrl.RESET}"
            else:
                selector = " "
                label = f"{TermCtrl.WHITE}{item['label']}{TermCtrl.RESET}"
                desc = f"{TermCtrl.DIM}{item['description']}{TermCtrl.RESET}"
            
            id_text = f"{idx + 1}. "
            spacing = " " * (20 - len(item['label']))
            print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {selector} {id_text}{label}{spacing}{desc}{' ' * (self.term_width - 50 - len(item['description']))}{TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        
        print(f" {TermCtrl.BRIGHT_CYAN}╰{'─' * (self.term_width - 4)}╯{TermCtrl.RESET}")
        print(f"\n {TermCtrl.DIM}Use number keys to navigate, Enter to select{TermCtrl.RESET}")
    
    def render_status(self, message=None):
        platform_info = SystemManager.detect_platform()
        status_text = message if message else "Ready"
        
        print(f"\n {TermCtrl.BRIGHT_BLACK}Status: {TermCtrl.RESET}{status_text}")
        print(f" {TermCtrl.BRIGHT_BLACK}System: {TermCtrl.RESET}{platform_info.capitalize()}")

    def get_user_selection(self):
        try:
            choice = input("\n Selection (1-5): ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.menu_items):
                return int(choice) - 1
            return self.current_selection
        except KeyboardInterrupt:
            return len(self.menu_items) - 1
        except:
            return self.current_selection
    
    def check_dependencies_for_action(self, action_id):
        if action_id in ["flood", "answers", "graphical"]:
            try:
                import colorama
                import pystyle
            except ImportError:
                DependencyChecker.install_missing_packages()
            
            if action_id == "flood":
                if not SystemManager.is_dependency_installed("node"):
                    print(f"{TermCtrl.BRIGHT_RED}Node.js is required for this feature.{TermCtrl.RESET}")
                    time.sleep(2)
        return True
    
    def execute_selected_action(self, selection):
        action_id = self.menu_items[selection]["id"]
        
        if not self.check_dependencies_for_action(action_id):
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return...{TermCtrl.RESET}")
            return
        
        SystemManager.clear_screen()
        
        try:
            if action_id == "howto":
                self.execute_howto()
            elif action_id == "flood":
                self.execute_flood()
            elif action_id == "answers":
                self.execute_answers()
            elif action_id == "graphical":
                self.execute_graphical()
            elif action_id == "exit":
                self.exit_requested = True
                return
                
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to menu...{TermCtrl.RESET}")
            
        except KeyboardInterrupt:
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to menu...{TermCtrl.RESET}")
        except Exception as e:
            print(f"\n{TermCtrl.BRIGHT_RED}Error: {str(e)}{TermCtrl.RESET}")
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to menu...{TermCtrl.RESET}")
    
    def execute_howto(self):
        print(f"{TermCtrl.BOLD}{TermCtrl.BRIGHT_CYAN}User Guide{TermCtrl.RESET}\n")
        print(f"1. Flooder: Create multiple automated players in games.")
        print(f"2. Answer Hack: Retrieve answers using a Quiz ID.")
        print(f"3. GUI: Launch a visual window for these tools.")
    
    def execute_flood(self):
        target = os.path.join(self.src_dir if self.is_src_available else self.kitty_dir, "main.py" if self.is_src_available else "Flood/main.py")
        try:
            subprocess.run([sys.executable, target])
        except Exception as e:
            print(f"Execution error: {e}")
    
    def execute_answers(self):
        target = os.path.join(self.src_dir if self.is_src_available else self.kitty_dir, "client.py")
        try:
            subprocess.run([sys.executable, target])
        except Exception as e:
            print(f"Execution error: {e}")
            
    def execute_graphical(self):
        if self.is_src_available:
            try:
                import PyQt5
                subprocess.run([sys.executable, os.path.join(self.gui_dir, "main.py")])
            except ImportError:
                print(f"PyQt5 not found. Attempting install...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyQt5'])
                subprocess.run([sys.executable, os.path.join(self.gui_dir, "main.py")])
        else:
            self.execute_answers()
    
    def run(self):
        while not self.exit_requested:
            SystemManager.clear_screen()
            self.term_width, self.term_height = SystemManager.detect_terminal_size()
            self.render_menu()
            self.render_status()
            selection = self.get_user_selection()
            if 0 <= selection < len(self.menu_items):
                self.current_selection = selection
                self.execute_selected_action(selection)

def main():
    try:
        if not DependencyChecker.check_python_version():
            sys.exit(1)
        DependencyChecker.install_missing_packages()
        
        manager = MenuManager()
        manager.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()