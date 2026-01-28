import streamlit as st
import fitz 
import asyncio
import edge_tts
import os

st.set_page_config(page_title="Novel to Audiobook", page_icon="🎧")

st.title("🎧 PDF to Audiobook Converter")
st.write("Upload a novel and let AI read it to you.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save temp file
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Convert to Audiobook"):
        with st.spinner("Processing... This may take a minute for long novels."):
            # 1. Extract
            doc = fitz.open("temp.pdf")
            text = "".join([page.get_text() for page in doc])
            
            # 2. Clean (Simple version)
            clean_text = " ".join(text.split())
            
            # 3. Convert (Limit to first 50,000 chars for the web demo)
            async def make_audio():
                communicate = edge_tts.Communicate(clean_text[:50000], "en-US-GuyNeural")
                await communicate.save("output.mp3")

            asyncio.run(make_audio())
            
            st.success("Conversion Complete!")
            st.audio("output.mp3")
            
            with open("output.mp3", "rb") as f:
                st.download_button("Download MP3", f, file_name="audiobook.mp3")