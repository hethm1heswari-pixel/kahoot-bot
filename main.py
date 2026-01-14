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
    
    @staticmethod
    def pos(x, y):
        return f"\033[{y};{x}H"

class SystemManager:
    @staticmethod
    def detect_platform():
        system = platform.system().lower()
        if system == 'windows': return "windows"
        elif system == 'linux':
            if os.path.exists("/data/data/com.termux"): return "android"
            return "linux"
        elif system == 'darwin': return "macos"
        else: return "unknown"
    
    @staticmethod
    def clear_screen():
        system = SystemManager.detect_platform()
        try:
            if system == "windows": os.system('cls')
            else: os.system('clear')
        except: print("\n" * 100)
            
    @staticmethod
    def detect_terminal_size():
        try:
            columns, lines = os.get_terminal_size()
            return columns, lines
        except: return 80, 24

class DependencyChecker:
    @staticmethod
    def check_python_version():
        if sys.version_info < (3, 6):
            print(f"{TermCtrl.BRIGHT_RED}Error: Python 3.6+ required.{TermCtrl.RESET}")
            return False
        return True
    
    @staticmethod
    def install_missing_packages():
        # Added Selenium and Webdriver Manager to auto-install list
        packages = ['colorama', 'pystyle', 'selenium', 'webdriver_manager']
        for package in packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True

class MenuManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # Updated to point to your new 'dev' folder
        self.dev_dir = os.path.join(self.base_dir, "dev")
        
        self.exit_requested = False
        self.current_selection = 0
        self.menu_items = [
            {"id": "howto", "label": "How to Use", "description": "Interactive guide for these tools"},
            {"id": "flood", "label": "Game Flooder", "description": "Automated player utility"},
            {"id": "answers", "label": "Answer Hack", "description": "Get answers for a Quiz ID"},
            {"id": "autobot", "label": "Auto-Input Bot", "description": "Automatically clicks shapes in Chrome"},
            {"id": "exit", "label": "Exit", "description": "Close application"}
        ]
    
    def render_menu(self):
        w, _ = SystemManager.detect_terminal_size()
        print(f" {TermCtrl.BRIGHT_CYAN}╭{'─' * (w - 4)}╮{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {TermCtrl.BOLD}Kahoot Bot V32{TermCtrl.RESET}{' ' * (w - 19)}{TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}├{'─' * (w - 4)}┤{TermCtrl.RESET}")
        
        for idx, item in enumerate(self.menu_items):
            selector = f"{TermCtrl.BRIGHT_GREEN}▶{TermCtrl.RESET}" if idx == self.current_selection else " "
            label = f"{TermCtrl.BRIGHT_WHITE}{item['label']}{TermCtrl.RESET}"
            desc = f"{TermCtrl.DIM}{item['description']}{TermCtrl.RESET}"
            print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {selector} {idx+1}. {label:<18} {desc:<35} {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        
        print(f" {TermCtrl.BRIGHT_CYAN}╰{'─' * (w - 4)}╯{TermCtrl.RESET}")

    def get_user_selection(self):
        try:
            choice = input(f"\n {TermCtrl.BRIGHT_YELLOW}Selection (1-{len(self.menu_items)}): {TermCtrl.RESET}")
            if choice.isdigit() and 1 <= int(choice) <= len(self.menu_items):
                return int(choice) - 1
            return self.current_selection
        except: return self.current_selection
    
    def execute_selected_action(self, selection):
        action_id = self.menu_items[selection]["id"]
        SystemManager.clear_screen()
        
        try:
            if action_id == "howto":
                print("1. Flooder: Adds bots to a game.\n2. Answer Hack: Shows answers in terminal.\n3. Auto Bot: Clicks shapes for you.")
            elif action_id == "flood":
                subprocess.run([sys.executable, os.path.join(self.dev_dir, "Flood", "main.py")])
            elif action_id == "answers":
                subprocess.run([sys.executable, os.path.join(self.dev_dir, "client.py")])
            elif action_id == "autobot":
                # Runs the new auto_input.py we created
                subprocess.run([sys.executable, os.path.join(self.dev_dir, "auto_input.py")])
            elif action_id == "exit":
                self.exit_requested = True
                return
            
            if not self.exit_requested:
                input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return...{TermCtrl.RESET}")
        except Exception as e:
            print(f"Error: {e}")
            input("Press Enter...")

    def run(self):
        while not self.exit_requested:
            SystemManager.clear_screen()
            self.render_menu()
            selection = self.get_user_selection()
            self.current_selection = selection
            self.execute_selected_action(selection)

if __name__ == "__main__":
    DependencyChecker.check_python_version()
    DependencyChecker.install_missing_packages()
    MenuManager().run()