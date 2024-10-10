import streamlit as st
import streamlit.components.v1 as components

# Load the HTML file
try:
    with open("static/metamask_connect.html", "r") as f:
        html_content = f.read()
    
    # Display the HTML content using components.html
    components.html(html_content, height=600, scrolling=True)

except FileNotFoundError:
    st.error("Could not find the HTML file. Make sure it's in the correct location.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
