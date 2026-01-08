#Make sure ollama is running in background as this program is build on LLMA local so one need to install it
# ollama pull llama3 

import requests
import time
import pyautogui as pg
import streamlit as st


def chat_once(user_input: str, history: list) -> str:
    conversation = "You are a humorous, funny, roast-style assistant.\n\n"

    # Inject previous chat history
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"

    # Add current user input
    conversation += f"User: {user_input}\nAssistant:"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": conversation,
            "stream": False
        },
        timeout=120
    )
    return response.json()["response"]

#optional (IF YOUR PROGRAM DOESNT RUN COMMENT OUT THIS SECTION and write "streamlit run main.py" in terminal to start the web application)
pg.click(x=301,y=847)
time.sleep(0.5)
pg.write("streamlit run main.py")
time.sleep(0.5)
pg.press("enter")
time.sleep(0.5)


#Web setup
st.set_page_config(page_title="Chat Bot", layout="centered")
st.title("Humorous Web Chat Application")

    #chat history initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", placeholder="Type your message here")

if user_input:
    reply = chat_once(user_input,st.session_state.chat_history)

    st.session_state.chat_history.append(
        {"role": "user", "content" : user_input}
    )

    st.session_state.chat_history.append(
        {"role": "assistant", "content" : reply}
    )

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")