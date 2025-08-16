CodeAlpha Task 4 – Sentiment Analysis

This project performs Sentiment Analysis on Amazon cell phone reviews. Using Natural Language Processing (NLP) techniques with the VADER sentiment analyzer, it classifies reviews as Positive, Negative, or Neutral.
The project also exports structured results to Excel and generates bar and pie chart visualizations to better understand public opinion about products.

📂 Dataset
Source: Amazon Product Data (Cell Phones & Accessories) – widely used for NLP and sentiment analysis research.

Files Used:
reviews.csv → contains user reviews (text, ratings, metadata).
items.csv → product details (brand, model, etc.) – can be merged later for brand-level insights.

🚀 Features
✔ Loads and processes Amazon reviews dataset
✔ Uses VADER (Valence Aware Dictionary for Sentiment Reasoning) for sentiment scoring
✔ Classifies reviews into:
✅ Positive
❌ Negative
⚪ Neutral
✔ Saves results in Excel (sentiment_results.xlsx)
✔ Generates visualizations:
📊 Bar Chart – Sentiment distribution
🥧 Pie Chart – Sentiment proportions
✔ Modular structure – easy to extend (e.g., analyze by brand, time trends, etc.)

🛠️ Requirements
Make sure you have Python 3.8+ installed. Install dependencies with:
   - pip install pandas nltk matplotlib seaborn openpyxl
     python -m nltk.downloader vader_lexicon

📂 Project Structure
CodeAlpha_SentimentAnalysis/
│── data/
│   └── reviews.csv              
│── output/
│   ├── sentiment_results.xlsx   
│   └── visuals/
│       ├── sentiment_bar.png     
│       └── sentiment_pie.png     
│── sentiment.py                  
│── README.md                     

📊 Outputs

Excel File → output/sentiment_results.xlsx
. Contains each review with:
    - Review Text
    - Sentiment Score (numeric compound score)
    - Sentiment Label (Positive/Negative/Neutral)
. Visualizations → stored in output/visuals/
   - Bar Chart → distribution of reviews across sentiments
   - Pie Chart → percentage share of sentiments
