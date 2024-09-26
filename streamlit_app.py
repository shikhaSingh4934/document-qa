import streamlit as st
import openai 


first_page = st.Page("lab1.py",title="First page")
second_page = st.Page("lab2.py",title="second page")
Third_page = st.Page("lab3A.py",title="Third page")
Fourth_page = st.Page("lab4.py",title="Fourth page")

pg = st.navigation([first_page,second_page,Third_page,Fourth_page])
st.set_page_config(page_title="test")
pg.run()
