import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.context import ctx
from src.config import params

def split_data(df):
    quantile = params.split.time_based_train_size
    dt = pd.to_datetime(df.timestamp)
    threshold = pd.to_datetime(np.quantile(dt.values.astype("int64"), quantile))
    train_df, test_df = df[dt.values < threshold], df[dt.values >= threshold]
    return train_df, test_df

if __name__ == "__main__":
    df = pd.read_csv(ctx.data_dir / "interim" / "grouped_by_user_with_distances.csv", index_col=[0, 1])
    train_df, test_df = split_data(df)
    train_df.to_csv(ctx.data_dir / "interim" / "time_based_split_train.csv")
    test_df.to_csv(ctx.data_dir / "interim" / "time_based_split_test.csv")
