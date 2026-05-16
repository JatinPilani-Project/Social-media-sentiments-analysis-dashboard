import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Sentiment Dashboard", layout="wide")

st.title("AI Social Media Sentiment Dashboard")
st.subheader("Developed by Jatin Pilani")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    text_column = st.selectbox("Select Text Column", df.columns)

    df["Sentiment"] = df[text_column].apply(analyze_sentiment)

    st.write("### Dataset Preview")
    st.dataframe(df.head())

    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    fig = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Sentiment Distribution"
    )

    st.plotly_chart(fig)

    st.write("### Sentiment Counts")
    st.bar_chart(df["Sentiment"].value_counts())

    text = " ".join(df[text_column].astype(str))

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    fig2, ax = plt.subplots(figsize=(10,5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    st.pyplot(fig2)

else:
    st.info("Upload a CSV file containing social media comments/posts.")