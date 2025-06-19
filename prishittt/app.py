import streamlit as st

st.set_page_config(
    page_title="Document Splitting Toolkit",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Welcome to the Document Splitting Toolkit")

st.markdown("""
### A suite of tools to automate the splitting of your consolidated documents.

This application provides specialized tools to handle different file types. Please select a tool from the sidebar to begin.
""")

with st.container(border=True):
    st.header("Available Tools:")
    st.markdown("""
        - **📄 PDF Splitter:** Splits a single PDF into multiple files based on a recurring header text (e.g., `Account : ...`).
        - **📊 Excel Splitter:** Splits a single Excel sheet into multiple `.xlsx` files based on the unique values in a specified column.
        - **✍️ Word Splitter:** Splits a `.docx` document into multiple files based on a keyword or phrase found in the text.
    """)

st.info("👈 **Select a tool from the sidebar to get started!**")