import streamlit as st
import requests

st.set_page_config(page_title="AI Cyber Assistant")

st.title("🤖 AI Cyber Assistant")

HF_TOKEN = st.secrets["HF_TOKEN"]

user_input = st.text_input("💬 اسأل:")

if st.button("اسأل"):

    if user_input:
        API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

        headers = {
            "Authorization": f"Bearer {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}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": user_input
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code != 200:
                st.error(response.text)
            else:
                result = response.json()

                if isinstance(result, list):
                    st.success(result[0]["generated_text"])
                else:
                    st.success(result)

        except Exception as e:
            st.error(e)
