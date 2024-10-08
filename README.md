# Image-Processing-API-with-Flask
# Image Processing API

This project provides an API for processing images to extract sensitive information such as Aadhaar numbers, PAN card numbers, and bank account numbers using OpenAI's GPT-4 Vision model.

## Features

- Extract text from images using OpenAI's GPT-4 Vision model
- Identify and extract Aadhaar numbers, PAN card numbers, and bank account numbers from the extracted text
- RESTful API endpoint for easy integration

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-processing-api.git
   cd image-processing-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. The API will be available at `http://localhost:5000`.

3. To process an image, send a POST request to the `/upload` endpoint with the image file:
   ```
   curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:5000/upload
   ```

   Replace `/path/to/your/image.j
