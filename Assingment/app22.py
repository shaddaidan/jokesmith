# app.py
import streamlit as st
from joke_app import JokeFetcher
from streamlit.components.v1 import html

st.set_page_config(
    page_title="JokeSmith - AI Joke App",
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
        .section {
            border-radius: 15px;
            padding: 1.5em;
            margin-bottom: 1.5em;
            background: #f9f9f9;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            animation: slideUp 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# 💡 Title and Subtitle
st.markdown('<div class="main-title">JokeSmith 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered joke forge — brew hilarious moments instantly!</div>', unsafe_allow_html=True)

# 🔧 Joke Settings Section
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("🎛 Joke Settings")
    category = st.selectbox("Choose a Category", ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"])
    joke_type = st.radio("Joke Type", ["single", "twopart"], horizontal=True)
    amount = st.slider("Number of Jokes", 1, 10, 1)
    st.markdown("</div>", unsafe_allow_html=True)

# 🚀 Joke Generation Section
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("😂 Generate Your Jokes")

    if st.button("🎉 Fetch Jokes"):
        fetcher = JokeFetcher(category=category, joke_type=joke_type, amount=amount)
        fetcher.fetch_jokes()

        for i, joke in enumerate(fetcher.jokes, 1):
            st.markdown(f"""
            <div style="margin-bottom: 1em; padding: 1em; border-left: 5px solid #ff4b4b; background-color: #fff;">
            <strong>Joke {i}</strong><br>
            <span style="font-size: 1.1em;">{joke}</span>
            </div>
            """, unsafe_allow_html=True)

        # Save Options
        st.markdown("### 💾 Save These Jokes")
        col1, col2 = st.columns(2)
        with col1:
            txt_file = fetcher.save_as_txt("jokes.txt")
            with open(txt_file, "rb") as f:
                st.download_button("📄 Download as TXT", data=f, file_name="jokes.txt")
        with col2:
            pdf_file = fetcher.save_as_pdf("jokes.pdf")
            with open(pdf_file, "rb") as f:
                st.download_button("📝 Download as PDF", data=f, file_name="jokes.pdf")

    st.markdown("</div>", unsafe_allow_html=True)

# 🔚 Footer
st.markdown("---")
st.markdown("<center>Built with ❤️ using Python and Streamlit</center>", unsafe_allow_html=True)
