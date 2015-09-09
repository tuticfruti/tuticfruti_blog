from selenium import webdriver


class SeleniumDriver:

    @classmethod
    def open(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def close(cls):
        if cls.driver:
            cls.driver.quit()
