from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class TelegramAutomation():
    def __init__(self):
        # Initialize the WebDriver using webdriver-manager
        options = webdriver.ChromeOptions()
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
        print("Please log in to Telegram Web manually within 60 seconds.")
        time.sleep(60)

        # Check if the login was successful
        try:
            _ = self.driver.find_element(
                By.XPATH, '//*[contains(@class, "input-search-input")]')
            print("Login successful!")
        except Exception:
            print("Login failed. Please check your credentials and try again.")
            self.driver.quit()
            exit()

    def go_to_source_group(self, url):
        # Now you can proceed to source group
        self.go_to_group(url)
        print("Waiting for 10 seconds to load the group...")
        time.sleep(10)

        # checking for new message
        while True:
            messages = self.driver.find_elements(By.CLASS_NAME, "bubble")

            if messages:
                last_message = messages[-1].text
                print("Last message:", last_message)
                if self.check_for_new_meessage(last_message):
                    print("New message found!", last_message)
                    break
            print("Waiting for 10 seconds to check for new messages...")
            time.sleep(10)

    def check_for_new_meessage(self, msg):
        if msg != self.message:
            self.message = msg
            return True
        return False

    def go_to_group(self, url):
        self.driver.get(url)

    def format_message(self, message):
        return message

    def send_message(self, message):
        message_box = self.driver.find_element(
            By.XPATH, '//*[contains(@class, "composer_rich_textarea")]')
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
        cond = bot.login()
        # 2. Go to the source group
        bot.go_to_source_group('')
        # formatted_message = self.format_message(last_message)
        # self.go_to_group()
        # self.send_message(formatted_message)
        bot.close()
    except Exception as e:
        print("An error occurred:", str(e))
        bot.close()
