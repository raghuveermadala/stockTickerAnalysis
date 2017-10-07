#!/usr/bin/python3

from scrapers.scrape import scrape_page
# if you want to use this scraper without the RESTful api webservice then
# change this import: from scrape import scrape_page
import re

try:
    import pandas as pd
    pandasImported = True
except ImportError:
    pandasImported = False

BASE_URL = "http://finviz.com/quote.ashx?t="
VALUE_NAMES_XPATH = '//*[@class="snapshot-td2-cp"]/text()'
VALUES_XPATH = '//*[@class="snapshot-td2"]/b/text() | //*[@class="snapshot-td2"]/b/*/text()'

def get_statistics_table(page):
    """
    This function will return the financial statistics table on a stock's finviz page, if it exists as a
    Python dictionary
    :param page: HTML tree structure based on the html markup of the scraped web page.
    :return: a dictionary of all the financial statistics listed on a stock's finviz page, otherwise will
    return a empty dictionary
    """
    value_names = page.xpath(VALUE_NAMES_XPATH)

    values = page.xpath(VALUES_XPATH)
    values = [value if value != "-" else None for value in values]

    table = dict(zip(value_names, values))

    return table

def get_statistic(ticker_symbol, stat_name, page=None):
    """
    This function will get the associated financial statistic from the corresponding finviz page given the
    statistic's name and the ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param stat_name: The name of the interested financial statistic (e.g., "P/E", "Price", "Volume").
    An exhaustive list of available financial statistics can be found on a stock's finviz page
    :param page: HTML tree structure based on the html markup of the scraped web page. If one is not passed in the
    function will scrape the page
    :return: the value of the interested financial statistic if it exists, otherwise None
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    table = get_statistics_table(page)

    if stat_name in table.keys() and table[stat_name]:
        return table[stat_name]
    else:
        return None

def get_all_statistics(ticker_symbol, page=None):
    """
    This function will get all the associated financial statistics from the correspoding finviz page
    given the ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GGOG", "MSFT")
    :param page: HTML tree structure based on the html markup of the scraped page. If one is not passed in the
    function will scrape the page
    :return: a dictionary of all the financial statistics listed on a stock's finviz page, otherwise None
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    table = get_statistics_table(page)

    if table:
        return table
    else:
        return None

def get_all_statistics_series(ticker_symbol):
    """
    Return pandas Series of ticker symbol. Try to convert to numeric.
    """

    if not pandasImported:
        raise Exception("Pandas not installed.")

    d = get_all_statistics(ticker_symbol)

    new_dict = {}

    for k,v in d.items():
        if v == None:
            continue
        if ('%' in v) and (v.index('%') == (len(v)-1)):
            # percent
            new_dict[k + '(%)'] = float(v[:-1])
        elif (k == '52W Range'):
            m = re.match('([0-9\.\-]+) - ([0-9\.\-]+)',v)
            new_dict['52W Low'] = float(m.group(1))
            new_dict['52W High'] = float(m.group(2))
        else:
            try:
                # remove any commas
                v = re.sub(',','',v)
                v = re.sub('B','E9',v)  # expoentiate billions
                v = re.sub('M','E6',v)
                v = re.sub('K','E3',v)
                new_dict[k] = float(v)
            except ValueError:
                new_dict[k] = v


    return pd.Series(new_dict)

def get_all_statistics_df(symbol_list):
    """Return a dataframe for a list of symbols.
    """
    series = []

    for s in symbol_list:
        series.append(get_all_statistics_series(s))

    return pd.DataFrame(series,index=symbol_list)


if __name__ == "__main__":
    # Test Cases
    print(get_statistic("AAPL", "P/E"))
    print(get_statistic("AAPL", "Inst Own"))
    print(get_statistic("AAPL", "Change"))
    print(get_statistic("AAPL", "This should return None"))
    print(get_all_statistics("AAPL"))
