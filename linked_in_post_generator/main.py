""" 
    Module: main.py.py
    
    Author: Nashith vp
    
    Description:
    
    Created On: 15-02-2026
"""
import streamlit as st
from few_shot import FewShotPosts
from post_creator import PostGenerator


def main():
    st.title("Linked in post generator")

    col1, col2, col3 = st.columns(3)
    few_shot_post = FewShotPosts()

    with col1:
        selected_tag = st.selectbox("Title", options=few_shot_post.get_unique_tags())

    with col2:
        selected_length = st.selectbox("Content Length", options=["Short", "Medium", "Long"])

    with col3:
        selected_language = st.selectbox("Language", options=["English", "Hinglish"])

    if st.button("Create Post"):
        post_generator = PostGenerator(selected_length, selected_language, selected_tag)
        st.write(post_generator.generate_post())


if __name__ == "__main__":
    main()

    # Run command: streamlit run main.py
