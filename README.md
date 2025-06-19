Document-Splitting-Toolkit
https://j6wysqrdyxpbn5co8wyuyz.streamlit.app/
A versatile Streamlit web application designed to automate the splitting of consolidated documents like PDFs, Excel spreadsheets, and Word files into multiple, individual files. 

💼 Document Splitting Toolkit
A versatile Streamlit web application designed to automate the splitting of consolidated documents like PDFs, Excel spreadsheets, and Word files into multiple, individual files.

This toolkit provides a clean, user-friendly interface for finance professionals, administrators, and anyone who needs to quickly de-consolidate large documents without manual effort.

🌟 Key Features
Multi-Document Support: Provides specialized tools for different file types.
📄 PDF Splitter: Splits a single PDF into multiple files based on a recurring header text (e.g., Account : ...). Supports plain text and Regular Expressions for advanced matching.
📊 Excel Splitter: Splits a single Excel sheet into multiple .xlsx files based on the unique values in a user-specified column (e.g., split by 'Client Name').
✍️ Word Splitter: Splits a .docx document into multiple files every time it encounters a specific keyword or phrase (e.g., "Client Statement").
🚀 User-Friendly Interface: A clean, modern UI built with Streamlit, with clear instructions and feedback.
📦 Zipped Output: Bundles all generated files into a single .zip archive for convenient, one-click downloading.
📸 Screenshots
Main Welcome Page:

PDF Splitter in Action:

(How to add screenshots: Take a screenshot of your app, upload it to a new issue in your GitHub repository, and then copy the image link it generates.)

🛠️ Technology Stack
Backend & Frontend: Python, Streamlit
PDF Manipulation: PyPDF2
Excel Manipulation: Pandas, Openpyxl
Word Manipulation: python-docx
🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Python 3.8+
pip (Python's package installer)
Installation
Clone the repository:

git clone https://github.com/[your-github-username]/doc-splitter.git
cd doc-splitter
(Replace [your-github-username] with your actual GitHub username)

Create and activate a virtual environment (Recommended): This keeps your project's dependencies isolated from your system's Python.

# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install the required libraries: The requirements.txt file contains all the necessary packages.

pip install -r requirements.txt
Run the Streamlit application:

streamlit run app.py
Your default web browser should automatically open with the application running at http://localhost:8501.

📂 Project Structure
The project is organized as a multi-page Streamlit application:

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgements
The Streamlit team for creating an amazing framework for data apps.
The developers of the open-source libraries PyPDF2, Pandas, and python-docx that power the core functionality of this toolkit.# prishitttttttt
