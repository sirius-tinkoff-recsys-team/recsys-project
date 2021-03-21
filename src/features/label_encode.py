import pickle

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.context import ctx
from src.config import params

def label_encode(df, encoders=None):
    result = df[[]].copy()
    encoders = encoders or dict()
    for col in ["userId", "loc_id", "geo_place"]:
        if col in encoders:
            encoder = encoders[col]
            result[col] = encoder.transform(df[col])
        else:
            encoder = LabelEncoder()
            result[col] = encoder.fit_transform(df[col])
            encoders[col] = encoder
    return result, encoders

if __name__ == "__main__":
    df_filtered = pd.read_csv(ctx.data_dir / "interim" / "filtered_by_frequency.csv")
    df_categorical_geoposition = pd.read_csv(ctx.data_dir / "interim" / "categorical_geoposition.csv")
    df = pd.concat([df_filtered, df_categorical_geoposition], axis=1)
    result, encoders = label_encode(df)
    result.to_csv(ctx.data_dir / "interim" / "label_encoded.csv", index=False)
    pickle.dump(encoders, open(ctx.root_dir / "artifacts" / "label_encoders.pkl", "wb"))
