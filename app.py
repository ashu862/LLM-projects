from dotenv import load_dotenv

load_dotenv() #load all the envronment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#funcion to load gemini pro Vision

model=genai.GenerativeModel('gemini-pro-vision-v1-5k')

def get_gemini_response(input,image,prompt):
  response=model.generate_content([input,image[0],prompt])
  return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts = [
        {
         "mime_type":  uploaded_file.type,
         "data": bytes_data
        }

        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploade")

#initialise our streamlit app

st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input=st.text_input("input Prompt: ",key="input")
uploaded_file=st.file_uploader("Upload your Invoice",type=["pdf","jpg","png"])
image=""

if uploaded_file is not None:
  image=Image.open(uploaded_file)
  st.image(image, caption="Uploaded Image", use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices.We will upload a image as invoices and 
you will have to answer any questions based in the uploaded invoice image
"""
# if submit butoon is clicked
if submit:
  image_data=input_image_details(uploaded_file)
  response=get_gemini_response(input_prompt,image_data,input)
  st.subheader("The Response is")
  st.write(response)

