import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()


class TelegramAutomation():
    def __init__(self):
        # Initialize the WebDriver using webdriver-manager
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')

        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        self.driver.maximize_window()
        self.message = None

    def login(self):
        # Open Telegram Web
        self.driver.get('https://web.telegram.org')

        # Wait for the user to manually log in
        # print("Please log in to Telegram Web manually within 60 seconds.")
        # time.sleep(30)
        # print("30 seconds remaining...")
        # time.sleep(30)

        # Check if the login was successful
        while True:
            print("Checking if login was successful...")
            try:
                _ = self.driver.find_element(
                    By.TAG_NAME, "input")
                print("Login successful!")
                time.sleep(5)
                break
            except Exception:
                time.sleep(2)

    def go_to_source_group(self):
        # Now you can proceed to source group
        self.go_to_group(os.getenv("SOURCE_GROUP_URL"))

        # checking for new message
        while True:
            messages = self.driver.find_elements(By.CLASS_NAME, "bubble")

            if messages:
                last_message = messages[-1].text
                print("Last message:", last_message)
                if self.check_for_new_meessage(last_message):
                    if "facebook" not in last_message.lower():
                        self.message = last_message
                        print("New message found!", last_message)
                    break
            print("Waiting for 10 seconds to check for new messages...")
            time.sleep(10)

    def check_for_new_meessage(self, msg):
        if msg != self.message:
            return True
        return False

    def go_to_group(self, url):
        print("Going to the group: ", url)
        self.driver.get(url)
        print("Waiting for 10 seconds to load the group...")
        time.sleep(10)

    def format_message(self):
        """
        Covering 2 scenarios for now:
        1. Format the msg with GEMINI API
        2. Send as it is
        """
        # first trim the date from message
        msg = self.message
        msg = msg.rsplit("\n", 2)[0]

        # now try with GEMINI API else send as it is
        try:
            genai.configure(api_key=os.getenv('API_KEY'))
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            response = model.generate_content(
                f"""Please paraphrase this message, do make sure to use emojis
                but less and dont change the coin name also remove
                the yearly word: {msg}""")
            resp = response.text
            return resp
        except Exception as e:
            print("GEMINI API didn't work because:", str(e))
            print("Sending the message as it is...")
            return msg

    def send_message(self, message):
        self.driver.refresh()
        time.sleep(5)
        self.go_to_group(os.getenv("TARGET_GROUP_URL"))
        message_box = self.driver.find_element(
            By.CLASS_NAME, "input-message-input")
        message_box.send_keys(message)
        message_box.send_keys(Keys.RETURN)

    def close(self):
        print("Closing the browser in 5 seconds...")
        time.sleep(5)
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    bot = TelegramAutomation()
    try:
        # 1. Login
        bot.login()
        while True:
            # 2. Go to the source group
            bot.go_to_source_group()
            formatted_message = bot.format_message()
            print("Sending the message:", formatted_message)
            bot.send_message(formatted_message)
            print("Message sent successfully!")

    except Exception as e:
        print("An error occurred:", str(e))
        bot.close()
