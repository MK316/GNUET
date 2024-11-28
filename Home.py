import streamlit as st

# Your HTML formatted title
title_html = """
<h1 style='text-align: center;'>
    <span style='color: #71c6c6;'>G</span>
    <span style='color: gray;'>allery for </span>
    <span style='color: #71c6c6;'>N</span>
    <span style='color: gray;'>urturing </span>
    <span style='color: #71c6c6;'>U</span>
    <span style='color: gray;'>pcoming</span><br>
    <span style='color: #f9d34c;'>E</span>
    <span style='color: gray;'>nglish </span>
    <span style='color: #81d38c;'>T</span>
    <span style='color: gray;'>eachers</span>
</h1>
"""

# Initial content
st.markdown(title_html, unsafe_allow_html=True)
st.caption("Welcome to the Gallery for Nurturing Upcoming English Teachers (GNU-ET), where I've carefully selected a range of tools designed and developed specifically to support your journey toward the English teacher qualification exam. Each application in this gallery is crafted to enhance your personal study experience. I hope these resources prove invaluable as you progress towards your certification goals.")
st.write("In preparation (since Nov.28, 2024)")

# Image placed at the bottom of the page
st.image("https://github.com/MK316/GNUET/raw/main/images/bg3.png")
