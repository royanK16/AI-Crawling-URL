import streamlit as st 
from scrape import scrape_website, split_dom_content, extract_body_content, clean_body_content
from parse import parse_with_ollama
import pandas as pd

st.title("AI Web Scraper")
url = st.text_input("Enter the URL to scrape:")

if st.button("Scrape Site"):
    st.write("Scraping from:", url)
    result = scrape_website(url)
    st.write("Scraping complete!")
    
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    split_content = split_dom_content(cleaned_content)
    
    st.session_state.dom_content = cleaned_content
    
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)
        
def export_to_csv(data, filename="data.csv"):
    # If result is a list of dicts or dict, convert to DataFrame
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([{"result": str(data)}])
    df.to_csv(filename, index=False)
    return filename

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse from the DOM content: ")
    
    if st.button("Parse Content"):
        if parse_description:
            st.write("Waiting for response...")
            dom_chunk = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunk, parse_description)
            st.session_state.parse_result = result
            st.write(result)
            
    if "parse_result" in st.session_state and st.session_state.parse_result is not None:
        if st.button("Export Result to CSV file"):
            csv_file = export_to_csv(st.session_state.parse_result)
            st.write(f"Waiting for exporting to CSV file....")
            st.success(f"Result exported to {csv_file}")
            
            with open(csv_file, "rb") as f:
                st.download_button(label="Download CSV", 
                                    data= f.read(), 
                                    file_name=csv_file,
                                    mime="text/csv")
