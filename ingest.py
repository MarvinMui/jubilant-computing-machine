from sentence_transformers import SentenceTransformer, util
import pandas as pd

model = SentenceTransformer("all-MiniLM-L6-v2")

CANONICAL_OS = ["Windows 10 Pro", "Windows 10", "macOS", "MacOS X", "Other"]
CANONICAL_OS_EMB = model.encode(CANONICAL_OS, convert_to_tensor=True)

CANONICAL_LOCATION = ["New York", "London", "Tokyo", "Remote"]
CANONICAL_LOCATION_EMB = model.encode(CANONICAL_LOCATION, convert_to_tensor=True)

CANONICAL_STATUS = ["active", "inactive", "maintenance"]
CANONICAL_STATUS_EMB = model.encode(CANONICAL_STATUS, convert_to_tensor=True)


def normalize(df):
    # normalization rules
    df["os"] = feature_normalize(df['os'], CANONICAL_OS, CANONICAL_OS_EMB)
    df["location"] = feature_normalize(df['location'], CANONICAL_LOCATION, CANONICAL_LOCATION_EMB)
    df["status"] = feature_normalize(df['status'], CANONICAL_STATUS, CANONICAL_STATUS_EMB)

    df["assigned_to"] = df["assigned_to"].str.replace(".", "", regex=False).str.strip()

    # Insert into DuckD
    return df


def feature_normalize(input, canonical, canon_emb):
    values = input.fillna("Other").astype(str).tolist()
    val_emb = model.encode(values, convert_to_tensor=True)

    # Compute cosine similarities (num_records x num_known)
    sim = util.cos_sim(val_emb, canon_emb)

    # Pick best-matching canonical value for each row
    best_idx = sim.argmax(dim=1).tolist()
    normalized = [canonical[i] for i in best_idx]

    return pd.Series(normalized, index=input.index)
