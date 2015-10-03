from .web_element import WebElement, WebElementCollection
from . import locators


class HomePageLink(WebElement):
    _locator = locators.HOME_PAGE_LINK


class CategoryLink(WebElement):
    def is_enabled(self):
        return 'active' in self.get_attribute('class')


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


class CommentForm(WebElement):
    _locator = locators.COMMENT_FORM


class AuthorInput(WebElement):
    _locator = locators.AUTHOR_INPUT


class EmailInput(WebElement):
    _locator = locators.EMAIL_INPUT


class ContentTextarea(WebElement):
    _locator = locators.CONTENT_TEXTAREA


class CommentCollection(WebElementCollection):
    _locator = locators.COMMENTS


class PostDetails(WebElement):
    _locator = locators.POST_DETAILS


class CategoryCollection(WebElementCollection):
    _locator = locators.CATEGORIES


class PostTagCollection(WebElementCollection):
    _locator = locators.POST_TAGS


class PostCategoryCollection(WebElementCollection):
    _locator = locators.POST_CATEGORIES
