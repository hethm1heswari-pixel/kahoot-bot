import os
import time
import requests
import pyautogui
import random
from pynput import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Style:
    CYAN, GREEN, YELLOW, RED, BOLD, RESET = "\033[96m", "\033[92m", "\033[93m", "\033[91m", "\033[1m", "\033[0m"

class KahootStealthBot:
    def __init__(self):
        self.coords = {} 
        self.answers = []
        self.driver = None
        self.last_answered_q = -1
        self.is_running = True
        self.wrong_questions = []
        self.q_start_time = 0

    def get_answers(self, quiz_id):
        url = f"https://create.kahoot.it/rest/kahoots/{quiz_id}"
        try:
            data = requests.get(url).json()
            return [next(i for i, c in enumerate(q['choices']) if c['correct']) for q in data['questions']]
        except: return None

    def get_game_state(self):
        try:
            counter = self.driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='question-index-counter']")
            current_num = int(counter.text.split(' ')[0])
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "[data-functional-selector='answer-0']")
            is_visible = len(buttons) > 0 and buttons[0].is_displayed()
            return current_num - 1, is_visible
        except: return None, False

    def human_click(self, correct_idx, is_mistake=False):
        # 1. Human hesitation (the bot's "thinking" time)
        delay = random.uniform(0.2, 3.2)
        time.sleep(delay)
        
        # 2. Determine target
        final_target = correct_idx
        if is_mistake:
            possible_wrong = [i for i in range(4) if i != correct_idx]
            final_target = random.choice(possible_wrong)

        # 3. Move and Click
        target_x, target_y = self.coords[final_target]
        pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.4, 0.8), tween=pyautogui.easeInOutQuad)
        pyautogui.click()

        # 4. CALC AND DISPLAY TIME
        total_time = time.time() - self.q_start_time
        print(f"{Style.CYAN}[TEST] Q{self.last_answered_q + 2} Answered in: {total_time:.2f}s (Delay was {delay:.2f}s){Style.RESET}")

    def kill_switch(self):
        # Global listener for Ctrl+0
        def on_activate():
            print(f"\n{Style.RED}KILL SWITCH ACTIVATED. TERMINATING.{Style.RESET}")
            self.is_running = False
            os._exit(0)

        listener = keyboard.GlobalHotKeys({'<ctrl>+0': on_activate})
        listener.start()

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Style.CYAN}{Style.BOLD}=== KAHOOT GHOST BOT v47 (Stealth Mode) ==={Style.RESET}")
        
        q_id = input("1. Quiz ID: ").strip()
        pin = input("2. Game PIN: ").strip()
        name = input("3. Nickname: ").strip()
        wrongs = input("4. Question numbers to get WRONG (e.g. 3, 8): ").strip()
        self.wrong_questions = [int(x.strip()) for x in wrongs.split(',')] if wrongs else []

        self.answers = self.get_answers(q_id)
        if not self.answers: return

        # Browser Setup
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://kahoot.it")
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located((By.NAME, "gameId"))).send_keys(pin + Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.NAME, "nickname"))).send_keys(name + Keys.ENTER)

        # Calibration
        print(f"\n{Style.CYAN}=== CALIBRATION (While in Lobby) ==={Style.RESET}")
        colors = ["RED (Triangle)", "BLUE (Diamond)", "YELLOW (Circle)", "GREEN (Square)"]
        for i, color in enumerate(colors):
            input(f"Hover over {color} and press Enter...")
            self.coords[i] = pyautogui.position()
        
        self.kill_switch()
        print(f"{Style.GREEN}STEALTH FULL-AUTO ACTIVE.{Style.RESET}")
        print(f"Kill Switch: {Style.BOLD}Ctrl + 0{Style.RESET}")

        while self.is_running:
            q_idx, active = self.get_game_state()
            
            # If buttons JUST appeared, start the timer
            if active and q_idx != self.last_answered_q and self.q_start_time == 0:
                self.q_start_time = time.time() 

            if active and q_idx != self.last_answered_q:
                is_fail = (q_idx + 1) in self.wrong_questions
                
                # We pass the start time into the click function
                self.human_click(self.answers[q_idx], is_mistake=is_fail)
                
                self.last_answered_q = q_idx
                self.q_start_time = 0 # Reset timer for next question
            
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        KahootStealthBot().run()
    except: pass