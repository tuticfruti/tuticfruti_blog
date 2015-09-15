from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from tuticfruti_blog.core.exceptions import ElementNotFoundError
from .selenium_driver import SeleniumDriver

WAITING_TIME = 2


class WebElement:
    def __init__(self, parent=None, locator=None):
        self.parent = parent
        self.locator = locator

    @property
    def text(self):
        return self._wrapped.text

    @property
    def _wrapped(self):
        try:
            if self.parent:
                return_value = self.parent._wrapped.find_element(*self.locator)
            else:
                wdw = WebDriverWait(SeleniumDriver.driver, WAITING_TIME)
                wdw.until(lambda driver: driver.find_element(*self.locator))
                return_value = SeleniumDriver.driver.find_element(*self.locator)
            return return_value
        except (TimeoutException, NoSuchElementException):
            raise ElementNotFoundError('Element not found: {}'.format(self.locator))

    def click(self):
        self._wrapped.click()

    def find_by_id(self, id):
        return WebElement(parent=self, locator=(By.ID, id))

    def find_by_class_name(self, class_name):
        return WebElement(parent=self, locator=(By.CLASS_NAME, class_name))


class WebElementCollection:
    @property
    def _wrapped(self):
        try:
            wdw = WebDriverWait(SeleniumDriver.driver, WAITING_TIME)
            wdw.until(lambda driver: driver.find_elements(*self.locator))
            return SeleniumDriver.driver.find_elements(*self.locator)
        except TimeoutException:
            raise ElementNotFoundError('Element {} not found.'.format(self.locator))

    def __len__(self):
        return len(self._wrapped)

    def __getitem__(self, key):
        return WebElement(locator=(By.ID, self._wrapped[key].get_attribute('id')))
