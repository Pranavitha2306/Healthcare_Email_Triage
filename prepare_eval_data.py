import pandas as pd
from routing import EMERGENCY_WORDS

df = pd.read_csv("eval_emails.csv")

def auto_type(row):
    text = row["email"].lower()
    if row["expected_route"] == "emergency":
        if any(word in text for word in EMERGENCY_WORDS):
            return "emergency"
        return "emergency_no_keyword"
    if row["expected_route"] == "no_documents":
        return "out_of_scope"
    return "routine"

df["split"] = df["split"].fillna("dev")

needs_type = df["type"].isna() | (df["type"] == "<type>")
df.loc[needs_type, "type"] = df[needs_type].apply(auto_type, axis=1)

print(df["type"].value_counts())
df.to_csv("eval_emails.csv", index=False)
print("saved eval_emails.csv")
