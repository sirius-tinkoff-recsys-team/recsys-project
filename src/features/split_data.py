import pandas as pd
from sklearn.model_selection import train_test_split

from src.context import ctx
from src.config import params

def split_data(df):
    unique_users = df.index.get_level_values(0).unique()
    users_train, users_test = train_test_split(
        unique_users, 
        test_size=params.split.test_size,
        random_state=params.split.random_state,
    )
    train_df, test_df = df.loc[users_train], df.loc[users_test]
    return train_df, test_df

if __name__ == "__main__":
    df = pd.read_csv(ctx.data_dir / "interim" / "grouped_by_user_with_distances.csv", index_col=[0, 1])
    train_df, test_df = split_data(df)
    train_df.to_csv(ctx.data_dir / "processed" / "train.csv")
    test_df.to_csv(ctx.data_dir / "processed" / "test.csv")
