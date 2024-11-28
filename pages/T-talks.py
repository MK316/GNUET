import streamlit as st
from gtts import gTTS
import pandas as pd
import random
from io import BytesIO
import base64
import requests

# URLs for each tab's data
urls = {
    "Opening": "https://raw.githubusercontent.com/MK316/GNUET/refs/heads/main/data/t-talks01.csv",
    "Objectives": "https://raw.githubusercontent.com/MK316/GNUET/refs/heads/main/data/t-talks01.csv",
    "Feedback": "https://raw.githubusercontent.com/MK316/GNUET/refs/heads/main/data/t-talks01.csv",
    "Closing": "https://raw.githubusercontent.com/MK316/GNUET/refs/heads/main/data/t-talks01.csv"
}

# Function to load data from a URL
def load_data(url):
    response = requests.get(url)
    data = pd.read_csv(BytesIO(response.content))
    return data

# Function to play audio
def play_audio(text):
    tts = gTTS(text, lang='en')
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay>'
    st.markdown(href, unsafe_allow_html=True)

# Main app
def main():
    st.title("Multipage App with Multiple Tabs and Audio")
    
    tab_keys = ["Opening", "Objectives", "Feedback", "Closing"]
    tabs = st.tabs(tab_keys)

    data_stores = {}
    for i, key in enumerate(tab_keys):
        with tabs[i]:
            if key not in data_stores:
                data_stores[key] = load_data(urls[key])
            data = data_stores[key]

            mode = st.radio("Choose display mode:", ('Ordered', 'Random'), key=f'mode_{key}')
            index = st.session_state.get(f'index_{key}', 0)

            if mode == 'Random':
                chosen_row = data.sample()
            else:
                if index >= len(data):
                    index = 0
                chosen_row = data.iloc[index]
                st.session_state[f'index_{key}'] = index + 1

            expression = chosen_row['Expression'].values[0]
            st.write(expression)
            play_audio(expression)

            if st.button("Next", key=f'next_{key}'):
                if mode == 'Random':
                    chosen_row = data.sample()
                else:
                    index = st.session_state[f'index_{key}']
                    if index >= len(data):
                        index = 0
                    chosen_row = data.iloc[index]
                    expression = chosen_row['Expression'].values[0]
                    st.session_state[f'index_{key}'] = index + 1
                    st.write(expression)
                    play_audio(expression)

if __name__ == "__main__":
    main()
