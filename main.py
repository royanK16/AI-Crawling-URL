import streamlit as st
from scrape import scrape_website, split_dom_content, extract_body_content, clean_body_content
from parse import parse_with_gemini
import pandas as pd
import os

st.title("AI Web Scraper")
url = st.text_input("Enter the URL to scrape:")

def export_to_csv(data, filename="data.csv"):
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, list):
        # Handle cases where the list contains non-dict items
        if all(isinstance(item, dict) for item in data):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([{"result": str(data)}])
    else:
        df = pd.DataFrame([{"result": str(data)}])
    
    df.to_csv(filename, index=False)
    return filename

if st.button("Scrape Site"):
    if url:
        st.info("Scraping from: " + url)      
        try:
            result = scrape_website(url)
            if result:
                st.success("Scraping complete!")
                body_content = extract_body_content(result)
                cleaned_content = clean_body_content(body_content)
                split_content = split_dom_content(cleaned_content)
            
                st.session_state.dom_content = cleaned_content
                st.session_state.parse_result = None  # Reset parse result
            
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            else: 
                st.error("Scraping failed. No content was returned. Please check the URL.")
                
        except Exception as e:
            st.error(f"An error occurred during scraping: {e}")
    else:
        st.warning("Please enter a URL to scrape.")

if "dom_content" in st.session_state and st.session_state.dom_content:
    parse_description = st.text_area("Describe what you want to parse from the DOM content:", key="parse_description")
    
    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Waiting for AI to parse..."):
                try:
                    dom_chunk = split_dom_content(st.session_state.dom_content)
                    result = parse_with_gemini(dom_chunk, parse_description)
                    st.session_state.parse_result = result
                    st.success("Parsing complete!")
                except Exception as e:
                    st.error(f"An error occurred during parsing: {e}")
        else:
            st.warning("Please provide a description for parsing.")
            
    if "parse_result" in st.session_state and st.session_state.parse_result:
        st.write("### Parsed Result")
        st.write(st.session_state.parse_result)

        # Create the CSV file once the parsing is done and store its path in session_state
        if "csv_file_path" not in st.session_state:
            csv_file_path = export_to_csv(st.session_state.parse_result)
            st.session_state.csv_file_path = csv_file_path
        
        # Display the download button
        with open(st.session_state.csv_file_path, "rb") as f:
            st.download_button(
                label="Download Parsed Data as CSV", 
                data=f, 
                file_name="data.csv",
                mime="text/csv"
            )


