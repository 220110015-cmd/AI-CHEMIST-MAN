from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
def get_gemini_response(input,image,prompt):
  model = genai.GenerativeModel('gemini-2.0-flash-001')
  response = model.generate_content([input,image[0],prompt])
  return response.text
def input_image_setup(uploaded_file):
  #check if the file is uploaded or not
  if uploaded_file is not None :
    #Read the file into bytes
    bytes_data = uploaded_file.getvalue()
    image_parts = [
      {
        "mime_type" : uploaded_file.type,#get the mime type of uploaded file
        "data" : bytes_data
      }
    ]
    return image_parts
  else : 
    raise FileNotFoundError("No File is Uploaded") 
##initialize our streamlit app  
input_prompt = """ 
you are an expert pharamaceutical/chemist where you need to see the tablets from
             the input image and ,  also provide the details of every drug / tablets items with  below format

             1.Examine the image carefully and identify the tablets depicted.
             2.Describe the uses and functionalities of each tablet shown in the image.
             3.Provide information on the intended purposes,features and typical applications of the tablets.
             4.If possible , include any notable specifications or distinguishing characteristics of each tablet.
             5.Ensure clarity and conciseness in your descriptions, focusing on key details and distinguishing facts
            ----
"""
##initialize our streamlit app
st.set_page_config(page_title="AI CHEMIST APP")
st.header("AI CHEMIST APP")
input = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Upload an Image....", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Uploaded Image", width="stretch")
submit_button = st.button("Tell Me")
if submit_button:
  image_data = input_image_setup(uploaded_file)
  response = get_gemini_response(input_prompt,image_data,input)
  st.subheader("The Response is")
  st.write(response)
