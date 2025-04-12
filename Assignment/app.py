# app.py
import streamlit as st  # Import Streamlit for building the web app
from joke_app import JokeFetcher  # Import the JokeFetcher class from your joke_app module

# Set basic page configuration for the Streamlit app
st.set_page_config(page_title="JokeSmith - Joke App", page_icon="😂", layout="centered")

# Add custom CSS styling for the main title and subtitle
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

# Display main title and subtitle on the main page using HTML
st.markdown('<div class="main-title">JokeSmith 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered joke forge — brew hilarious moments instantly!</div>', unsafe_allow_html=True)

# Sidebar configuration for user to customize joke preferences
with st.sidebar:
    st.header("🎛 Joke Settings")  # Sidebar title

    # Allow users to select categories of jokes
    category = st.multiselect(
        "Category", 
        ["Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"],
        default=["Programming"]
    )

    # Select type of joke: any, single-line, or two-part
    joke_type = st.selectbox("Type", ["Any", "single", "twopart"])

    # Choose how many jokes to fetch (1 to 10)
    amount = st.slider("Number of Jokes", 1, 10, 1)

    # Select language for the jokes
    lang = st.selectbox("Language", ["en", "de", "es", "fr", "cs", "pt"])

    # Choose content types to exclude (like NSFW or racist content)
    blacklist = st.multiselect("Blacklist Flags", ["nsfw", "religious", "political", "racist", "sexist"])

    # Optional string to filter jokes by keyword
    search_string = st.text_input("Search String")

    # Option to return API headers (for debugging/inspection)
    return_headers = st.checkbox("Return Headers (to see JSON)")

# Main button to trigger joke fetching
if st.button("Get Jokes"):
    # Create an instance of the JokeFetcher with user-selected options
    fetcher = JokeFetcher(
        category=category if category else None,
        blacklist=blacklist if blacklist else None,
        joke_type=joke_type,
        search_string=search_string if search_string else None,
        amount=amount,
        lang=lang,
        return_headers=return_headers
    )

    # Fetch jokes from the API
    result = fetcher.fetch_jokes()

    # If return_headers is checked, display headers separately
    if return_headers:
        jokes, headers = result
        st.subheader("📋 Headers Returned:")
        st.json(dict(headers))  # Display headers in JSON format
    else:
        jokes = fetcher.jokes  # Just get the jokes

    # Display fetched jokes
    st.subheader("🃏 Here are your jokes:")
    for i, joke in enumerate(jokes, 1):
        st.markdown(f"**Joke {i}:**\n> {joke}")

    # Option to download the jokes as TXT or PDF files
    with st.expander("💾 Save Jokes"):
        txt_file = fetcher.save_as_txt("jokes.txt")
        pdf_file = fetcher.save_as_pdf("jokes.pdf")

        # Provide download button for TXT file
        with open(txt_file, "rb") as f:
            st.download_button("📄 Download as TXT", data=f, file_name="jokes.txt")

        # Provide download button for PDF file
        with open(pdf_file, "rb") as f:
            st.download_button("📝 Download as PDF", data=f, file_name="jokes.pdf")
