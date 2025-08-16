import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

DATA_DIR = "data"
OUTPUT_DIR = "output"
VIS_DIR = os.path.join(OUTPUT_DIR, "visuals")
os.makedirs(VIS_DIR, exist_ok=True)

def find_reviews_file():
    candidates = []
    for ext in ("*.csv","*.xlsx"):
        candidates.extend(glob.glob(os.path.join(DATA_DIR, f"*review*{ext}")))
        candidates.extend(glob.glob(os.path.join(DATA_DIR, f"*reviews*{ext}")))
    if not candidates:
        raise FileNotFoundError("No reviews file found in ./data (expected *review*.csv or *review*.xlsx).")
    return candidates[0]

def read_any(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1")
    elif ext in (".xlsx",".xls"):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def pick_text_column(df):
    candidates = ["reviewText","review_text","review","text","content","body","review_body","reviewBody","summary","title"]
    for c in candidates:
        if c in df.columns:
            return c
    raise KeyError(f"No review text column found. Available columns: {list(df.columns)}")

try:
    reviews_path = find_reviews_file()
    df = read_any(reviews_path)
    
    if df.empty:
        raise ValueError("The reviews file is empty.")
    
    print("🟢 Data loaded:", reviews_path, df.shape)
except Exception as e:
    raise SystemExit(f"❌ {e}")

# Ensure NLTK data is available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("📥 Downloading NLTK vader_lexicon...")
    nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

text_col = pick_text_column(df)

# Validate text column
if df[text_col].isna().all():
    raise ValueError(f"Text column '{text_col}' contains no valid text data.")

df[text_col] = df[text_col].astype(str).fillna("")

# Filter out empty strings
df = df[df[text_col].str.strip() != ""]
if df.empty:
    raise ValueError("No valid text data found for sentiment analysis.")

df["SentimentScore"] = df[text_col].apply(lambda x: sia.polarity_scores(x)["compound"])
def lab(s):
    return "Positive" if s > 0.05 else ("Negative" if s < -0.05 else "Neutral")
df["Sentiment"] = df["SentimentScore"].apply(lab)

os.makedirs(OUTPUT_DIR, exist_ok=True)
out_xlsx = os.path.join(OUTPUT_DIR, "sentiment_results.xlsx")
df[[text_col,"SentimentScore","Sentiment"]].to_excel(out_xlsx, index=False)
print("📊 Results saved:", out_xlsx)

counts = df["Sentiment"].value_counts()
plt.figure(figsize=(6,4))
sns.barplot(x=counts.index, y=counts.values)
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "sentiment_bar.png"))
plt.close()

plt.figure(figsize=(6,6))
plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%")
plt.title("Sentiment Distribution")
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "sentiment_pie.png"))
plt.close()

print("✅ Charts saved in:", VIS_DIR)
print("📈 Sentiment analysis completed successfully!")
