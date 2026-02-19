"""
Module: main.py

Author: Nashith VP

Description: Beautiful LinkedIn Post Generator Web App

Created On: 15-02-2026
"""

import streamlit as st
from few_shot import FewShotPosts
from post_creator import PostGenerator

# Configure page
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="wide"
)

def main():
    # Custom header
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        <div class="main-title">🚀 LinkedIn Post Generator</div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for settings
    few_shot_post = FewShotPosts()
    with st.sidebar:
        st.header("⚙️ Post Settings")
        selected_tag = st.selectbox("Title", options=few_shot_post.get_unique_tags())
        selected_length = st.radio("Content Length", ["Short", "Medium", "Long"])
        selected_language = st.radio("Language", ["English", "Hinglish"])

    # Main content area
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("✨ Create Post", use_container_width=True):
        post_generator = PostGenerator(selected_length, selected_language, selected_tag)
        st.success("Here’s your generated post:")
        st.write(post_generator.generate_post())

    # Footer
    st.markdown(
        """
        <hr>
        <div style='text-align: center; color: gray;'>
            Made with ❤️ by Nashith VP
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

# Run command: streamlit run main.py
