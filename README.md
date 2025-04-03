# AI Chatbot with Image Processing and Voice Integration

## Overview
This project is an AI-powered chatbot integrated with Google's Gemini API for text-based and voice-based interactions. It also includes an image processing feature using the Python Imaging Library (PIL) and OCR capabilities with Tesseract.

## Features
- **Text-based Chat**: Users can type their queries, and the chatbot responds using the Gemini API.
- **Voice Chat**: Users can interact with the chatbot using voice input.
- **Text-to-Speech**: The chatbot can read out responses using pyttsx3.
- **Image Processing**: Users can apply filters, resize, crop, or add watermarks to images.
- **OCR (Optical Character Recognition)**: Extracts text from images using Tesseract.

## Technologies Used
- Python
- Google Gemini API (via `google.generativeai`)
- Speech Recognition (`speech_recognition`)
- Text-to-Speech (`pyttsx3`)
- GUI (`tkinter`)
- Image Processing (`Pillow` / `PIL`)
- OCR (`pytesseract`)
- Threading (`threading`)

## Installation
### Prerequisites
Ensure you have Python installed (preferably 3.7+). Install the required dependencies using:

```sh
pip install google-generativeai speechrecognition pyttsx3 pillow pytesseract
```

### Setting up Google Gemini API
Replace `api_key` in the script with your Google Gemini API key:
```python
 genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

### Installing Tesseract OCR
#### Windows:
1. Download and install Tesseract from: [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
2. Add the installation path to system environment variables.

#### Linux/macOS:
```sh
sudo apt install tesseract-ocr
```

## Usage
### Running the Chatbot
Run the script:
```sh
python chatbot.py
```

### Chatting with Gemini API
- Type a message and press **Send**.
- Speak using the **Voice Chat** button.
- To stop text-to-speech, press **Stop Speaking**.
- Press **Start Speaking** to repeat the last response.
- Type "bye" to exit the chat.

### Image Processing
1. Click **Browse Image** and select an image file.
2. Choose an action:
   - Apply Filters
   - Resize
   - Crop
   - Add Watermark
3. The extracted text (if any) is displayed in the chat history.

## Future Enhancements
- Improve voice recognition with custom wake words.
- Add real-time chatbot response suggestions.
- Enhance UI with better design and responsiveness.

## License
This project is open-source and available under the MIT License.

