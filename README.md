
# 🚗 Smart Conversations on Wheels

### A Next-Gen Voice Chatbot for Car Showrooms

> **Technologies**: PyTorch, Groq API, Google API, Llama 3.1, Google Calendar, gTTS, Streamlit, Speech Recognition, Python

---

## 📌 Overview

**Smart Conversations on Wheels** is an advanced, voice-enabled AI assistant built for car showrooms to automate customer interactions such as appointment scheduling, inventory inquiries, and vehicle comparisons. Powered by **LLMs (Llama3.1 via Groq API)** and **Google’s APIs**, this bot streamlines showroom workflows, boosts user satisfaction, and reduces manual effort by up to **60%**.

---

## ✨ Features

* 🔊 **Voice-Controlled Chatbot**: Built with `speech_recognition` and `gTTS` for real-time voice interaction.
* 📆 **Appointment Scheduler**: Integrated with **Google Calendar API** to check availability and book visits.
* 🚗 **Car Inventory Assistant**: Intelligent query handling for car details and comparisons.
* 🧠 **LLM Integration**: Uses `Groq API` with **Llama 3.1** for generating human-like responses.
* 📧 **Email Integration**: Sends appointment details to users' email using Gmail SMTP.
* 🛠️ **Smart Parsing**: Extracts and validates time, dates, phone numbers using `regex`, `dateparser`.
* ✅ **Failsafes**: Handles fallback for unrecognized speech or invalid inputs.
* 📉 **Impact**: Reduced manual intervention by **60%**, increased customer handling efficiency by **40%**.

---

## 🛠️ Tech Stack

| Component              | Tool / Library                         |
| ---------------------- | -------------------------------------- |
| Voice Interface        | `speech_recognition`, `gTTS`, `pygame` |
| Calendar Scheduling    | `Google Calendar API`, `OAuth`         |
| LLM Integration        | `Groq API` (LLaMA 3.1 model)           |
| NLP + Prompting        | `Groq.ChatCompletion`                  |
| UI/UX Layer (Optional) | `Streamlit`                            |
| Email Delivery         | `smtplib`, `email.mime`                |
| Time Parsing           | `dateparser`, `datetime`               |

---

## 🚗 Supported Cars

Supports inquiry for **20+ BMW models**, categorized into:

* SUVs, Coupes, Roadsters
* Electric Vehicles
* M-series Sports Cars

See `car_inventory` in code for full list.

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/smart-conversations-on-wheels.git
cd smart-conversations-on-wheels

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API credentials
# - credentials.json for Google OAuth
# - .env file for Groq API key

# 4. Run the assistant
python voice_chatbot.py
```

---

## 🔐 API Setup

### 🗝️ `.env` file

```
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_google_gemini_key
```

### 🔑 Google Calendar Auth

* Save your `credentials.json` from Google Cloud Console in project root.
* Script handles token creation via `token.json`.

---

## 🧠 Sample Interaction

**User**: “Tell me about BMW X5”
**Bot**: “BMW X5 is a luxury mid-size SUV with cutting-edge features.”

**User**: “I want to book an appointment”
**Bot**: "Sure! Let's get your name, phone, and preferred time."

---

## 📨 Email Preview

```
Subject: Appointment Booking

Details:
Name: John Doe
Phone: (123) 456-7890
Date: June 1, 2025
Time: 11:00 AM
```

---

## 📬 Contact

Built by [Saran Koundinya Tummalagunta](https://www.linkedin.com/in/sarankoundinya/)

Feel free to reach out for collaboration or feature suggestions!

---

Let me know if you want me to generate a `requirements.txt` as well or turn this into a downloadable file.
