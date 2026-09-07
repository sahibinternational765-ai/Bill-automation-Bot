import streamlit as st
import pdfplumber
import requests
import pandas as pd

# Set page layout
st.set_page_config(page_title="Bill Processor Bot", layout="centered")
st.title("📄 Bill Processor & WhatsApp Notifier")

# User inputs for credentials
whatsapp_number = st.text_input("WhatsApp Number (with country code):", "+911234567890")
callmebot_token = st.text_input("CallMeBot Token:", type="password")

def extract_data_from_pdf(pdf_file):
    """Extracts text and simple table data from an uploaded PDF bill."""
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    return extracted_text

def send_whatsapp_message(phone, token, message):
    """Sends notification via CallMeBot API."""
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={requests.utils.quote(message)}&apikey={token}"
    response = requests.get(url)
    return response.status_code == 200

# File uploader
uploaded_file = st.file_uploader("Upload your Bill (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    if st.button("Process Bill & Send Notification"):
        if not callmebot_token or not whatsapp_number:
            st.error("Please provide both WhatsApp Number and CallMeBot Token.")
        else:
            with st.spinner("Extracting bill data..."):
                bill_details = extract_data_from_pdf(uploaded_file)
            
            st.subheader("Extracted Bill Details")
            st.text_area("Bill Content", bill_details, height=200)
            
            # Send alert
            summary_msg = f"🔔 *New Bill Processed*\n\nFile Name: {uploaded_file.name}\n\nSummary:\n{bill_details[:200]}..."
            with st.spinner("Sending WhatsApp notification..."):
                success = send_whatsapp_message(whatsapp_number, callmebot_token, summary_msg)
            
            if success:
                st.success("WhatsApp notification sent successfully!")
            else:
                st.error("Failed to send WhatsApp message. Check credentials.")
