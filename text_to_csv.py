import pandas as pd

# Read the facts line by line
with open("data/news.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Create DataFrame
df = pd.DataFrame({
    "id": list(range(1, len(lines)+1)),
    "text": lines
})

# Save to CSV
df.to_csv("data/verified_facts.csv", index=False)