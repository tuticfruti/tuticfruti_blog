from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from tuticfruti_blog.core.utils import singleton
from .selenium_driver import SeleniumDriver
from .locators import CommonLocators

WAITING_TIME = 5


class WebElement:
    @property
    def wrapped(self):
        try:
            wdw = WebDriverWait(SeleniumDriver().driver, WAITING_TIME)
            wdw.until(lambda driver: driver.find_element(*self.locator))
            return SeleniumDriver().driver.find_element(*self.locator)
        except TimeoutException:
            return None

    def click(self):
        self.wrapped.click()


class WebElementCollection:
    @property
    def wrapped(self):
        try:
            wdw = WebDriverWait(SeleniumDriver().driver, WAITING_TIME)
            wdw.until(lambda driver: driver.find_elements(*self.locator))
            return SeleniumDriver().driver.find_elements(*self.locator)
        except TimeoutException:
            return None

    def __len__(self):
        return len(self.wrapped)


class HomeLink(WebElement):
    locator = CommonLocators.HOME_LINK


class PythonCategoryLink(WebElement):
    locator = CommonLocators.PYTHON_CATEGORY_LINK


class DjangoCategoryLink(WebElement):
    locator = CommonLocators.DJANGO_CATEGORY_LINK


class MiscellaneousCategoryLink(WebElement):
    locator = CommonLocators.MISCELLANEOUS_CATEGORY_LINK


class PostsCollection(WebElementCollection):
    locator = CommonLocators.POSTS
