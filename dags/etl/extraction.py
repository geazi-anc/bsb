import requests
from bs4 import BeautifulSoup


def get_top5_best_sellers(url: str = 'https://www.nytimes.com/books/best-sellers/') -> list:
    """
    Extract the top5 best sellers fiction books from homepage of New York Times.

    Parameters:
        url (str): url to best sellers page of New York Times

    Returns:
        best_sellers (list): list of top5 best sellers
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    top5_list = soup.find('h2', id="combined-print-and-e-book-fiction")
    top5_list = top5_list.parent.ol

    top5_books = top5_list.find_all('li', itemprop="itemListElement")
    week = soup.time.text
    best_sellers = []

    for rank, book in enumerate(top5_books, start=1):
        weeks_on_the_list = book.p.text
        title = book.h3.text
        written_by = book.find(itemprop="author").text
        description = book.find(itemprop="description").text
        buy = [{store.text: store.get('href')}
               for store in book.ul.find_all('a')]

        best_seller = {
            'rank': rank,
            'week': week,
            'weeks_on_the_list': weeks_on_the_list,
            'title': title,
            'description': description,
            'written_by': written_by,
            'buy': buy
        }

        best_sellers.append(best_seller)

    return best_sellers
