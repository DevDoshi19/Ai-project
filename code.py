import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, simpledialog
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import pytesseract
import threading

# Configure Google Gemini API
genai.configure(api_key="Your_api_key")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

stop_speaking = False


def speak(text):
    global stop_speaking
    stop_speaking = False
    engine.say(text)
    engine.runAndWait()


def stop_speech():
    global stop_speaking
    stop_speaking = True
    engine.stop()


def chat_with_gemini(user_input):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(user_input)
    return response.text if response else "I'm not sure, please try again."


def text_chat():
    user_input = entry.get()
    if user_input.lower() == "bye":
        chat_history.insert(tk.END, "Chatbot: Goodbye! 👋\n")
        root.quit()
    elif user_input.lower() == "stop":
        stop_speech()
    else:
        response = chat_with_gemini(user_input)
        chat_history.insert(tk.END, f"You: {user_input}\n")
        chat_history.insert(tk.END, f"Chatbot: {response}\n")
        threading.Thread(target=speak, args=(response,)).start()
    entry.delete(0, tk.END)

def voice_chat():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_history.insert(tk.END, "Listening...\n")
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            chat_history.insert(tk.END, f"You (Voice): {user_input}\n")
            response = chat_with_gemini(user_input)
            chat_history.insert(tk.END, f"Chatbot: {response}\n")
            threading.Thread(target=speak, args=(response,)).start()
        except sr.UnknownValueError:
            chat_history.insert(tk.END, "Couldn't understand, please try again.\n")
        except sr.RequestError:
            chat_history.insert(tk.END, "Speech recognition service is unavailable.\n")


def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    image = Image.open(file_path)
    action = simpledialog.askinteger("Image Processing", "Choose an action: 1-Filter, 2-Resize, 3-Crop, 4-Watermark")

    if action == 1:
        filters = {
            1: ImageFilter.BLUR,
            2: ImageFilter.DETAIL,
            3: ImageFilter.SHARPEN,
            4: ImageFilter.SMOOTH_MORE,
            5: ImageFilter.EDGE_ENHANCE,
            6: ImageFilter.SMOOTH,
            7: ImageFilter.CONTOUR
        }
        filter_choice = simpledialog.askinteger("Choose Filter",
                                                "1-Blur, 2-Detail, 3-Sharpen, 4-Smooth More, 5-Edge Enhance, 6-Smooth, 7-Contour")
        if filter_choice in filters:
            image = image.filter(filters[filter_choice])
            image.show()

    elif action == 2:
        width = simpledialog.askinteger("Resize", "Enter new width:")
        height = simpledialog.askinteger("Resize", "Enter new height:")
        if width and height:
            image = image.resize((width, height))
            image.show()

    elif action == 3:
        left = simpledialog.askinteger("Crop", "Enter pixels to cut from left:")
        top = simpledialog.askinteger("Crop", "Enter pixels to cut from top:")
        right = simpledialog.askinteger("Crop", "Enter pixels to cut from right:")
        bottom = simpledialog.askinteger("Crop", "Enter pixels to cut from bottom:")
        if all(v is not None for v in [left, top, right, bottom]):
            image = image.crop((left, top, right, bottom))
            image.show()

    elif action == 4:
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        x = simpledialog.askinteger("Watermark", "Enter X coordinate:")
        y = simpledialog.askinteger("Watermark", "Enter Y coordinate:")
        text = simpledialog.askstring("Watermark", "Enter watermark text:")
        r = simpledialog.askinteger("Color", "Enter Red (0-255):")
        g = simpledialog.askinteger("Color", "Enter Green (0-255):")
        b = simpledialog.askinteger("Color", "Enter Blue (0-255):")
        if all(v is not None for v in [x, y, text, r, g, b]):
            draw.text((x, y), text, fill=(r, g, b), font=font)
            image.show()

    extracted_text = pytesseract.image_to_string(image)
    chat_history.insert(tk.END, f"Extracted Text: {extracted_text}\n")


def start_speech():
    last_response = chat_history.get("end-3c", "end-2c")
    if last_response:
        threading.Thread(target=speak, args=(last_response,)).start()


# Tkinter GUI Setup
root = tk.Tk()
root.title("AI Chatbot with Gemini API")
root.geometry("600x500")
root.configure(bg="#f4f4f4")

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Poppins", 12), height=15, width=70)
chat_history.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

entry = tk.Entry(root, font=("Poppins", 14))
entry.pack(padx=10, pady=5, fill=tk.X)

button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)

send_button = tk.Button(button_frame, text="Send", font=("Poppins", 12), command=text_chat)
send_button.grid(row=0, column=0, padx=5)

voice_button = tk.Button(button_frame, text="Voice Chat", font=("Poppins", 12),
                         command=lambda: threading.Thread(target=voice_chat).start())
voice_button.grid(row=0, column=1, padx=5)

stop_button = tk.Button(button_frame, text="Stop Speaking", font=("Poppins", 12), command=stop_speech)
stop_button.grid(row=0, column=2, padx=5)

start_button = tk.Button(button_frame, text="Start Speaking", font=("Poppins", 12), command=start_speech)
start_button.grid(row=0, column=3, padx=5)

image_button = tk.Button(button_frame, text="Browse Image", font=("Poppins", 12), command=browse_image)
image_button.grid(row=0, column=4, padx=5)

root.mainloop()
