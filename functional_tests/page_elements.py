from .web_element_wrapper import WebElement, WebElementCollection
from .locators import CommonLocators


class HomeLink(WebElement):
    locator = CommonLocators.HOME_LINK


class CategoryLink(WebElement):
    def is_active(self):
        return 'active' in self._wrapped.get_attribute('class')


class PythonCategoryLink(CategoryLink):
    locator = CommonLocators.PYTHON_CATEGORY_LINK


class DjangoCategoryLink(CategoryLink):
    locator = CommonLocators.DJANGO_CATEGORY_LINK


class MiscellaneousCategoryLink(CategoryLink):
    locator = CommonLocators.MISCELLANEOUS_CATEGORY_LINK


class PostsCollection(WebElementCollection):
    locator = CommonLocators.POSTS


class PaginationPrevLink(WebElement):
    locator = CommonLocators.PAGINATION_PREV_LINK


class PaginationNextLink(WebElement):
    locator = CommonLocators.PAGINATION_NEXT_LINK


class Container(WebElement):
    locator = CommonLocators.CONTAINER
