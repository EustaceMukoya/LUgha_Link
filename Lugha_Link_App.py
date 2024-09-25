from flask import Flask, request, jsonify, render_template
import speech_recognition as SR
from googletrans import Translator
from googletrans import Translator, LANGUAGES
import pyttsx3

app = Flask(__name__)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def SpeechRecognition():
    SpeechRecognizer = SR.Recognizer()
    #speak("How can I help you")
    print("Listening")
    with SR.Microphone() as mic:
        try:
            SpeechRecognizer.adjust_for_ambient_noise(mic, duration=0.2)
            Text = SpeechRecognizer.recognize_google(SpeechRecognizer.listen(mic), language="en-US")
            Text = str(Text).lower()
            print(Text)
            return Text
        except SR.exceptions.UnknownValueError:
            return "Sorry, I did not understand."
        except Exception as e:
            print(f"An error eccurred: {e}")
            return"Sorry, an error occurred"
            
@app.route('/voice-input', methods=['POST'])
def voice_input():
    try:
        recognized_text = SpeechRecognition()
        return jsonify({'recognizedText': recognized_text})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500  # Return error response


def translate_to_swahili(text):
    try:
        if not text:
            raise ValueError("Empty source text")

        translator = Translator()

        # Check if the source language is set to English
        if translator.detect(text).lang != 'en':
            print(f"Source text language is not English: {translator.detect(text).lang}")
            return "Please provide an English text to translate."

        translation = translator.translate(text, dest='sw')
        print("Translation result:", translation)

        if translation.text:
            translated_text = translation.text
            print("Translated text:", translated_text)
            return translated_text
        else:
            raise ValueError("Translation result is empty")

    except ValueError as e:
        print(f"Value Error: {e}")
        return str(e)

    except Exception as e:
        print("Translation Error:", e)
        return "Translation failed. Please try again later."

@app.route('/')
def index():
    return render_template('User Interface.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        print("Received data:", data)
        source_text = data['sourceText']
        translated_text = translate_to_swahili(source_text)

        if translated_text.startswith("Please provide") or translated_text.startswith("Translation failed"):
            return jsonify({'error': translated_text}), 400
        else:
            
            return jsonify({'translatedText': translated_text})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/speak', methods=['POST'])
def speak_text():
    try:
        data = request.get_json()
        text = data['text']
        speak(text)
        return jsonify({'message': 'Text spoken successfully'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)