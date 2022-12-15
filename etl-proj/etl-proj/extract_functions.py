from lib import requests, pandas as pd
from common import get_html_content, extract_table, create_df


def extract_exchange_rates(url):
    """
    extracting latest exchange rates for all the circulating currencies from REST API through an API key,
    transforming the data into a DataFrame through Pandas and
    saving it into a .csv file
    """
    response_json = requests.get(url).json()
    rates = dict(response_json["rates"])
    exchange_rate_df = pd.DataFrame(list(rates.items()), columns=["currency_code", "rate_per_1EUR"])
    exchange_rate_df.to_csv("data/processed/exchange_rates.csv")


def extract_country_codes(url):
    """
    extracting all the country codes and relevant country names through webscraping with BeautifulSoup,
    creating df with Pandas and saving it into a .csv file
    """
    soup_countries = get_html_content(url)
    table_countries = extract_table(soup_countries, "table")
    countries_df = create_df(table_countries, **{"0": "country", "3": "country_code"})

    countries_df.to_csv("data/processed/countries.csv")


def extract_currency_codes(url, tag, tag_text):
    """
    extracting all currency codes and relevant currency names through webscraping with BeautifulSoup,
    creating df with Pandas
    """
    soup_curr = get_html_content(url)
    curr_table = extract_table(soup_curr, tag, tag_text)
    return create_df(curr_table, **{"0": "country", "1": "currency", "2": "code"})