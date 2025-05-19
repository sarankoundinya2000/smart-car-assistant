## authenticate and authorize 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import speech_recognition as sr
from googlesearch import search
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from gtts import gTTS
import os
from playsound import playsound
from dotenv import load_dotenv
from groq import Groq
import os
from gtts import gTTS
import pygame
import smtplib
from datetime import datetime
import dateparser
import regex as re

car_inventory = [
    {"name": "BMW X5", "category": "SUV"},
    {"name": "BMW X3", "category": "SUV"},
    {"name": "BMW X7", "category": "SUV"},
    {"name": "BMW X6", "category": "SUV Coupe"},
    {"name": "BMW X4", "category": "SUV Coupe"},
    {"name": "BMW 3 Series", "category": "Sedan"},
    {"name": "BMW 5 Series", "category": "Sedan"},
    {"name": "BMW 7 Series", "category": "Sedan"},
    {"name": "BMW 2 Series", "category": "Coupe"},
    {"name": "BMW 4 Series", "category": "Coupe"},
    {"name": "BMW 8 Series", "category": "Coupe"},
    {"name": "BMW Z4", "category": "Roadster"},
    {"name": "BMW i3", "category": "Electric Hatchback"},
    {"name": "BMW i4", "category": "Electric Gran Coupe"},
    {"name": "BMW iX", "category": "Electric SUV"},
    {"name": "BMW i7", "category": "Electric Sedan"},
    {"name": "BMW M2", "category": "Sports Coupe"},
    {"name": "BMW M4", "category": "Sports Coupe"},
    {"name": "BMW M5", "category": "Sports Sedan"},
    {"name": "BMW M8", "category": "Sports Coupe"}
]
car_details = [f"{car['name']} ({car['category']})" for car in car_inventory]


SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

## checking availability 
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def check_availability(date, service):
    calendar_id = 'primary'
    start_of_day = datetime.combine(date, datetime.min.time()).isoformat() + 'Z'
    end_of_day = datetime.combine(date, datetime.max.time()).isoformat() + 'Z'
    
    events_result = service.events().list(calendarId=calendar_id, timeMin=start_of_day, timeMax=end_of_day,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    available_slots = []
    if not events:
        available_slots.append("Full day available")
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            available_slots.append((start, end))

   
    return available_slots

def book_calendar_event(name, phone, date, time, email, service):
    calendar_id = 'primary'
    event_start = datetime.combine(date, time)
    event_end = event_start + timedelta(hours=1)
    
    event = {
        'summary': 'Appointment with ' + name,
        'description': f'Phone: {phone}',
        'start': {
            'dateTime': event_start.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': event_end.isoformat(),
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': email},
        ],
    }
    
    event = service.events().insert(calendarId=calendar_id, body=event, sendUpdates='all').execute()
    print('Event created: %s' % (event.get('htmlLink')))
    return event


def is_phone_number(text):
    """Check if the text is a valid phone number."""
    return re.fullmatch(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text) is not None

def format_phone_number(text):
    """Format the phone number to a standard format."""
    digits = re.sub(r'\D', '', text)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    else:
        return text
        
def clean_time(time_str):
    # Use regex to extract the time part with am/pm, ignoring periods and other text
    match = re.search(r'(\d{1,2}:\d{2}\s*[ap]\.?[m]\.?)', time_str, flags=re.IGNORECASE)
    if match:
        cleaned_time_str = match.group(1).replace('.', '').strip()
        time_format = "%I:%M %p"
        time_obj = datetime.strptime(cleaned_time_str, time_format).time()
        return time_obj
    else:
        raise ValueError("Time format not recognized")
def book_appointment():
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    
    while True:
        speak_text("Provide your name. Could you please spell your name?")
        name = recognize_speech()
        if name:
            name = name.replace(" ", "")
            speak_text(f"Did I get that right? Your name is {name}.")
            confirm = recognize_speech()
            if confirm and "yes" in confirm.lower() or confirm and "that's correct" in cofirm.lower() or confirm and "thats correct" in confirm.lower() :
                break
            elif confirm is None:
                speak_text("I couldn't understand you. Could you please repeat it?")
            else:
                speak_text("Let's try again.")
        else:
            speak_text("I couldn't understand you. Could you please repeat it?")

    while True:
        speak_text("Provide your phone number.")
        phone = recognize_speech()
        if is_phone_number(phone):
            phone = format_phone_number(phone)
            speak_text(f"Is {phone} your correct phone number?")
            confirm = recognize_speech()
            if confirm and "yes" in confirm.lower() or confirm and "that's correct" in cofirm.lower() or confirm and "thats correct" in confirm.lower():
                break
            else:
                speak_text("Let's try again.")
        else:
            speak_text("I couldn't understand the phone number. Let's try again.")

    parsed_date = None
    
    while True:
        speak_text("Provide the date for the appointment.")
        date_text = recognize_speech()
        if date_text:
            parsed_date = dateparser.parse(date_text)
            if parsed_date:
                speak_text(f"Would you like to schedule the appointment on {parsed_date.strftime('%B %d %Y')}?")
                confirm = recognize_speech()
                if confirm and "yes" in confirm.lower():
                    break
                elif confirm is None:
                    speak_text("I couldn't understand you. Could you please repeat it?")
                else:
                    speak_text("Let's try again.")
            else:
                speak_text("I couldn't understand you. Could you please repeat it?")

    parsed_time = None
    while True:
        speak_text("Provide the time for the appointment.")
        time_text = recognize_speech()
        if time_text:
            parsed_time = clean_time(time_text)
            if parsed_time:
                speak_text(f"Is {parsed_time.strftime('%I:%M %p')} the time you want to book?")
                confirm = recognize_speech()
                if confirm and "yes" in confirm.lower():
                    break
                elif confirm is None:
                    speak_text("I couldn't understand you. Could you please repeat it?")
                else:
                    speak_text("Let's try again.")
            else:
                speak_text("I couldn't understand you. Could you please repeat it?")

    available_slots = check_availability(parsed_date, service)
    if available_slots:
        speak_text(f"Available slots on {parsed_date.strftime('%B %d, %Y')}: {', '.join(available_slots)}")
        while True:
            speak_text("Would you like to book this slot?")
            confirm = recognize_speech()
            if confirm and "yes" in confirm.lower():
                break
            elif confirm is None:
                speak_text("I couldn't understand you. Could you please repeat it?")
            else:
                speak_text("Let's try again.")
    else:
        speak_text("Sorry, no slots available. Please choose another date or time.")

    appointment_details = f"Details: \nName: {name}\nPhone: {phone}\nDate: {parsed_date.strftime('%B %d, %Y')}\nTime: {parsed_time.strftime('%I:%M %p')}"

    while True:
        speak_text("Would you like to receive the appointment details by email?")
        confirm_email = recognize_speech()

        if confirm_email and "yes" in confirm_email.lower():
            while True:
                speak_text("Please provide your email address.")
                email_address = recognize_speech()
                if email_address:
                    if "at" in email_address.lower() or "at the rate" in email_address.lower():
                        email_address = email_address.lower().replace("at the rate", "@").replace("at", "@")
                        email_address = email_address.lower().replace("dot", ".")
                        email_address = email_address.replace(" ", "")
                    if "@" in email_address and "." in email_address.split("@")[-1]:
                        speak_text(f"Is {email_address} your correct email address?")
                        confirm = recognize_speech()
                        if confirm and "yes" in confirm.lower():
                            send_email(email_address, "Appointment Booking", appointment_details)
                            book_calendar_event(name, phone, parsed_date, parsed_time, email_address, service)
                            speak_text("Your appointment is booked and details have been sent to your email, and an event has been created in your Google Calendar. Thanks for calling us, goodbye!")
                            break
                        elif confirm is None:
                            speak_text("I couldn't understand you. Could you please repeat it?")
                        else:
                            speak_text("Let's try again.")
                else:
                    speak_text("I couldn't understand you. Could you please repeat it?")
            break
        elif confirm_email is None:
            speak_text("I couldn't understand you. Could you please repeat it?")
        else:
            speak_text("Okay, the appointment is booked without email confirmation. Thanks for calling us. Goodbye.")
        email = "17671A1238@gmail.com"

        
load_dotenv('groqapi.env')

client = Groq(
    api_key=os.environ['GROQ_API_KEY'],
)

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    os.remove("response.mp3")


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        #speak_text("I'm listening.")
        #print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            #print("Could not understand audio")
            return None
        except sr.RequestError:
            #print("Could not request results; check your network connection")
            return None
        except Exception as e:
            print(f"An error occurred during speech recognition: {e}")
            return None

def generate_response(prompt):
    try:
        completion = client.chat.completions.create(model="llama3-70b-8192",
        messages=[
                {
                "role": "system", "content":     
                f"""You are Sandy, a helpful BMW car showroom assistant.
                You should only provide information about cars that are in our inventory. 
                Given the list of cars in inventory: {', '.join(car_details)}, please provide details about a specific car. 
                If the car is not in the list, respond that the car is not available. If the user asks about any other topic, 
                respond accordingly without adding any car-related prompts."""
                },
                {"role": "user", "content": prompt + " give response in one line"}],
                temperature=0.6,
                max_tokens=150,
                top_p=1,
                stream=False,
                stop=None,
        )
    
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."

def send_email(to_address, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        msg = 'Subject: {}\n\n{}'.format(subject, body)
        server.starttls()
        server.login('koundinyasaran@gmail.com', 'gugr gdxr qvwy ilkg')
        server.sendmail('koundinyasaran@gmail.com', to_address, msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def voice_chatbot():
    print("Entered")
    speak_text( "Hi, I'm Sandy. How can I assist you today? I can provide you with details about the BMW cars available in our showroom, compare cars based on your preferences, and help you find the best car for your needs."
)

    while True:
        query = recognize_speech()
        if query:
            #print(query)
            if "goodbye" in query.lower() or "thank you" in query.lower() or "bye" in query.lower():
                speak_text("Thank you for calling us. Goodbye!")
                break
            elif "book appointment" in query.lower() or "appointment" in query.lower():
                response = generate_response(query + "provide in one sentence less than 10 words: you can say i would like book an appointment according to your schedule")
                speak_text(response)
                speak_text("do you want to book an appointment: Say yes or no ")
                query = recognize_speech()
                if "yes" in query.lower():
                    book_appointment()
                    break
                else :
                    speak_text("Goodbye. Thanks for calling us , have a good day and take care")
            else:
                response = generate_response(query)
                #print(f"Chatbot response: {response}")
                speak_text(response)

voice_chatbot()
