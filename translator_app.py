import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import Runnable

# ---- Set your Google Gemini API key ----
# Either set in your environment OR directly assign here (not recommended for production)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI_API_KEY_HERE"

# ---- Configure the Gemini model via LangChain ----
try:
    llm = ChatGoogleGenerativeAI(
        google_api_key="AIzaSyBTPDAVY2fKwg5zvipyIDkzqwybsoMO5qA",
        model="gemini-2.0-flash",
        temperature=0.3
    )
except Exception as e:
    st.error(f"Error initializing Gemini model: {e}")
    st.stop()

# ---- Define the translation prompt ----
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI that translates English to French."),
    ("human", "Translate the following sentence to French:\n\n{sentence}")
])

# ---- Create the chain ----
chain: Runnable = prompt | llm

# ---- Build the Streamlit UI ----
st.set_page_config(page_title="English to French Translator")
st.title("🌍 English to French Translator")

sentence = st.text_input("Enter an English sentence:")

if st.button("Translate"):
    if not sentence.strip():
        st.warning("Please enter a valid English sentence.")
    else:
        try:
            # Run the chain
            result = chain.invoke({"sentence": sentence})
            
            # Extract the text response
            translation = result.content if hasattr(result, "content") else str(result)
            
            st.success("✅ Translation complete!")
            st.write(f"**French:** {translation}")
        
        except Exception as e:
            st.error(f"⚠️ An error occurred during translation: {e}")
