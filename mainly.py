import streamlit as st
import fitz  # PyMuPDF
import openai

st.set_page_config(page_title="Algorithm Extractor", layout="centered")

st.title("📘 AI Algorithm Info Extractor")
st.write("Upload a CS paper (PDF) and get key algorithm info automatically!")

# 🔑 Add your API key (or set it as an environment variable for safety)
openai.api_key = st.secrets.get("openai_api_key", "")

# Upload section
uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")

if uploaded_file is not None:
    st.info("⏳ Extracting text from your PDF...")
    
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    st.success("✅ Text extracted. Sending to GPT...")

    prompt = f"""
Extract the following information from the research paper text below:

- Title
- Authors
- Algorithm name (if any)
- Problem it solves
- Time complexity
- Space complexity
- Any pseudocode or algorithm steps

Output in this JSON format:
{{
  "title": "...",
  "authors": ["..."],
  "algorithm_name": "...",
  "problem_solved": "...",
  "time_complexity": "...",
  "space_complexity": "...",
  "pseudocode": "..."
}}

Here is the research paper text:
{full_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts algorithm-related information from research papers."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response['choices'][0]['message']['content']
    
    st.success("✅ Here's the extracted algorithm info:")
    st.code(result, language='json')
