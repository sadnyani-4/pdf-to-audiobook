import fitz  # PyMuPDF
import asyncio
import edge_tts

# 1. Extract text from PDF
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

# 2. Clean text (remove common PDF artifacts)
def clean_text(text):
    # Basic cleaning: remove extra newlines and spaces
    text = text.replace('\n', ' ').replace('\r', ' ')
    return " ".join(text.split())

# 3. Convert to Audio
async def text_to_audio(text, output_file):
    # You can change the voice. Run `edge-tts --list-voices` for more.
    voice = "en-US-GuyNeural" 
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

async def main():
    input_pdf = "novel.pdf"     # Put your file name here
    output_mp3 = "audiobook.mp3"
    
    print("📖 Extracting text...")
    raw_text = extract_text(input_pdf)
    
    print("🧹 Cleaning text...")
    final_text = clean_text(raw_text)
    
    # Optional: Truncate for testing (Edge-TTS has a limit on very long strings)
    # final_text = final_text[:5000] 

    print(f"🎙️ Generating audio: {output_mp3}...")
    await text_to_audio(final_text, output_mp3)
    print("✅ Done!")

if __name__ == "__main__":
    asyncio.run(main())