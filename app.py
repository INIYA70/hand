import streamlit as st
from PIL import Image
from utils import extract_text

st.set_page_config(layout="wide")
st.markdown('<link rel="stylesheet" href="style.css">', unsafe_allow_html=True)

st.title("📝 Handwritten Notes to Typed Page")

uploaded_image = st.file_uploader("Upload your handwritten note", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Handwritten Note", use_column_width=True)

    with st.spinner("Extracting text..."):
        extracted_text = extract_text(image)

    # ---- Layout: Top right
    col1, col2 = st.columns([8, 2])
    with col2:
        st.markdown('<div class="top-right">Date: ____<br>Page No: 1</div>', unsafe_allow_html=True)

    # ---- Title
    st.markdown('<div class="title">Introduction</div>', unsafe_allow_html=True)

    # ---- Subtitle
    st.markdown('<div class="header">What is <span style="color:gold">machine learning</span>?</div>', unsafe_allow_html=True)

    # ---- Extracted Text
    formatted_output = "\n".join(extracted_text)
    st.write(formatted_output)
