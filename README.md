Spotify Artist Top 10 Songs Finder and Compare

This script allows the user to search for an artist on Spotify and retrieve and compare their top 10 songs

How to use my script:

1. Make sure to set the Spotify API credentials (client_ID and client_secret) in a .env file

2. Run the script, and it will prompt you to enter the two names of the artist you want to search and compare

PS: You have to have a solid internet connection since I am grabbing from spotify's API

Programmer: Jarrett Karner


READ.ME

This script is intended to:

Authentication:
- The script get an access token from the Spotify API using client credentials.

Artist Search:
- Users can input two artist names (comma-separated) to search for on Spotify.
- The script checks artist names and provides feedback on invalid characters.

Top 10 Songs Retrieval:
- For each artist, the script gets and displays their top 10 songs along with popularity ratings.

Data Storage:
- The script stores the data in a Pandas DataFrame.

CSV File:
- The script writes the data to a CSV file named top_tracks_data.csv.

Data Analysis:
- The script reads back data from the CSV file and displays some of the DataFrame where song popularity is greater than a specified threshold (default threshold is 20).

Feel free to contribute or add anything that would enhance the program :)
