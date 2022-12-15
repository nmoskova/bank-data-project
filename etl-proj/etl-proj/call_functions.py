from extract_functions import extract_country_codes, extract_exchange_rates, \
    extract_currency_codes
from lib import pandas as pd
from common import drop_duplicates, create_common_table, create_currencies_table


url_countries = "https://www.worldometers.info/country-codes/"

url_currency_codes = 'https://docs.1010data.com/1010dataReferenceManual/DataTypesAndFormats/currencyUnitCodes.html'
span_text = 'ISO 4217 Codes'

base = "EUR"
apikey = "HG34EOgHmTDKtWU407NnrCTajE7WhZnG"
url = f'https://api.apilayer.com/exchangerates_data/latest?base={base}&apikey={apikey}'


extract_exchange_rates(url)
extract_country_codes(url_countries)

curr_df = extract_currency_codes(url_currency_codes, "span", span_text)

exchange_rates_df = pd.read_csv("data/processed/exchange_rates.csv")
countries_df = pd.read_csv("data/processed/countries.csv")

curr_df_cleaned = drop_duplicates(curr_df, exchange_rates_df, subset=["country"])
common_table = create_common_table(curr_df_cleaned, countries_df, left_on="country", right_on="country", how="left")

country_codes = common_table.iloc[:, [4, 0, 2]]
country_codes.to_csv("data/processed/country_codes.csv")

currency_codes = common_table[["code", "currency"]]
create_currencies_table(currency_codes, exchange_rates_df, left_on="code", right_on="currency_code", how="inner")
