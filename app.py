import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Handwriting to Layout-preserved Text", layout="centered")

st.title("📝 Handwritten Image to Text with Original Layout")

uploaded_file = st.file_uploader("Upload your handwritten image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Original Handwritten Image", use_column_width=True)

    with st.spinner("Reading text..."):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(img_np)

        # Draw on blank white image
        height, width, _ = img_np.shape
        canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

        for (bbox, text, prob) in results:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            cv2.putText(canvas, text, top_left, font, font_scale, (0, 0, 0), thickness)

        st.image(canvas, caption="🖋️ Detected Text (Same Layout)", use_column_width=True)

        # Extract raw text for download
        extracted_text = "\n".join([text for (_, text, _) in results])
        st.download_button("📥 Download Extracted Text", extracted_text, file_name="output.txt")


