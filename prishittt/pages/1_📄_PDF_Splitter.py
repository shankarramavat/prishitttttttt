import streamlit as st
import re
import zipfile
import tempfile
from PyPDF2 import PdfReader, PdfWriter
import io
import os

# --- THE DEFINITIVE HEURISTIC ENGINE V4 ---
# This engine is specifically designed to find "Account : [number] [code] - [name]" patterns.

def find_statement_start_pages(pdf_reader, log_container):
    """
    Scans the PDF to find the start pages of each new client statement based on a
    robust, hard-coded structural pattern. This is the core automatic engine.
    Returns: A list of dictionaries, each containing the page number and full header line.
    """
    log_container.write("🧠 Analyzing document for statement headers...")
    
    # This regex is the heart of the engine. It looks for the precise structure of your statements.
    # It's flexible with spacing and case-insensitive.
    # Pattern: "Account" -> optional space -> ":" -> any numbers/chars -> "-" -> any chars
    pattern = re.compile(
        r"Account\s*:\s*[\w\d\s-]+\s+-\s+.*", 
        re.IGNORECASE
    )
    
    detected_sections = []
    last_full_header = None

    for page_num, page in enumerate(pdf_reader.pages):
        try:
            text = page.extract_text() or ""
            # A header is almost always in the first 10-15 lines.
            for line in text.split('\n')[:15]:
                match = pattern.search(line)
                if match:
                    full_header = match.group(0).strip()
                    # This is the key to grouping: only add if the header is NEW.
                    if full_header != last_full_header:
                        log_container.write(f"  - Found new client on page {page_num + 1}: **{full_header}**")
                        detected_sections.append({
                            'page_num': page_num,
                            'header': full_header
                        })
                        last_full_header = full_header
                    # Once a header is found on a page, we can move to the next page.
                    break 
        except Exception:
            continue
            
    if not detected_sections:
        log_container.error("❌ **CRITICAL: No statement headers found.** The PDF does not seem to contain any lines matching the 'Account : [number] - [name]' structure. Please ensure the PDF is text-based and not an image.")
        return []

    log_container.success(f"✅ Analysis complete. Found **{len(detected_sections)}** individual client statements.")
    return detected_sections

def create_zip_from_sections(pdf_reader, sections, log_container):
    """
    Takes the verified list of sections and creates the final ZIP file with 100% accuracy.
    """
    num_pages = len(pdf_reader.pages)
    zip_buffer = io.BytesIO()
    files_created = 0
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, section in enumerate(sections):
                start_page_num = section['page_num']
                
                # The end page is one page before the next section starts, or the last page of the PDF.
                end_page_num = (sections[i + 1]['page_num'] - 1) if (i + 1 < len(sections)) else (num_pages - 1)
                
                # Use the full header for the filename, as requested.
                header_text = section['header']
                sanitized_name = re.sub(r'[\\/*?:"<>|]', "_", header_text)
                if len(sanitized_name) > 100:
                    sanitized_name = sanitized_name[:100]
                filename = f"{sanitized_name}.pdf"
                
                output_path = os.path.join(temp_dir, filename)
                pdf_writer = PdfWriter()
                
                log_container.write(f"  - Creating `{filename}` (Pages {start_page_num + 1} to {end_page_num + 1})")
                
                for page_num in range(start_page_num, end_page_num + 1):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                    
                with open(output_path, "wb") as out_pdf:
                    pdf_writer.write(out_pdf)
                
                zipf.write(output_path, arcname=filename)
                files_created += 1

    return zip_buffer.getvalue(), files_created


# --- UI: THE ULTIMATE "ONE-CLICK" EXPERIENCE ---
st.set_page_config(page_title="PDF Splitter", layout="wide")
st.title("📄 The Definitive One-Click PDF Splitter")
st.markdown("### For Intermediary Transaction Statements. No Configuration Needed.")

with st.container(border=True):
    st.header("Upload Your Consolidated PDF Statement")
    uploaded_file = st.file_uploader("The tool will automatically find all client statements and split the file.", type="pdf", label_visibility="collapsed")

if uploaded_file:
    # The entire process is now unified under one button for a seamless, automatic experience.
    if st.button("🚀 Process and Split PDF", type="primary", use_container_width=True):
        st.header("Processing Results")
        log_expander = st.expander("Show Detailed Processing Logs", expanded=True)
        
        with st.spinner("Analyzing document and splitting files..."):
            pdf_reader = PdfReader(uploaded_file)
            
            # The core automatic detection logic is called here.
            detected_sections = find_statement_start_pages(pdf_reader, log_expander)

            if detected_sections:
                # If sections are found, proceed immediately to create the ZIP.
                zip_data, files_created = create_zip_from_sections(pdf_reader, detected_sections, log_expander)

                if zip_data and files_created > 0:
                    st.success(f"**Success!** The PDF has been split into **{files_created}** individual client statements.")
                    st.balloons()
                    st.download_button(
                        label=f"⬇️ Download ZIP File ({files_created} documents)",
                        data=zip_data,
                        file_name=f"Split_{uploaded_file.name.replace('.pdf', '.zip')}",
                        mime="application/zip",
                        use_container_width=True
                    )
        # If the detection function returns nothing, the error is already displayed in the log expander.