import psycopg2
import feedparser
import torch

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification


class NewsAI:

    def __init__(self):

        print("=" * 50)
        print("📰 NEWS AI V3")
        print("=" * 50)

        # -----------------------------
        # DATABASE
        # -----------------------------

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

        # -----------------------------
        # LOAD FINBERT MODEL
        # -----------------------------

        print("Loading FinBERT AI...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            "ProsusAI/finbert"
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            "ProsusAI/finbert"
        )

        print("✅ FinBERT Loaded Successfully")


        # ----------------------------------------
        # DOWNLOAD NEWS
        # ----------------------------------------

    def fetch_news(self):

        print("\n📥 Downloading latest financial news...\n")

        url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL&region=US&lang=en-US"

        feed = feedparser.parse(url)

        if len(feed.entries) == 0:

            print("❌ No news found.")

            return []

        articles = []

        for article in feed.entries[:10]:

            title = article.title
            link = article.link
            source = "Yahoo Finance"

            # ---------------------------------
            # CHECK DUPLICATE
            # ---------------------------------

            self.cur.execute(
                """
                SELECT id
                FROM news_cache
                WHERE url=%s
                """,
                (link,)
            )

            if self.cur.fetchone():

                print("⏭ Already Exists")
                print(title)
                print()

                continue

            articles.append({

                "title": title,
                "url": link,
                "source": source

            })

        print(f"📰 {len(articles)} New Articles Found\n")

        return articles 


        # ----------------------------------------
        # AI SENTIMENT ANALYSIS
        # ----------------------------------------

    def analyze_news(self, articles):

        if len(articles) == 0:

            print("✅ No new articles to analyze.")
            return

        print("🤖 FinBERT is analyzing news...\n")

        labels = {

            0: "NEGATIVE",
            1: "NEUTRAL",
            2: "POSITIVE"

        }

        for article in articles:

            title = article["title"]

            inputs = self.tokenizer(

                title,

                return_tensors="pt",

                truncation=True,

                max_length=256

            )

            with torch.no_grad():

                outputs = self.model(**inputs)

            probabilities = torch.softmax(outputs.logits, dim=1)

            prediction = torch.argmax(probabilities).item()

            confidence = float(probabilities[0][prediction]) * 100

            sentiment = labels[prediction]

            print("📰", title)
            print("Sentiment :", sentiment)
            print("Confidence: {:.2f}%".format(confidence))
            print()

            self.cur.execute("""

                INSERT INTO news_cache
                (

                    title,
                    source,
                    sentiment,
                    url

                )

                VALUES
                (

                    %s,
                    %s,
                    %s,
                    %s

                )

            """, (

                article["title"],
                article["source"],
                sentiment,
                article["url"]

            ))

        self.conn.commit()

        print("✅ News saved successfully!") 
        
           
    # ----------------------------------------
    # CLOSE DATABASE
    # ----------------------------------------

    def close(self):

        self.cur.close()
        self.conn.close()

        print("✅ Database Connection Closed")


# ==========================================
# RUN NEWS AI
# ==========================================

if __name__ == "__main__":

    ai = NewsAI()

    try:

        articles = ai.fetch_news()

        ai.analyze_news(articles)

        print()
        print("=" * 50)
        print("📰 NEWS AI V3 FINISHED")
        print("=" * 50)

    except Exception as e:

        print()
        print("❌ NEWS AI ERROR")
        print(e)

    finally:

        ai.close()    