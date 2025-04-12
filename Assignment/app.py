# app.py
import streamlit as st
from joke_app import JokeFetcher

st.set_page_config(page_title="JokeSmith - Joke App", page_icon="😂", layout="centered")

# Styling
st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            text-align: center;
            color: #ff4b4b;
            font-weight: bold;
            margin-bottom: 10px;
            animation: fadeIn 2s ease-in-out;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #666;
            margin-bottom: 2em;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">JokeSmith 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered joke forge — brew hilarious moments instantly!</div>', unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.header("🎛 Joke Settings")
    category = st.multiselect("Category", ["Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"], default=["Programming"])
    joke_type = st.selectbox("Type", ["Any", "single", "twopart"])
    amount = st.slider("Number of Jokes", 1, 10, 1)
    lang = st.selectbox("Language", ["en", "de", "es", "fr", "cs", "pt"])
    blacklist = st.multiselect("Blacklist Flags", ["nsfw", "religious", "political", "racist", "sexist"])
    search_string = st.text_input("Search String")
    return_headers = st.checkbox("Return Headers")

# Button
if st.button("Get Jokes"):
    fetcher = JokeFetcher(
        category=category if category else None,
        blacklist=blacklist if blacklist else None,
        joke_type=joke_type,
        search_string=search_string if search_string else None,
        amount=amount,
        lang=lang,
        return_headers=return_headers
    )

    result = fetcher.fetch_jokes()

    if return_headers:
        jokes, headers = result
        st.subheader("📋 Headers Returned:")
        st.json(dict(headers))
    else:
        jokes = fetcher.jokes

    st.subheader("🃏 Here are your jokes:")
    for i, joke in enumerate(jokes, 1):
        st.markdown(f"**Joke {i}:**\n> {joke}")

    with st.expander("💾 Save Jokes"):
        txt_file = fetcher.save_as_txt("jokes.txt")
        pdf_file = fetcher.save_as_pdf("jokes.pdf")
        with open(txt_file, "rb") as f:
            st.download_button("📄 Download as TXT", data=f, file_name="jokes.txt")
        with open(pdf_file, "rb") as f:
            st.download_button("📝 Download as PDF", data=f, file_name="jokes.pdf")
