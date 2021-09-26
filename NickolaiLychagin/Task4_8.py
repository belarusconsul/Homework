# Task 4.8
# Implement a Pagination class helpful to arrange text on pages and list
# content on given page. The class should take in a text and a positive
# integer which indicate how many symbols will be allowed per each page
# (take spaces into account as well). You need to be able to get the
# amount of whole symbols in text, get a number of pages that came out
# and method that accepts the page number and return quantity of symbols
# on this page. If the provided number of the page is missing print the
# warning message "Invalid index. Page is missing". If you're familliar
# with using of Excpetions in Python display the error message in this way.
#  Pages indexing starts with 0.

# Optional: implement searching/filtering pages by symblos/words and
# displaying pages with all the symbols on it. If you're querying by
# symbol that appears on many pages or if you are querying by the word
# that is splitted in two return an array of all the occurences.

from re import finditer
from math import ceil


class Pagination:
    """
    Pagination class.

    INIT
        text - Type string.
        limit - Type integer. Positive integer which indicates 
                how many symbols are allowed per each page.

    ATTRIBUTES
        item_count - Type integer. Number of symbols in text.
        page_count - Type integer. Number of pages.
        
    METHODS
        count_items_on_page(page) - Return number of symbols on particular page
                                    or raise Exception if page is invalid.
        find_page(word): - Return list of page numbers where word is present 
                           or raise Exception if word is missing.
        display_page(page) - Return text on particular page  
                             or raise Exception if page is invalid.
    """
    
    def __init__(self, text, limit):
        self.text = text
        self.limit = limit
        self.item_count = len(self.text)
        self.page_count = ceil(self.item_count / limit)

    def count_items_on_page(self, page):
        if page > self.page_count - 1 or page < 0:
            raise Exception("Invalid index. Page is missing.")
        elif page < self.page_count - 1:
            return self.limit
        return self.item_count - (self.limit * (self.page_count - 1))

    def find_page(self, word):
        indices = [m.start() for m in finditer(word, self.text)]
        if not indices:
            raise Exception(f"'{word}' is missing on the pages")
        set_of_pages = set()
        for ind in indices:
            start_page = ind // 5
            end_page = (ind + len(word)) // 5
            if start_page == end_page:
                set_of_pages.add(start_page)
            else:
                set_of_pages.update(range(start_page, end_page + 1))
        return list(sorted(set_of_pages))

    def display_page(self, page):
        if page > self.page_count - 1 or page < 0:
            raise Exception("Invalid index. Page is missing.")
        start = page * self.limit
        return f"'{self.text[start: start+5]}'"


# =============================================================================
# pages = Pagination("Your beautiful text", 5)
# print(pages.page_count)
# print(pages.item_count)
# print(pages.count_items_on_page(0))
# print(pages.count_items_on_page(3))
# print(pages.count_items_on_page(4))
# print(pages.find_page("Your"))
# print(pages.find_page("e"))
# print(pages.find_page("beautiful"))
# print(pages.find_page('great'))
# print(pages.display_page(0))
# =============================================================================
