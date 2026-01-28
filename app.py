import streamlit as st
import fitz 
import asyncio
import edge_tts
import os
import io

st.set_page_config(page_title="Novel Reader Pro", page_icon="📖")

st.title("📖 Novel to Audiobook Converter")
st.info("Tip: Large novels are processed in chunks to ensure high quality.")

uploaded_file = st.file_uploader("Upload your Novel (PDF)", type="pdf")

async def convert_chunks(text_chunks):
    combined_audio = b""
    progress_bar = st.progress(0)
    
    for i, chunk in enumerate(text_chunks):
        communicate = edge_tts.Communicate(chunk, "en-US-GuyNeural")
        # Collect audio data in memory
        async for chunk_data in communicate.stream():
            if chunk_data["type"] == "audio":
                combined_audio += chunk_data["data"]
        
        # Update progress
        progress_bar.progress((i + 1) / len(text_chunks))
    
    return combined_audio

if uploaded_file:
    if st.button("Start Conversion"):
        with st.spinner("Extracting and cleaning text..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            full_text = " ".join([page.get_text() for page in doc])
            clean_text = " ".join(full_text.split())

            # Split text into chunks of 3000 characters (approx 500 words)
            # This prevents the TTS engine from timing out
            chunks = [clean_text[i:i+3000] for i in range(0, len(clean_text), 3000)]
            
            st.write(f"Processing {len(chunks)} chapters/chunks...")
            
            # Run the conversion
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_data = loop.run_until_complete(convert_chunks(chunks))
            
            st.success("✨ Your audiobook is ready!")
            st.audio(audio_data, format="audio/mp3")
            
            st.download_button(
                label="Download Full Audiobook",
                data=audio_data,
                file_name="my_audiobook.mp3",
                mime="audio/mp3"
            )