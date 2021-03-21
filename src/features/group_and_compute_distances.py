import pandas as pd

from haversine import haversine_vector
from pandarallel import pandarallel

from src.context import ctx
from src.config import params

def process_one_user(df_one_user):
    df_one_user = df_one_user.sort_values("timestamp")
    df_one_user["dist"] = 0
    geopositions = df_one_user[["long", "lat"]].values
    df_one_user.iloc[1:, df_one_user.columns.get_loc("dist")] = haversine_vector(
        geopositions[:-1],
        geopositions[1:],
    )
    return df_one_user

def group_and_compute_distances(df):
    result = (
        df
        .groupby("userId")
        .parallel_apply(process_one_user)
    )
    result.index.names = ["index_0", "index_1"]
    return result

if __name__ == "__main__":
    pandarallel.initialize(progress_bar=True)
    df = pd.read_csv(ctx.data_dir / "interim" / "label_encoded.csv")
    result = group_and_compute_distances(df)
    result.to_csv(ctx.data_dir / "interim" / "grouped_by_user_with_distances.csv")
