import streamlit as st
import requests

# Title for the app
st.title('POC - Skistar Boende AI')

# Text input
user_input = st.text_input("Beskriv vilket boende du är ute efter:")

# Button to send the text to the API
if st.button('Skicka'):
    if user_input:
        # Prepare the API request
        url = "https://api.retool.com/v1/workflows/06a7e91c-605a-4565-9e8c-863a20318f98/startTrigger"
        headers = {
            "Content-Type": "application/json",
            "X-Workflow-Api-Key": "retool_wk_a74f115700d0450b90a9e8f21b74c0d5"  
        }
        payload = {
            "body": user_input
        }

        # Send the request to the API
        response = requests.post(url, json=payload, headers=headers)
        
        # Send the request to the API
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Assuming the API returns the text in the JSON response under 'data'
            result = response.json().get('data', "No data returned")
            st.write("Response from API:", result)
        else:
            st.error(f"Failed to send data. Status code: {response.status_code}")
    else:
        st.error("Please enter some text before sending.")





