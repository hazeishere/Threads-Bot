import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from g4f.client import Client

# Load environment variables
load_dotenv()

# Constants
THREADS_USERNAME = os.getenv('THREADS_USERNAME')
THREADS_PASSWORD = os.getenv('THREADS_PASSWORD')
THREADS_URL = "https://www.threads.net/login"

# Prompts to ask ChatGPT
PROMPTS = [
    "產生一句發人深省的人生格言",
    "寫一個關於現代科技的有趣觀察",
    "一個關於人性的有趣事實",
    "為企業家創作一條激勵人心的信息",
    "一條關於社交媒體的機智評論",
    "關於財富的真相",
    "分享一個關於健康的冷知識",
    "寫出一段諷刺的話",
    "寫一條能夠激勵人心的話",
    "隨機分享為何愛情是美好的",
    "隨機產生一句幹話",
    "隨機分享一個普遍知識",
    "隨機從書裡分享一個觀點",
    "分享對於AI的看法",
    "隨機提出一個問題",
    "一段容易引起爭議的話",
    "一段容易引起共鳴的話",
]

class ThreadsBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def login_to_threads(self):
        try:
            self.driver.get(THREADS_URL)
            time.sleep(3)
            
            # Login flow
            username_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username, phone or email']")))
            username_input.send_keys(THREADS_USERNAME)
            
            password_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']")))
            password_input.send_keys(THREADS_PASSWORD)
            password_input.send_keys(Keys.RETURN)
            
            time.sleep(5)  # Wait for login to complete
            
        except TimeoutException:
            print("Failed to login to Threads")
            return False
        return True

    def get_chatgpt_response(self):
        try:
            # Select random prompt
            prompt = random.choice(PROMPTS)

            client = Client()
            
            # Get response using g4f
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                web_search=False
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Failed to get AI response: {e}")
            return None

    def post_to_threads(self, content):
        try:
            self.driver.get(THREADS_URL)
            time.sleep(3)
            
            # Click new post button
            new_post_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class*='x1i10hfl'][role='button']")))
            new_post_button.click()
            
            # Fill in post content
            post_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']")))
            post_input.send_keys(content)
            
            # Click post button
            post_input.send_keys(Keys.COMMAND + Keys.RETURN)
            
            time.sleep(3)  # Wait for post to complete
            
        except TimeoutException:
            print("Failed to post to Threads")
            return False
        return True

    def run(self):
        if self.login_to_threads():
            content = self.get_chatgpt_response()
            if content:
                if self.post_to_threads(content):
                    print("Successfully posted to Threads!")
                else:
                    print("Failed to post to Threads")
        self.driver.quit()

def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def main():
    bot = ThreadsBot()
    bot.run()

if __name__ == "__main__":
    main()
