

def format_best_seller_title(best_seller: dict) -> dict:
    """
    Transform title of best seller.

    Transform best seller title from uppercase to lowercase.
    After, each first letter of word to uppercase.

    Parameters:
        best_seller (dict): best seller dictionary, with 'title' field

    Returns:
        best_seller (dict): best_seller dictionary with transformed title
    """

    best_seller = best_seller.copy()

    title = best_seller['title']
    title = title.lower().title()

    best_seller['title'] = title
    return best_seller


def format_author_name(best_seller: dict) -> dict:
    """
    Remove 'by' word in the begin of author name.

    Parameters:
        best_seller (dict): best seller dictionary, with 'written_by' field

    Returns:
        best_seller (dict): best seller dictionary, with 'written_by' field without 'by' word in the begin
    """

    best_seller = best_seller.copy()

    written_by = best_seller['written_by']
    written_by = written_by.replace('by ', '')

    best_seller['written_by'] = written_by
    return best_seller


def convert_weeks_on_the_list_to_int(best_seller: dict) -> dict:
    """
    Transform the weeks on the list from a phrase to number.

    Remove 'weeks on the list' of the end of the phrase.
    If result is 'New', replace to 0.
    Else result is number, convert to int.

    Parameters:
        best_seller (dict): best seller dictionary, with 'weeks_on_the_list' field

    Returns:
        best_seller (dict): best seller dictionary, with 'weeks_on_the_list' converted to number
    """

    best_seller = best_seller.copy()

    weeks = best_seller['weeks_on_the_list']
    weeks = weeks.replace(' weeks on the list', '')
    weeks = 0 if weeks == 'New this week' else int(weeks)

    best_seller['weeks_on_the_list'] = weeks
    return best_seller


def apply(best_sellers: list, *funcs) -> list:
    """
    Apply transform functions to each best seller in list.

    Parameters:
        best_sellers (list): list of best sellers dictionary
        *funcs (callable): list of functions to apply in each best seller in list

    Returns:
        best_sellers (list): best sellers list transformed by functions
        """

    [[best_seller.update(func(best_seller))
      for best_seller in best_sellers] for func in funcs]

    return best_sellers
