import streamlit as st
import easyocr
from PIL import Image
import os

st.set_page_config(page_title="Handwritten Text Extractor", layout="wide", initial_sidebar_state="expanded")
st.title("📝 Handwritten Note to Text Converter")

uploaded_file = st.file_uploader("Upload your handwritten note image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Handwritten Note", use_column_width=True)

    with st.spinner("Extracting text... Please wait"):
        reader = easyocr.Reader(['en'])
        result = reader.readtext(uploaded_file)

        # Extract only the text part from result, filter None or empty values
        extracted_text = [text[1] for text in result if text[1]]

        # Join and display the formatted output
        if extracted_text:
            formatted_output = "\n".join(extracted_text)
            st.markdown(
                f"""
                <div style="text-align: right;">
                    <b>Date:</b> _____<br>
                    <b>Page No:</b> 1
                </div>

                <div style="padding-top: 20px;">
                    <pre style="background-color: #f5f5f5; padding: 15px; border-radius: 10px;">{formatted_output}</pre>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("No readable text found in the image.")

