# %% libraries
from elevenlabs import voices, generate, set_api_key, UnauthenticatedRateLimitError
import numpy as np
import streamlit as st
from elevenlabs import generate, play
from dotenv import load_dotenv, find_dotenv
from transformers import pipeline
import os
import requests

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


# %%  image 2 text
def img2text(url):
    captioner = pipeline(
        "image-to-text", model="Salesforce/blip-image-captioning-base")
    text = captioner(url)[0]['generated_text']

    print(text)
    return text


# img2text('profile pic venice.jpg')

# %%  LLM
# API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom-560m"
API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"

headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}


def generate_story(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


caption = 'a cup of coffee and a keyboard on a wooden table '

story = generate_story({
    "inputs": caption
})
print(story)
# %%  Image to audio
API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"
# API_URL = "https://api-inference.huggingface.co/models/speechbrain/tts-tacotron2-ljspeech"
# API_URL = "https://api-inference.huggingface.co/models/speechbrain/tts-tacotron2-ljspeech"
# API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}


def text2audio(message):
    payloads = {
        "inputs": message
    }
    response = requests.post(API_URL, headers=headers, json=payloads)

    with open('audio.flac', 'wb') as file:
        file.write(response.content)
    # return response.json()

# text2audio(story[0]['generated_text'])


# %% elevenlabs
# set_api_key("d4d9460e71f7fd550c3221b70950aa09")

# st.set_page_config(initial_sidebar_state="collapsed")


def pad_buffer(audio):
    # Pad buffer to multiple of 2 bytes
    buffer_size = len(audio)
    element_size = np.dtype(np.int16).itemsize
    if buffer_size % element_size != 0:
        audio = audio + b'\0' * (element_size - (buffer_size % element_size))
    return audio


def generate_voice(text, voice_name, model_name):
    audio = generate(
        text[:250],  # Limit to 250 characters
        voice=voice_name,
        model=model_name
    )
    audio_data = np.frombuffer(pad_buffer(audio), dtype=np.int16)
    audio_bytes = audio_data.tobytes()
    return audio_bytes


# %%
def main():
    st.set_page_config(page_title='Image to audio story')
    uploaded_file = st.file_uploader("Choose an image...")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open(uploaded_file.name, 'wb') as file:
            file.write(bytes_data)
        st.image(uploaded_file, use_column_width=True)
        caption = img2text(uploaded_file.name)

        st.text("Caption: ")
        st.write(caption)
        # with st.expander('Caption'):
        #     st.write(caption)

        # if st.button("Generate a story..."):
        # story = generate_story(caption)
        # st.text("Story: ")
        # st.write(story)
        # with st.expander('Story'):
        #     st.write(story)
        # text2audio(story[0]['generated_text'])

        text2audio(caption)
        st.audio("audio.flac")

    st.text("")


#######
    input_text = st.text_area(
        "Input Text (250 characters max)",
        value="Hahaha OHH MY GOD! This is SOOO funny, I-I am Eleven a text-to-speech system!",
        max_chars=250
    )

    all_voices = voices()
    input_voice = st.selectbox(
        "Voice",
        options=[voice.name for voice in all_voices],
        index=0
    )

    input_model = st.radio(
        "Model",
        options=["eleven_monolingual_v1", "eleven_multilingual_v1"],
        index=0
    )

    if st.button("Generate Voice"):
        try:
            audio = generate_voice(input_text, input_voice, input_model)
            st.audio(audio, format='audio/wav')
            play(audio)

        except UnauthenticatedRateLimitError:
            st.error(
                "Thanks for trying out ElevenLabs TTS! You've reached the free tier limit. Please provide an API key to continue.")
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()

# %%
