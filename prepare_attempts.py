'''
Description of the program
'''
import pandas as pd
import random


def rename_column(col):
    if '@' in col:
        return col.split('@')[-1]
    else:
        return col

def main():
    df = pd.read_csv('problem_per_user.csv')
    rename_to = {column: rename_column(column) for column in df.columns}
    df.rename(rename_to, inplace=True, axis='columns')
    const_cols = df.columns[ df.nunique()==1 ]
    df.drop(const_cols, inplace=True, axis='columns')
    columns_to_maybe_drop = [col for col in df.columns if len(col) == 32]
    num_to_drop = len(columns_to_maybe_drop) - 10
    cols_to_drop = random.sample(columns_to_maybe_drop, num_to_drop)
    df.drop(cols_to_drop, inplace=True, axis='columns')
    df['average_grade'] = df.apply(lambda row: round(row['average_grade'], 2),axis=1)
    df.fillna(0, axis='columns', inplace=True)
    df.to_csv('problem_per_user.csv', index=False)


if __name__ == '__main__':
    main()

