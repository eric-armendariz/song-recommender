import requests
import base64
import json


def main():
    #Get Auth token from Spotify API
    #client_id = 
    #client_secret = 

    client_creds = base64.b64encode(f"{client_id}:{client_secret}".encode())
    token_url = "https://accounts.spotify.com/api/token"

    token_data = {
        "grant_type": "client_credentials"
    }

    token_header = {
        "authorization": f"Basic {client_creds.decode()}"
    }

    r = requests.post(token_url, data=token_data, headers=token_header)
    token_response = r.json()
    access_token = token_response['access_token']

    request_header = {
        "Authorization": f"Bearer {access_token}"
    }


    #Get playlists from user
    #get_user_id(request_header)

    get_user_playlists(request_header)


def get_user_id(header):
    web_link = "https://api.spotify.com/v1/me"
    r = requests.get(web_link, headers=header)
    response = r.json()
    uri = response['uri']
    return uri[13:]
    

def get_user_playlists(header, user_id="ena456-us"):
    web_link = "https://api.spotify.com/v1/users/" + user_id + "/playlists"
    r = requests.get(web_link, headers=header)

    my_playlists = r.json()

    print(my_playlists['items'][0]['name'])

    

if __name__ == "__main__":
    main()