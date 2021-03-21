import pandas as pd

from src.context import ctx
from src.config import params

def categorize_geoposition(df):
    result = df[[]].copy()
    result["round_long"] = df["long"].round(params.geoposition.round_precision).astype(str)
    result["round_lat"] = df["lat"].round(params.geoposition.round_precision).astype(str)
    result["geo_place"] = result["round_long"] + "_" + result["round_lat"]
    result = result[["geo_place"]]
    return result

if __name__ == "__main__":
    df_filtered = pd.read_csv(ctx.data_dir / "interim" / "filtered_by_frequency.csv")
    result = categorize_geoposition(df_filtered)
    result.to_csv(ctx.data_dir / "interim" / "categorical_geoposition.csv")
