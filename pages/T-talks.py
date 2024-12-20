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
    if response.status_code == 200:
        data = pd.read_csv(BytesIO(response.content))
        return data
    else:
        st.error(f"Failed to load data from {url}. HTTP status: {response.status_code}")
        return pd.DataFrame()

# Function to play audio
def play_audio(text):
    tts = gTTS(text, lang='en')
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<audio controls src="data:audio/mp3;base64,{b64}"></audio>'
    st.markdown(href, unsafe_allow_html=True)

# Main app
def main():
    st.title("Teacher talks")
    
    tab_keys = ["Opening", "Objectives", "Feedback", "Closing"]
    tabs = st.tabs(tab_keys)

    data_stores = {}
    for i, key in enumerate(tab_keys):
        with tabs[i]:
            if key not in data_stores:
                data_stores[key] = load_data(urls[key])
            data = data_stores[key]

            mode = st.radio("Choose display mode:", ('Ordered', 'Random'), key=f'mode_{key}')
            index_key = f'index_{key}'
            index = st.session_state.get(index_key, 0)

            if mode == 'Random':
                chosen_row = data.sample().reset_index(drop=True)
            else:
                if index >= len(data):
                    index = 0
                chosen_row = data.iloc[[index]].reset_index(drop=True)
                st.session_state[index_key] = index + 1

            if not chosen_row.empty:
                expression = chosen_row['Expression'].iat[0]
                st.write(expression)
                play_audio(expression)

                if st.button("Next", key=f'next_{key}'):
                    st.session_state[index_key] += 1  # Increment index to update the state
                    # Use the following line to refresh only the necessary parts or manage states more granularly
                    # st.write or st.empty to update parts of your app instead of rerunning everything

if __name__ == "__main__":
    main()
