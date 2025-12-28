import streamlit as st
import requests
import pandas as pd

# Din Finnhub API-nyckel
FINNHUB_API_KEY = "d587fohr01qptoaqpcagd587fohr01qptoaqpcb0"

# Funktion för att hämta nyheter från Finnhub
def get_news(category="general"):
    url = f"https://finnhub.io/api/v1/news?category={category}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data

# Streamlit UI
st.set_page_config(page_title="Finansnyheter Dashboard", layout="wide")
st.title("📈 Finansnyheter från Finnhub")

# Filter för kategori
category = st.selectbox("Välj kategori:", ["general", "forex", "crypto", "merger", "technology"])

# Uppdateringsknapp
if st.button("🔄 Uppdatera nyheter"):
    news_data = get_news(category)
    st.success("Nyheter uppdaterade!")
else:
    news_data = get_news(category)

# Om det finns nyheter
if news_data:
    # Konvertera till DataFrame
    df = pd.DataFrame(news_data)[["headline", "summary", "source", "datetime"]]
    df["datetime"] = pd.to_datetime(df["datetime"], unit="s")

    # Visa nyheter i tabellformat
    st.subheader(f"Senaste nyheterna ({category.capitalize()}):")
    st.dataframe(df)

    # Exportera till CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Ladda ner som CSV",
        data=csv,
        file_name="finnhub_news.csv",
        mime="text/csv"
    )
else:
    st.warning("Inga nyheter hittades.")

