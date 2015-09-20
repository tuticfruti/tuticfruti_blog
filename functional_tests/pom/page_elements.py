from .web_element import WebElement, WebElementCollection
from . import locators


class HomePageLink(WebElement):
    _locator = locators.HOME_PAGE_LINK


class CategoryLink(WebElement):
    def is_enabled(self):
        return 'active' in self.get_attribute('class')


class PythonCategoryLink(WebElement):
    _locator = locators.PYTHON_CATEGORY_LINK


class DjangoCategoryLink(WebElement):
    _locator = locators.DJANGO_CATEGORY_LINK


class MiscellaneousCategoryLink(WebElement):
    _locator = locators.MISCELLANEOUS_CATEGORY_LINK


class Container(WebElement):
    _locator = locators.CONTAINER


class PrevLink(WebElement):
    _locator = locators.PREV_LINK


class NextLink(WebElement):
    _locator = locators.NEXT_LINK


class PostCollection(WebElementCollection):
    _locator = locators.POSTS


class SearchForm(WebElement):
    _locator = locators.SEARCH_FORM


class SearchFormInput(WebElement):
    _locator = locators.SEARCH_FORM_INPUT


class SearchFormButton(WebElement):
    _locator = locators.SEARCH_FORM_BUTTON
