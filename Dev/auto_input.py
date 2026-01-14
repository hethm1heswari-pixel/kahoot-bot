import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Allow this script to see your 'dev' folder
sys.path.append(os.path.join(os.getcwd(), 'dev'))
from client import Kahoot

def start_auto_bot():
    print("--- Kahoot Shape-Based Auto Bot ---")
    quiz_id = input("Enter Kahoot Quiz ID: ")
    kahoot = Kahoot(quiz_id)
    
    if not kahoot.data:
        print("Invalid Quiz ID.")
        return

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://kahoot.it")
    
    print("\n[!] Join the game manually. I will click the shapes automatically.")

    current_q = 0
    total_q = kahoot.get_quiz_length()

    while current_q < total_q:
        try:
            # 1. Get the question details
            q_details = kahoot.get_question_details(current_q)
            choices = q_details.get("choices", [])
            
            # 2. Find which index is the correct one
            correct_index = -1
            for idx, choice in enumerate(choices):
                if choice.get("correct"):
                    correct_index = idx
                    break
            
            if correct_index == -1:
                current_q += 1
                continue

            # 3. Wait for the answer buttons to appear
            # Kahoot uses data-functional-selector for buttons (e.g., answer-0, answer-1)
            wait = WebDriverWait(driver, 20)
            button_selector = f"button[data-functional-selector='answer-{correct_index}']"
            
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
            
            # 4. Click the colored shape!
            button.click()
            print(f"✅ Q{current_q + 1}: Clicked Shape Index {correct_index}")
            
            current_q += 1
            time.sleep(3) # Wait for the next question transition

        except Exception:
            # Still waiting for the question to start...
            pass

    print("Game complete!")
    driver.quit()

if __name__ == "__main__":
    start_auto_bot()