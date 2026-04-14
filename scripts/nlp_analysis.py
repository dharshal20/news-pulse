"""
nlp_analysis.py
---------------
All NLP logic lives here.
- Sentiment scoring using VADER
- Keyword extraction using YAKE
- Topic classification using keyword matching (no ML needed)
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

try:
    import yake
    _keyword_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=8, features=None)
    _use_yake = True
except ImportError:
    from rake_nltk import Rake
    _rake = Rake()
    _use_yake = False

# ── Topic keyword map ─────────────────────────────────────────────────────────
TOPIC_KEYWORDS = {
    "Politics":  ["election", "government", "president", "minister", "parliament",
                  "senate", "congress", "vote", "policy", "democrat", "republican",
                  "modi", "biden", "trump", "political", "party", "campaign"],
    "Economy":   ["economy", "inflation", "gdp", "market", "stock", "trade",
                  "recession", "bank", "interest rate", "budget", "tax", "finance",
                  "investment", "rupee", "dollar", "fiscal", "revenue", "debt"],
    "Technology":["technology", "ai", "artificial intelligence", "software",
                  "startup", "apple", "google", "microsoft", "meta", "tesla",
                  "robot", "cyber", "hack", "data", "app", "tech", "openai"],
    "Health":    ["health", "hospital", "disease", "vaccine", "covid", "cancer",
                  "medicine", "doctor", "who", "pandemic", "virus", "treatment",
                  "drug", "patient", "mental health", "surgery", "medical"],
    "Climate":   ["climate", "environment", "carbon", "emission", "global warming",
                  "flood", "drought", "renewable", "solar", "pollution", "wildlife",
                  "forest", "weather", "earthquake", "storm", "disaster"],
    "Sports":    ["cricket", "football", "ipl", "fifa", "olympic", "player",
                  "match", "tournament", "champion", "score", "goal", "team",
                  "league", "trophy", "coach", "stadium", "athlete"],
    "Crime":     ["crime", "murder", "arrest", "police", "court", "jail", "fraud",
                  "terror", "attack", "shooting", "death", "killed", "robbery",
                  "scam", "corruption", "investigation", "sentence"],
}


def get_sentiment(text: str) -> dict:
    """
    Returns sentiment label and compound score for a given text string.

    Returns:
        {
            "label": "positive" | "negative" | "neutral",
            "score": float between -1 and 1
        }
    """
    if not text or not text.strip():
        return {"label": "neutral", "score": 0.0}

    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {"label": label, "score": round(compound, 4)}

def get_keywords(text: str) -> list:
    if not text or not text.strip():
        return []
    try:
        if _use_yake:
            keywords_with_scores = _keyword_extractor.extract_keywords(text)
            return [keyword for keyword, score in keywords_with_scores][:8]
        else:
            _rake.extract_keywords_from_text(text)
            phrases = _rake.get_ranked_phrases()
            return phrases[:8]
    except Exception:
        return []



def classify_topic(title: str, description: str) -> str:
    """
    Classifies an article into a topic using keyword matching.
    No ML — just checks if known keywords appear in the text.

    Returns:
        Topic string e.g. "Politics", or "General" if no match found.
    """
    combined = (title + " " + (description or "")).lower()

    topic_scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in combined)
        if count > 0:
            topic_scores[topic] = count

    if not topic_scores:
        return "General"

    # Return the topic with the most keyword matches
    return max(topic_scores, key=topic_scores.get)


def analyse_article(title: str, description: str) -> dict:
    """
    Full NLP pipeline for one article.
    Combines sentiment + keywords + topic into one result dict.

    Returns:
        {
            "sentiment": "positive" | "negative" | "neutral",
            "score": float,
            "keywords": "keyword1, keyword2, ...",
            "topic": "Politics"
        }
    """
    text = title + ". " + (description or "")
    sentiment_result = get_sentiment(text)
    keywords = get_keywords(text)
    topic = classify_topic(title, description or "")

    return {
        "sentiment": sentiment_result["label"],
        "score":     sentiment_result["score"],
        "keywords":  ", ".join(keywords),
        "topic":     topic
    }
