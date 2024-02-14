from gtts import gTTS

def generate_audio(text, filename='output.mp3'):
    """
    Generate an audio file from the given text using gTTS.

    Parameters:
    - text: The text to convert to speech.
    - filename: The name of the output audio file (default is 'output.mp3').
    """
    tts = gTTS(text=text, lang='en')  # You can specify the language here
    tts.save(filename)
    print(f"Audio file '{filename}' generated successfully!")

if __name__ == "__main__":
    text = input("Enter the text you want to convert to speech: ")
    generate_audio(text)
