from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .selenium_driver import SeleniumDriver
from .locators import CommonLocators

WAITING_TIME = 5


class WebElementMixin:
    @property
    def _wrapped(self):
        try:
            wdw = WebDriverWait(SeleniumDriver.driver, WAITING_TIME)
            wdw.until(lambda driver: driver.find_element(*self.locator))
            return SeleniumDriver.driver.find_element(*self.locator)
        except TimeoutException:
            return None

    def click(self):
        self._wrapped.click()


class WebElementCollectionMixin:
    @property
    def _wrapped(self):
        try:
            wdw = WebDriverWait(SeleniumDriver.driver, WAITING_TIME)
            wdw.until(lambda driver: driver.find_elements(*self.locator))
            return SeleniumDriver.driver.find_elements(*self.locator)
        except TimeoutException:
            return None

    def __len__(self):
        return len(self._wrapped)


class HomeLink(WebElementMixin):
    locator = CommonLocators.HOME_LINK


class CategoryLink(WebElementMixin):
    def is_active(self):
        return 'active' in self._wrapped.get_attribute('class')


class PythonCategoryLink(CategoryLink):
    locator = CommonLocators.PYTHON_CATEGORY_LINK


class DjangoCategoryLink(CategoryLink):
    locator = CommonLocators.DJANGO_CATEGORY_LINK


class MiscellaneousCategoryLink(CategoryLink):
    locator = CommonLocators.MISCELLANEOUS_CATEGORY_LINK


class PostsCollection(WebElementCollectionMixin):
    locator = CommonLocators.POSTS
