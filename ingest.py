from sentence_transformers import SentenceTransformer, util
import pandas as pd

model = SentenceTransformer("all-MiniLM-L6-v2")

CANONICAL_OS = ["Windows 10 Pro", "Windows 10", "macOS", "MacOS X", "Other", "Unknown OS"]
CANONICAL_OS_EMB = model.encode(CANONICAL_OS, convert_to_tensor=True)

CANONICAL_LOCATION = ["New York", "London", "Tokyo", "Remote", "Unknown"]
CANONICAL_LOCATION_EMB = model.encode(CANONICAL_LOCATION, convert_to_tensor=True)

CANONICAL_STATUS = ["active", "inactive", "maintenance"]
CANONICAL_STATUS_EMB = model.encode(CANONICAL_STATUS, convert_to_tensor=True)


def normalize(df):
    # field name standardize
    COLUMN_MAP = {
        "assigned_to": "assigned_user",
        "owner": "assigned_user",
        "user": "assigned_user",
        "os_name": "os",
        "encryption_status": "encryption"
    }

    df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns}, inplace=True)

    # null value handling
    df["os"] = df["os"].fillna("Unknown OS")
    df["location"] = df["location"].fillna("Unknown Location")
    df["status"] = df["status"].fillna("inactive")
    df["assigned_user"] = df["assigned_user"].fillna("Unassigned")

    # normalization rules
    df["os"] = feature_normalize(df['os'], CANONICAL_OS, CANONICAL_OS_EMB)
    df["location"] = feature_normalize(df['location'], CANONICAL_LOCATION, CANONICAL_LOCATION_EMB)
    df["status"] = feature_normalize(df['status'], CANONICAL_STATUS, CANONICAL_STATUS_EMB)
    df["encryption"] = df["encryption"].apply(normalize_encryption)

    df["assigned_user"] = df["assigned_user"].str.replace(".", "", regex=False).str.strip()

    return df

def normalize_encryption(val):
    if isinstance(val, str) and "enable" in val.lower():
        return True
    if isinstance(val, str) and "encrypt" in val.lower():
        return True
    return False


def feature_normalize(input, canonical, canon_emb):
    values = input.fillna("Other").astype(str).tolist()
    val_emb = model.encode(values, convert_to_tensor=True)

    # Compute cosine similarities (num_records x num_known)
    sim = util.cos_sim(val_emb, canon_emb)

    # Pick best-matching canonical value for each row
    best_idx = sim.argmax(dim=1).tolist()
    normalized = [canonical[i] for i in best_idx]

    return pd.Series(normalized, index=input.index)
