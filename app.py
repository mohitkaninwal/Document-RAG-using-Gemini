import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from PIL import Image

load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')

# Configure the API key
genai.configure(api_key=api_key)

def get_gemini_response(input_text, image_data, prompt):
    try:
        # Create the model instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Combine the prompts
        full_prompt = f"{prompt}\n\nUser Query: {input_text}"
        
        # Generate content with image and text
        response = model.generate_content([full_prompt, image_data])
        
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the uploaded file to PIL Image and then to the format expected by Gemini
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError('No file uploaded')

st.set_page_config(page_title='Document Analyzer')

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
 st.header('Gemini Application')
uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png'])
input_text = st.text_input('What do you want to know about the Document: ', key='input')

image = ''
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image',width=200)

col1, col2, col3 = st.columns([2, 2, 1])
with col2:
    submit = st.button('Generate Answer')

input_prompt = """
You are an expert OCR performer, analyze the uploaded file and answer the query accurately and briefly according to the input image.
"""

if submit:
    if uploaded_file is not None:
        try:
            with st.spinner('Analyzing image and generating response...'):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_text, image_data, input_prompt)
            
            st.subheader('LLM Response:')
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please upload an image before submitting.")