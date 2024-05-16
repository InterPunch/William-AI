import openai
import speech_recognition as sr
import threading
import pyttsx3
import tkinter as tk
import random
import datetime
import os


# Set your OpenAI API key here
openai.api_key = "INSRET APIKEY HERE!"

# Initialize pyttsx3 engine
engine = pyttsx3.init()




# Function to generate AI response
def generate_response(query):
    # Use your GPT-3.5 model to generate a response based on the input query
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are now Alfred! A AI butler created to serve your master"}, #you may instert your name after 'master'
            {"role": "user", "content": query}
        ],
	max_tokens=4096 # 4096 Is the max tokens for the model. If you are ok with shorter messages, lower it.
    )
    return response.choices[0].message['content']

def process_message(message):
    # Check if the message contains a reminder-setting command
    if "set a reminder for" in message:
        # Extract reminder text and time from the message
        parts = message.split(" at ")
        reminder_text = parts[0].replace("set a reminder for ", "").strip()
        reminder_time_text = parts[1].strip()

        # Parse the reminder time
        try:
            reminder_time = datetime.datetime.strptime(reminder_time_text, "%Y-%m-%d %H:%M:%S")
            set_reminder(reminder_text, reminder_time)
            return "Reminder set successfully."
        except ValueError:
            return "Failed to parse reminder time. Please provide the time in the format: YYYY-MM-DD HH:MM:SS"
    else:
        # If the message does not contain a recognized command, return a default response
        return generate_response(message)

# Function to recognize speech input
def speech_to_text():
    # Use SpeechRecognition library to recognize speech input from the user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        try:
            audio = r.listen(source, timeout=None)
            print("Recognition started")
            query = r.recognize_google(audio)
            print("You said:", query)
            entry.delete(0, tk.END)
            entry.insert(tk.END, query)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

# Function to handle button click event
def on_button_click():
    # Process user input
    user_input = entry.get()

    # Generate response
    response = process_message(user_input)
    #response = process_message(message)
    # Update response label
    response_label.config(text=response)
    
    #save response
    fileid = random.randint(1, 99999)
    filename = response[:18] + str(fileid) +".txt"
    with open(filename, 'w') as file:
         file.write(response)
    print("Response saved to file: " + filename)

    # Speak the response using pyttsx3
    engine.say(response)
    engine.runAndWait()
    

# Function to handle microphone button click event
def on_microphone_click():
    # Start speech recognition process in a separate thread
    threading.Thread(target=speech_to_text).start()

# Create GUI window
window = tk.Tk()
window.title("AI Assistant")

# Create face image
face_image = tk.PhotoImage(file="face.png")
face_label = tk.Label(window, image=face_image)
face_label.grid(row=0, column=0, columnspan=2)

# Create entry for user input
entry = tk.Entry(window, width=50)
entry.grid(row=1, column=0, padx=10, pady=10)

# Create microphone button
microphone_button = tk.Button(window, text="🎤", command=on_microphone_click)
microphone_button.grid(row=1, column=1, padx=10, pady=10)

# Create button to submit user input
button = tk.Button(window, text="Submit", command=on_button_click)
button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create label to display AI response
response_label = tk.Label(window, text="")
response_label.grid(row=3, column=0, columnspan=2)

# Start the Tkinter event loop
window.mainloop()
