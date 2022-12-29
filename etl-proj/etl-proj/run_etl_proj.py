from extract import extract_country_codes, extract_exchange_rates, \
    extract_currency_codes
from lib import pandas as pd
from transform import drop_wrong_values, create_common_table, create_currencies_table


base = "EUR"
apikey = "HG34EOgHmTDKtWU407NnrCTajE7WhZnG"
url_api = f'https://api.apilayer.com/exchangerates_data/latest?base={base}&apikey={apikey}'

url_countries = "https://www.worldometers.info/country-codes/"

url_currency_codes = 'https://docs.1010data.com/1010dataReferenceManual/DataTypesAndFormats/currencyUnitCodes.html'
span_text = 'ISO 4217 Codes'


def main():
    # step 1: extract exchange rates table and save it in "data/exchange_rates.csv"
    extract_exchange_rates(url_api)

    # step 2: extract country_codes table and save it in "data/countries.csv"
    extract_country_codes(url_countries)

    # step 3: extract currencies table and save it in "data/currency_codes.csv"
    extract_currency_codes(url_currency_codes, "span", span_text)

    # step 4: open exchange_rates, countries and currencies as df
    exchange_rates_df = pd.read_csv("data/exchange_rates.csv")
    countries_df = pd.read_csv("data/countries.csv")
    currency_codes_df = pd.read_csv("data/currency_codes.csv")

    # step 5: drop incorrect values from currency_codes_df
    curr_df_cleaned = drop_wrong_values(currency_codes_df, *["country"], "code", exchange_rates_df, "currency_code", "Zz")

    # step 6: join tables curr_df_cleaned and countries_df
    common_table = create_common_table(curr_df_cleaned, countries_df, left_on="country", right_on="country", how="left")

    # step 7: create a country_codes.csv file from common_table, columns 4, 0, 2
    country_codes = common_table.iloc[:, [4, 0, 2]]
    country_codes.to_csv("data/country_codes.csv")

    # step 8: create currencies.csv
    currency_codes = common_table[["code", "currency"]]
    create_currencies_table(currency_codes, exchange_rates_df, left_on="code", right_on="currency_code", how="inner")


if __name__ == '__main__':
    main()

