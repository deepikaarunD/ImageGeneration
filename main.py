import openai
import urllib.request
from PIL import Image
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("openai_api_key")

# Set the OpenAI API key
openai.api_key = openai_api_key

# Function to generate image
def generate_image(image_description):
    try:
        if not image_description.strip():
            st.warning("Please provide a valid image description.")
            return None

        # Generate image using OpenAI API
        img_response = openai.Image.create(
            prompt=image_description,
            n=1,
            size="512x512"
        )

        # Retrieve image URL from API response
        img_url = img_response['data'][0]['url']

        # Download image
        urllib.request.urlretrieve(img_url, 'img.png')

        # Open and return the image
        img = Image.open("img.png")
        return img

    except openai.error.InvalidRequestError as e:
        st.error(f"OpenAI API Error: {e.message}")
    except urllib.error.URLError as e:
        st.error(f"URL Error: {e.reason}")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

# Streamlit app
st.title('dall.E - Image Generation - OpenAI')

# Input field for image description
img_description = st.text_input('Image Description')

# Button to generate image
if st.button('Generate Image'):
    st.info("Generating image...")
    generated_img = generate_image(img_description)
    if generated_img:
        # Display generated image
        st.image(generated_img, caption='Generated Image', use_column_width=True)
        # Delete the downloaded image
        os.remove('img.png')
