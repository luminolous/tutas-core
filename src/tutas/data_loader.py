import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.fillna("", inplace=True)
    valid = df[df["Topik"] != ""].reset_index(drop=True)
    return valid