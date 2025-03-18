import streamlit as st
import requests

# Streamlit UI
st.title("🎶 Taylor Swift Lyrics Finder")
st.write("Enter the name of a Taylor Swift song to get its lyrics.")

# Input field for song name
song_name = st.text_input("Enter Song Name", "")

if st.button("Search Lyrics"):
    if song_name:
        # Making API request to Lyrics.ovh
        api_url = f"https://api.lyrics.ovh/v1/Taylor Swift/{song_name}"
        response = requests.get(api_url)

        if response.status_code == 200:
            lyrics = response.json().get("lyrics", "No lyrics found.")
            st.text_area("Lyrics", lyrics, height=300)
        else:
            st.error("Lyrics not found! Check the song name or try again.")
    else:
        st.warning("Please enter a song name.")
