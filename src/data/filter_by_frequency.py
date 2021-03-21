import pandas as pd

from src.context import ctx
from src.config import params

def filter_by_frequency(df):
    deduplicated = df.drop_duplicates(
        subset=["userId", "loc_id"], 
        keep="first"
    )
    location_to_unique_visitors_count = (
        deduplicated
        .groupby("loc_id")
        .agg({"userId": "count"})
        .reset_index()
    )
    satisfying_locations = location_to_unique_visitors_count[
        location_to_unique_visitors_count.userId > params.filter.required_unique_visitors
    ].loc_id
    visitor_to_unique_places_count = (
        deduplicated
        .groupby("userId")
        .agg({"loc_id": "count"})
        .reset_index()
    )
    satisfying_visitors = visitor_to_unique_places_count[
        visitor_to_unique_places_count.loc_id > params.filter.required_unique_places
    ].userId
    result = df.loc[
        df.loc_id.isin(satisfying_locations) & 
        df.userId.isin(satisfying_visitors)
    ]
    return result

if __name__ == "__main__":
    df = pd.read_csv(
        ctx.data_dir / "raw" / "loc-brightkite_totalCheckins.txt",
        sep="\t",
        header=None,
        names=["userId","timestamp","long","lat","loc_id"],
    )
    result = filter_by_frequency(df)
    result.to_csv(ctx.data_dir / "interim" / "filtered_by_frequency.csv", index=False)
