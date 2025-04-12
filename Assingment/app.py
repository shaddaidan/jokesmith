# app.py
import streamlit as st
from joke_app import JokeFetcher

st.set_page_config(
    page_title="JokeSmith - Joke App",
    page_icon="😂",
    layout="centered"
)

# 💥 Custom CSS for styling and animation
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


        .btn {
            align:center;
            padding: 5em ;
        }

        }
    </style>
""", unsafe_allow_html=True)

# 💡 Title and Subtitle
st.markdown('<div class="main-title">JokeSmith 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered joke forge — brew hilarious moments instantly!</div>', unsafe_allow_html=True)


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







# with st.sidebar:
#     st.header("🎛 Joke Settings")
#     category = st.selectbox("Category", ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"])
#     joke_type = st.radio("Type", ["single", "twopart"])
#     amount = st.slider("Number of Jokes", 1, 10, 1)

# if st.container():
#     st.markdown('<div class="btn">', unsafe_allow_html=True)
#     st.button("Get Jokes")
#     st.markdown('</div>', unsafe_allow_html=True)
#     fetcher = JokeFetcher(category=category, joke_type=joke_type, amount=amount)
#     fetcher.fetch_jokes()
    
#     st.subheader("🃏 Here are your jokes:")
#     for i, joke in enumerate(fetcher.jokes, 1):
#         st.markdown(f"**Joke {i}:**\n> {joke}")

#     with st.expander("💾 Save Jokes"):
#         txt_file = fetcher.save_as_txt("jokes.txt")
#         pdf_file = fetcher.save_as_pdf("jokes.pdf")
#         with open(txt_file, "rb") as f:
#             st.download_button("📄 Download as TXT", data=f, file_name="jokes.txt")
#         with open(pdf_file, "rb") as f:
#             st.download_button("📝 Download as PDF", data=f, file_name="jokes.pdf")