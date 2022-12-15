from lib import requests, pandas as pd, BeautifulSoup


def get_html_content(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")

    return soup


def extract_table(soup, tag, text=None):
    table = ''
    if not text:
        table = soup.find(tag)
    else:
        for t in soup.find_all(tag):
            if t.get_text() == text:
                table = t.find_parent("table")
                break
    return table


def create_df(table, **kwargs):  # {i: value}
    df = pd.read_html(str(table), flavor="bs4")[0]
    columns = df.columns

    renamed_columns = {}
    for k, v in kwargs.items():
        renamed_columns[columns[int(k)]] = v

    df.rename(columns=renamed_columns, inplace=True)
    df = df[[v for k, v in renamed_columns.items()]]

    df["country"] = [x.capitalize() for x in df["country"]]
    return df


def drop_duplicates(df, df_to_compare, subset):
    codes_from_exchange_rate_table = set(df_to_compare.currency_code.values)

    duplicated_codes_from_df = df.loc[df.duplicated(subset=subset, keep=False), :]
    duplicated_codes_from_df_ind = duplicated_codes_from_df.index

    wrong_values_from_df_ind = set(df[df["country"].str.contains("Zz")].index)
    values_to_remove = wrong_values_from_df_ind.union(set(duplicated_codes_from_df_ind))

    correct_codes_indexes = set(
        duplicated_codes_from_df_ind[(duplicated_codes_from_df['code'].isin(codes_from_exchange_rate_table))].to_list())

    rows_to_remove = list(values_to_remove.difference(correct_codes_indexes))

    df.drop(rows_to_remove, inplace=True)
    df.sort_values("code")
    return df


def create_common_table(df1, df2, left_on, right_on, how):
    table = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)
    # duplicated = table.loc[table.duplicated(subset=["country", "country_code"], keep=False), :]
    table = table.drop_duplicates(subset=['country'])
    table = table.dropna().reset_index(drop=True)
    return table


def create_currencies_table(df1, df2, left_on, right_on, how):
    currencies = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)
    currencies = currencies.iloc[:, [0, 1, 4]]
    currencies.drop_duplicates(inplace=True)
    currencies.set_index(["code"], inplace=True)
    currencies.to_csv("data/processed/currencies.csv")










