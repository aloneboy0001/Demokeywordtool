# Import necessary libraries
import streamlit as st
import bomber
import asyncio
import pandas as pd

# Function to run asyncio code
def run_asyncio_code(keyword, country):
    return asyncio.run(bomber.get_keyword_data(keyword, country))

# Function to display Keyword Data
def display_keyword_data(keyword_data):
    st.markdown("## Keyword Data")
    excluded_categories = [
        "Audience-Specific", "Problem-Solving", "Feature-Specific", 
        "Opinions/Reviews", "Cost-Related", "Trend-Based"
    ]
    for category, keywords in keyword_data.items():
        if category not in excluded_categories:
            st.markdown(f"### {category}")
            df = pd.DataFrame.from_dict(keywords, orient='index').transpose()
            st.dataframe(df)

# Streamlit UI layout setup
st.title("Keyword Bomber")
st.write("Enter the details below to fetch keyword data.")

input_keyword = st.text_input("Enter the keyword", "Marketing Automation")
input_country = st.text_input("Enter the country code", "US")

# Add margin above the button
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        # Add margin above the spinner
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        result = run_asyncio_code(input_keyword, input_country)
        if result.get('success'):
            display_keyword_data(result['result']['keyword_data'])
            # Promotional section
            st.markdown("### Want more keyword metrics with AI analysis?")
            st.markdown("Buy our **Premium Keyword Bomber Tool** for advanced features!")
            if st.button("Get the Premium"):
                # Redirect to Google website using the Streamlit function
                st.write('<script>window.open("https://www.google.com", "_blank");</script>', unsafe_allow_html=True)
        else:
            st.error("Failed to fetch data")  # Fixed the unterminated string error