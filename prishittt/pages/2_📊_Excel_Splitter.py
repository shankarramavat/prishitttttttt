import streamlit as st
import pandas as pd
import zipfile
import tempfile
import os
import io
import re

# --- Backend function is correct, no changes needed ---
def split_and_zip_excel(uploaded_file, column_name, log_container):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        log_container.info(f"✅ Excel file loaded successfully. Found {len(df)} rows.")
    except Exception as e:
        log_container.error(f"❌ Could not read Excel file. Details: {e}")
        return None, 0
    
    if column_name not in df.columns:
        log_container.error(f"❌ Column '{column_name}' not found in the Excel file.")
        log_container.info(f"Available columns are: {', '.join(df.columns)}")
        return None, 0

    unique_values = df[column_name].unique()
    log_container.success(f"✅ Found {len(unique_values)} unique values in column '{column_name}'.")
    files_created = 0
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        with tempfile.TemporaryDirectory() as temp_dir:
            for value in unique_values:
                df_subset = df[df[column_name] == value]
                sanitized_value = str(value).replace(" ", "_")
                sanitized_value = re.sub(r'[\\/*?:"<>|]', '', sanitized_value)
                filename = f"{sanitized_value}.xlsx"
                output_path = os.path.join(temp_dir, filename)
                df_subset.to_excel(output_path, index=False)
                zipf.write(output_path, arcname=filename)
                files_created += 1
                log_container.write(f"  - Created `{filename}` with {len(df_subset)} rows.")
    return zip_buffer.getvalue(), files_created

# --- UI LOGIC (CORRECTED) ---
st.set_page_config(page_title="Excel Splitter", layout="wide")
st.title("📊 Excel Sheet Splitter")

with st.container(border=True):
    st.header("1. Configure Split Settings")
    column_name = st.text_input("Enter the name of the column to split by (e.g., 'Client Name')")

with st.container(border=True):
    st.header("2. Upload Your Excel File")
    uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type="xlsx", label_visibility="collapsed")

if st.button("🚀 Process Excel File", type="primary", use_container_width=True):
    if uploaded_file is not None and column_name:
        st.header("3. Results")
        with st.spinner("Splitting Excel file..."):
            log_expander = st.expander("Show Processing Logs", expanded=True)
            zip_data, files_created = split_and_zip_excel(uploaded_file, column_name, log_expander)
            if zip_data:
                st.metric("Files Created", files_created)
                st.download_button(
                    label="⬇️ Download ZIP File",
                    data=zip_data,
                    file_name=f"Split_{uploaded_file.name.replace('.xlsx', '.zip')}",
                    mime="application/zip",
                    use_container_width=True
                )
    else:
        st.warning("⚠️ Please upload a file and enter a column name.")