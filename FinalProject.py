"""
Spotify Artist Top 10 Songs Finder and Compare

This script allows the user to search for an artist on Spotify and retrieve and compare their top 10 songs

How to use my script:
1. Make sure to set the Spotify API credentials (client_ID and client_secret) in a .env file
2. Run the script, and it will prompt you to enter the two names of the artist you want to search and compare

PS: You have to have a solid internet connection since I am grabbing from spotify's API

Programmer: Jarrett Karner
"""

import json
import base64
from requests import post, get
from dotenv import load_dotenv
import os
import re
import pandas as pd
import numpy as np

# Load environment variables from .env file
load_dotenv()

client_id = os.getenv("client_ID")
client_secret = os.getenv("client_secret")

# Function to retrieve an access token from the Spotify API
def get_token():
    auth_string = f"{client_id}:{client_secret}"
    #Returns base64 object and coverting to a string
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

#Linking url for the data
    url = "https://accounts.spotify.com/api/token"
    #ssociated with requests
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Function to generate the authorization header using the provided access token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Function to search for artists on Spotify
def search_for_artists(token, artist_names):
    artists = artist_names.split(',')
    results = []

    for artist_name in artists:
        if not re.match("^[a-zA-Z0-9 ]+$", artist_name.strip()):
            print(f"Invalid characters in artist name: {artist_name}. Please use alphanumeric characters only.")
            continue

        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        query = f"?q={artist_name}&type=artist&limit=1"

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]

        if len(json_result) > 0:
            results.append(json_result[0])
        else:
            print(f"No artist with the name '{artist_name}' exists...")

    return results

# Function to retrieve the top tracks of an artist from Spotify
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

# Use Main function based on what we learned in class
if __name__ == "__main__":
    # Get the access token
    token = get_token()

    # Prompt the user to enter a comma-separated list of artists
    artist_names_input = input("Enter the names of two artists you want to search (use a comma to separate the names): ")

    # Search for the artists
    results = search_for_artists(token, artist_names_input)

    # Create a DataFrame to store the data
    data = []

    # Display the top 10 tracks and store data in the DataFrame
    for result in results:
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)

        print(f"\nTop 10 songs for {result['name']}:\n")
        for idx, song in enumerate(songs[:10]):
            print(f"{idx + 1}. {song['name']}")

            # Store data in the DataFrame
            data.append({
                'Artist': result['name'],
                'Track Name': song['name'],
                'Popularity': song['popularity']
            })

    # Created a DataFrame from the data that we got
    df = pd.DataFrame(data)

    # I wrote the data to a detailed csv file
    df.to_csv('top_tracks_data.csv', index=False)

    # Reading the data back from the csv file
    df_read = pd.read_csv('top_tracks_data.csv')

    # Display the DataFrame where Popularity is greater than a threshold that is 20
    threshold = 20
    subset_df = df_read[df_read['Popularity'] > threshold]
    print(f"\nSubset of DataFrame where Popularity > {threshold}:\n")
    print(subset_df)
