# app.py
import streamlit as st
from joke_app import JokeFetcher

st.set_page_config(page_title="😂 Joke Generator", page_icon="🤣", layout="centered")
st.title("😂 Welcome to the Joke Generator!")

with st.sidebar:
    st.header("🎛 Joke Settings")
    category = st.selectbox("Category", ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"])
    joke_type = st.radio("Type", ["single", "twopart"])
    amount = st.slider("Number of Jokes", 1, 10, 1)
    lang = st.selectbox("Language", ["en", "de", "es", "fr", "cs", "pt"])

if st.button("Get Jokes"):
    fetcher = JokeFetcher(category=category, joke_type=joke_type, amount=amount, lang=lang)
    fetcher.fetch_jokes()
    
    st.subheader("🃏 Here are your jokes:")
    for i, joke in enumerate(fetcher.jokes, 1):
        st.markdown(f"**Joke {i}:**\n> {joke}")

    with st.expander("💾 Save Jokes"):
        txt_file = fetcher.save_as_txt("jokes.txt")
        pdf_file = fetcher.save_as_pdf("jokes.pdf")
        with open(txt_file, "rb") as f:
            st.download_button("📄 Download as TXT", data=f, file_name="jokes.txt")
        with open(pdf_file, "rb") as f:
            st.download_button("📝 Download as PDF", data=f, file_name="jokes.pdf")