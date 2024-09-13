import streamlit as st
import openai


first_page = st.Page("lab1.py",title="first page")
second_page = st.Page("lab2.py",title="second page")
second_page = st.Page("lab.py",title="Third page")

pg = st.navigation([first_page,second_page])
st.set_page_config(page_title="test")
pg.run()
