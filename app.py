import streamlit as st
import boto3

# 1. Page Settings
st.set_page_config(page_title="HealthClaims AI", page_icon="🏥")
st.title("🏥 HealthClaims AI")
st.write("Scan your medical bill to get started.")

# 2. Sidebar for Keys
with st.sidebar:
    st.header("Settings")
    aws_key = st.text_input("AWS Access Key", type="password")
    aws_secret = st.text_input("AWS Secret Key", type="password")

# 3. Photo Upload
uploaded_file = st.file_uploader("Upload a photo of your bill", type=['png', 'jpg', 'jpeg'])

if uploaded_file and aws_key and aws_secret:
    client = boto3.client('textract', 
                          aws_access_key_id=aws_key, 
                          aws_secret_access_key=aws_secret, 
                          region_name='us-east-1')

    if st.button("Read Bill"):
        with st.spinner('Reading...'):
            try:
                # This block must be indented exactly 4 spaces
                response = client.analyze_document(
                    Document={'Bytes': uploaded_file.getvalue()},
                    FeatureTypes=['QUERIES'],
                    QueriesConfig={'Queries': [
                        {'Text': 'What is the total amount?', 'Alias': 'TOTAL'},
                        {'Text': 'What is the hospital name?', 'Alias': 'HOSPITAL'}
                    ]}
                )
                res = response['QueriesConfigCustomPages'][0]['Results']
                st.success(f"Total Amount: {res[0]['Text']}")
                st.write(f"Hospital: {res[1]['Text']}")
            except Exception as e:
                # The 'except' must line up perfectly with 'try'
                st.error(f"Error: {e}")
