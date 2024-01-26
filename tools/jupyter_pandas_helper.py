from colorama import Style, Fore
import pandas as pd

red = Style.BRIGHT + Fore.RED
blu = Style.BRIGHT + Fore.BLUE
mgt = Style.BRIGHT + Fore.MAGENTA
gld = Style.BRIGHT + Fore.YELLOW
res = Style.RESET_ALL
bold_start = Style.BRIGHT
bold_end = Style.NORMAL


def describe(df):
    """
    Function copied from a notebook of Kaggle user: https://www.kaggle.com/dreygaen
    Generate a summary of the given DataFrame.

    :param df: The DataFrame to describe.
    :return: A pandas DataFrame containing the summary statistics of the input DataFrame.
    """
    print(f'{bold_start}Data shape : {bold_end}{red}{df.shape}{res}')
    print(f'{bold_start}____________________________________________________________________{bold_end}')
    summ = pd.DataFrame(df.dtypes, columns=['data type'])
    summ['missing_#'] = df.isnull().sum().values
    summ['missing_%'] = df.isnull().sum().values / len(df) * 100
    summ['unique'] = df.nunique().values
    desc = pd.DataFrame(df.describe(include='all').transpose())
    summ['mean'] = desc['mean'].values
    summ['std'] = desc['std'].values
    summ['min'] = desc['min'].values
    summ['25%'] = desc['25%'].values
    summ['50%'] = desc['50%'].values
    summ['75%'] = desc['75%'].values
    summ['max'] = desc['max'].values

    return summ


def cat_describe(df):
    """
    Method to describe categorical columns in a pandas DataFrame.

    :param df: pandas DataFrame object
    :return: pandas DataFrame object with column descriptions
    """
    print(f'{bold_start}Data shape : {bold_end}{red}{df.shape}{res}')
    print(f'{bold_start}____________________________________________________________________{bold_end}')
    summ = pd.DataFrame(df.dtypes, columns=['data type'])
    summ['missing_#'] = df.isnull().sum().values
    summ['missing_%'] = df.isnull().sum().values / len(df) * 100
    summ['unique'] = df.nunique().values
    desc = pd.DataFrame(df.describe(include='O').transpose())
    summ['top'] = desc['top'].values
    summ['freq'] = desc['freq'].values
    summ['freq'] = summ['freq'].astype(int)

    return summ
