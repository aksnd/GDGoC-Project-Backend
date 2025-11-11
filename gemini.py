import os
import google.generativeai as genai
from google.generativeai import types

GREEN = '\033[32m'
RESET = '\033[0m'

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

image_path = 'files/images/test.png'
prompt = 'What does beta mean in this image?'

def main():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except ValueError:
        print("Error: GEMINI_API_KEY cannot be found.")
        exit()

    model = genai.GenerativeModel('gemini-2.5-flash')

    image_path = input("Enter the image path: ")
    prompt = input("Enter the prompt: ")

    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        exit()

    image_part = {
        'mime_type': 'image/png',
        'data': image_bytes
    }

    response = model.generate_content(
        contents=[image_part, prompt]
    )

    print()
    print(f"{GREEN}{response.text}{RESET}")

if __name__ == "__main__":
    main()


