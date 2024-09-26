import asyncio
import re
import os
from edge_tts import Communicate

# List of available voices
voices = {
    '1': 'en-US-AriaNeural',
    '2': 'en-US-GuyNeural',
    '3': 'ml-IN-MidhunNeural',
    '4': 'ml-IN-SobhanaNeural',
    '5': 'en-ZA-LeahNeural',
    '6': 'en-ZA-LukeNeural',
    '7': 'en-TZ-ElimuNeural',
    '8': 'en-TZ-ImaniNeural',
    '9': 'en-GB-LibbyNeural',
    '10': 'en-IN-NeerjaNeural',
    '11': 'en-IN-PrabhatNeural',
    '12': 'en-US-AnaNeural',
    '13': 'en-US-ChristopherNeural',
    '14': 'en-US-EricNeural',
    '15': 'en-US-JennyNeural',
    '16': 'en-US-MichelleNeural',
    '17': 'en-US-RogerNeural',
    '18': 'en-US-SteffanNeural',
}

# Function to preprocess text (removes unnecessary symbols and spaces)
def preprocess_text(text):
    # Replace multiple spaces or symbols with a single space
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special characters except punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove multiple spaces and trim
    return text

# Function to convert pitch selection to Hz
def convert_pitch_to_hz(pitch_choice):
    if pitch_choice == '1':  # -50%
        return '-50Hz'
    elif pitch_choice == '2':  # -25%
        return '-25Hz'
    elif pitch_choice == '3':  # Normal (0%)
        return '+0Hz'  # Ensure correct format
    elif pitch_choice == '4':  # +25%
        return '+25Hz'
    elif pitch_choice == '5':  # +50%
        return '+50Hz'
    return '+0Hz'  # Default to normal

# Function to convert the manually entered speaking rate to percentage
def convert_rate_to_percentage(rate_choice):
    try:
        rate = int(rate_choice)
        if -100 <= rate <= 100:  # Ensure the value is between -100 and 100
            return f"{'+' if rate >= 0 else ''}{rate}%"
    except ValueError:
        return '+0%'  # Default to normal if the input is invalid
    return '+0%'  # Default to normal

# Function to save text to speech
async def save_tts(text, selected_voice_code, rate, pitch):
    output_directory = "/storage/emulated/0/Download"  # Ensure this directory exists
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
    output_path = f"{output_directory}/{selected_voice_code}.mp3"  # Change path as needed

    communicate = Communicate(
        text,
        voice=selected_voice_code,
        rate=rate,
        pitch=pitch
    )
    try:
        await communicate.save(output_path)
        print(f"Audio saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

# Function to handle long text input
def get_long_text():
    print("\nEnter the text you want to convert to speech (type 'done' on a new line to finish):")
    input_text = []
    while True:
        line = input()
        if line.lower().strip() == 'done':
            break
        input_text.append(line)
    return preprocess_text(' '.join(input_text))

# Main function
async def main():
    print("Available Voices:")
    for key, value in voices.items():
        print(f"{key}: {value}")

    selected_voice_code = voices.get(input("Enter the number of the voice you want to use: "))

    if selected_voice_code:
        print("\nEnter speaking rate (-100 to 100):")
        rate_choice = input("Enter rate (e.g., -100, 0, 50, etc.): ")
        rate = convert_rate_to_percentage(rate_choice)

        print("\nChoose pitch:")
        print("1: -50%")
        print("2: -25%")
        print("3: Normal (0%)")
        print("4: +25%")
        print("5: +50%")
        pitch_choice = input("Select pitch option (1-5): ")
        pitch = convert_pitch_to_hz(pitch_choice)

        text = get_long_text()  # Get the long text or paragraph

        await save_tts(text, selected_voice_code, rate, pitch)

# Running the script
if __name__ == "__main__":
    asyncio.run(main())
