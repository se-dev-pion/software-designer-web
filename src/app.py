import streamlit as st
import requests

st.title("API Test")
password = st.text_input("Please input API key", type="password")


def test_api(api_key: str):
    if st.button("Test"):
        if not api_key:
            st.error("Please input API key.")
            return
        with st.spinner("Sending request..."):
            try:
                response = requests.get(
                    "https://software-designer-api.vercel.app/",
                    headers={"Authorization": api_key},
                )
                if response.status_code == 200:
                    st.success("Request success")
                    st.text(response.text)
                else:
                    st.error(f"Request failure, status_code: {response.status_code}")

            except Exception as e:
                st.error(f"Request Error: {str(e)}")


test_api(password)
