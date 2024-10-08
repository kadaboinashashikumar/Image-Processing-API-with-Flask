from flask import Flask, request, jsonify
from openai import OpenAI
import base64
import json
import os
from dotenv import load_dotenv
import re

app = Flask(__name__)

def load_api_key():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return openai_api_key

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def create_openai_client(api_key):
    return OpenAI(api_key=api_key)

def send_image_to_openai(client, image_base64):
    response = client.chat.completions.create(
        model='gpt-4-vision-preview',
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Return text extracted from the image. Only return text, no other text or formatting."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                    }
                ],
            }
        ],
        max_tokens=500,
    )
    return response

def extract_identifiers(text):
    aadhaar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'
    pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'
    account_pattern = r'\b\d{9,18}\b'

    aadhaar_matches = re.findall(aadhaar_pattern, text)
    pan_matches = re.findall(pan_pattern, text)
    account_matches = re.findall(account_pattern, text)

    return {
        "aadhaar_numbers": list(set(aadhaar_matches)),
        "pan_numbers": list(set(pan_matches)),
        "account_numbers": list(set(account_matches))
    }

def process_response(response):
    text = response.choices[0].message.content.strip()
    identifiers = extract_identifiers(text)
    return identifiers

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        api_key = load_api_key()
        image_base64 = encode_image(file)
        client = create_openai_client(api_key)
        response = send_image_to_openai(client, image_base64)
        identifiers = process_response(response)
        
        result = {
            "message": "File processed successfully",
            "identifiers": identifiers
        }
        
        if not any(identifiers.values()):
            result["message"] = "No Aadhaar number / PAN card number / bank account number found"
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()