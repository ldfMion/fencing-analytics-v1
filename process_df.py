import pandas as pd


def add_touches_to_df(df: pd.DataFrame):
    # --- Step 1: Identify touches that count as a score ---
    # We'll assume only rows with a valid 'Side' and 'Action' indicate a scored touch.
    # Adjust this logic based on your own data definition.
    df["scored"] = df["Side"].isin(["L", "R"]) & df["Action"].notna()

    # --- Step 2: Determine who scored on each row ---
    df["left_score_touch"] = (df["Side"] == "L") & df["scored"]
    df["right_score_touch"] = (df["Side"] == "R") & df["scored"]

    # --- Step 3: Group by bout (Left Fencer vs Right Fencer) ---
    # Assuming one unique matchup at a time
    df["bout_id"] = df["Left Fencer"] + " vs " + df["Right Fencer"]

    # --- Step 4: Calculate cumulative scores in order ---
    df["Left Score"] = df.groupby("bout_id")["left_score_touch"].cumsum()
    df["Right Score"] = df.groupby("bout_id")["right_score_touch"].cumsum()

    # Drop intermediate logical columns if desired
    df = df.drop(columns=["scored", "left_score_touch", "right_score_touch"])

    return df
