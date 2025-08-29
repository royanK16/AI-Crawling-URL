import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Access the API key from Streamlit secrets
try:
    api_key = st.secrets["gemini_api_key"]
except KeyError:
    st.error("Gemini API Key not found. Please set it in your Streamlit secrets.")
    st.stop()

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the Gemini model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

def parse_with_gemini(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    parsed_result = []
    
    for i, chunk in enumerate(dom_chunks, start= 1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_result.append(response.content)
        
    return ".\n".join(parsed_result)

if st.button("Parse with Gemini"):
    dom_chunk = ["<p>Some text to parse</p>", "<p>More text to parse</p>"]
    parsed_content = parse_with_gemini(dom_chunk, "Extract all text from p tags")
    st.write(parsed_content)
