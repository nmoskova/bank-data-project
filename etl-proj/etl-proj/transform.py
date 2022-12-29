from lib import pandas as pd


def create_df(table, subset, **kwargs):  # {i: value}
    df = pd.read_html(str(table), flavor="bs4")[0]
    columns = df.columns

    renamed_columns = {}
    for k, v in kwargs.items():
        renamed_columns[columns[int(k)]] = v

    df.rename(columns=renamed_columns, inplace=True)
    df = df[[v for k, v in renamed_columns.items()]]

    df[subset] = [x.capitalize() for x in df[subset]]
    return df


def create_common_table(df1, df2, left_on, right_on, how):
    table = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)
    # duplicated = table.loc[table.duplicated(subset=["country", "country_code"], keep=False), :]
    table = table.drop_duplicates(subset=[left_on])
    table = table.dropna().reset_index(drop=True)
    return table


def create_currencies_table(df1, df2, left_on, right_on, how):
    path = "data/currencies.csv"
    currencies = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)
    currencies = currencies.iloc[:, [0, 1, 4]]
    currencies.drop_duplicates(inplace=True)
    currencies.set_index([left_on], inplace=True)
    currencies.to_csv(path)


def drop_wrong_values(df1, subset1_df1, subset2_df1, df2, subset_df2, substring=None):
    # make  set of the correct values from df2
    correct_values_df2 = set(df2[subset_df2].values)

    # finds duplicated values in subset1_df1 from df1
    duplicated_df1 = df1.loc[df1.duplicated(subset=subset1_df1, keep=False), :]
    duplicated_df1_ind = duplicated_df1.index

    # makes set of incorrect values.indexes which contain certain substring
    wrong_values_from_df1_ind = set()
    if substring:
        wrong_values_from_df1_ind = find_incorrect_values(df1, subset1_df1, substring)

    # gather wrong values indexes and duplicated indexes in one set
    values_to_remove = wrong_values_from_df1_ind.union(set(duplicated_df1_ind))

    # checks if values from subset2_df1 from duplicated_df1 exist in correct_values_df2 and makes set of their indexes
    correct_indexes_df1 = set(
        duplicated_df1_ind[(duplicated_df1[subset2_df1].isin(correct_values_df2))].to_list())

    # subtracts the correct_indexes from values_to_remove
    rows_to_remove = list(values_to_remove.difference(correct_indexes_df1))

    # drops the incorrect rows
    df1.drop(rows_to_remove, inplace=True)
    df1.sort_values(subset2_df1)
    return df1


def find_incorrect_values(df, subset, substr):
    return set(df[df["country"].str.contains("Zz")].index)