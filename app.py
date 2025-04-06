import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image
from textblob import TextBlob

st.set_page_config(page_title="Handwriting OCR with Layout & Spell Check", layout="centered")

st.title("📝 Handwriting to Text (Layout Preserved + Spelling Corrected)")

uploaded_file = st.file_uploader("Upload handwritten image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="📷 Original Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(img_np)

        height, width, _ = img_np.shape
        canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

        corrected_text = []
        raw_text = []

        for (bbox, text, prob) in results:
            (top_left, _, _, _) = bbox
            top_left = tuple(map(int, top_left))

            corrected = str(TextBlob(text).correct())
            corrected_text.append(corrected)
            raw_text.append(text)

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            cv2.putText(canvas, corrected, top_left, font, font_scale, (0, 0, 0), thickness)

        st.image(canvas, caption="🖋️ Corrected Text on Layout", use_column_width=True)

        st.subheader("🧾 Download Options:")
        st.download_button("📥 Raw Extracted Text", "\n".join(raw_text), file_name="raw_text.txt")
        st.download_button("📥 Corrected Text", "\n".join(corrected_text), file_name="corrected_text.txt")


