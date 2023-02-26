from flask import Flask, render_template, request
import folium
import json
import base64
import requests
import pycountry


def get_token(CLIENT_ID, CLIENT_SECRET):
    """ 
    Gets acces token from id and sectet

    Args:
        CLIENT_ID(str): client id
        CLIENT_SECRET(str): client secret
    Returns:
        (str): access token
    """

    auth_code = f'{CLIENT_ID}:{CLIENT_SECRET}'

    coded_credentials = base64.b64encode(auth_code.encode()).decode()

    auth_url = 'https://accounts.spotify.com/api/token'

    auth_data = {'grant_type': 'client_credentials'}

    auth_headers = {'Authorization': f'Basic {coded_credentials}'}

    response = requests.post(auth_url, data = auth_data, headers=auth_headers)

    access_token = response.json().get('access_token')

    return access_token



def get_artist_id_and_name(search_name, token):
    """ 
    Gets artist name and id 

    Args:
        search_name(str): query to seach
        token(str): access token
    Returns:
        (tuple): artist name and id 
    """
    # searching input
    search_url = 'https://api.spotify.com/v1/search'
    request_params = {'query': search_name, 'type': 'artist'}
    request_headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(search_url, params=request_params, headers=request_headers)

    response = response.json()["artists"]['items'][0]

    

    return response['name'], response['id']


def get_artist_top_track(artist_id, token, country = '', market = ''):
    """
    Gets artist's top track

    Argas:
        artist_id(str): artists id
        token(str): access token
        country(str): (optional) country where to search
        market(str): (optional) market where to search
    Returns:
        (tuple): artist top track name and id
    """
    request_params = {'market': 'US'}
    if country:
        request_params['country'] = country
    if market:
        request_params['market'] = market
    
    request_headers = {'Authorization': f'Bearer {token}'}
    search_url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'

    response = requests.get(search_url, params=request_params, headers=request_headers)

    return response.json()['tracks'][0]['name'], response.json()['tracks'][0]['id']


def get_track_markets(track_id, token):
    """
    Gets track markets

    Args:
        track_id(str): ID of track
        token(str): Access token
    Retuns:
        (list): available markets
    """
    search_url = f'https://api.spotify.com/v1/tracks/{track_id}'
    request_headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(search_url, headers=request_headers)

    return response.json()['album']['available_markets']


def crete_map(markets):
    """ 
    Geretates html map of track markets

    Args:
        markets(list): list of available markets
    Retuens:
        No return

    """
    atlas = folium.Map()
    alpha_3 = []
    with open('database\countries.geojson', encoding='utf-8') as raw_file:
        countries_geo = json.load(raw_file)
        for initial in markets:
            try:
                alpha_3.append(pycountry.countries.get(alpha_2 = initial).alpha_3)
            except AttributeError:
                    continue

        check_list = []

        for j in countries_geo['features']:
            # for j in countries_geo['features']:
            if j['properties']["ISO_A3"] in alpha_3:
                check_list.append(j['properties']["ISO_A3"])
                cntr = folium.GeoJson(j, name=j['properties']["ISO_A3"])
                folium.Popup(j['properties']["ADMIN"]).add_to(cntr)
                cntr.add_to(atlas)
                
    return atlas


def launch(client_id, client_secret, search_artist):
    """
    Starts getting info from API, generates map of markets
    Returns track name

    Args:
        client_id(str): ID of user(client)
        client_secret(str): SECRET of user(client)
        search_artist(str): Search request
    Retuns:
        (str): most popular track name
    """
    token = get_token(client_id, client_secret)

    artist = get_artist_id_and_name(search_artist, token)
    global artist_name
    artist_id = artist [1]
    artist_name = artist[0]

    track = get_artist_top_track(artist_id, token)
    global track_name
    track_name = track[0]
    track_id = track[1]

    track_markets = get_track_markets(track_id, token)

    atlas = crete_map(track_markets)

    return atlas

app = Flask(__name__)

@app.route("/")
def home():
    """ renders home.html """
    return render_template("home.html")


@app.route('/', methods=['POST'])
def get_artist():
    """
    Gets client id, artist and secret from html form
    begins generation of map of most popular track markets 
    """
    artist_querry = request.form['Artist']
    client_id = request.form['Client id']
    client_secret = request.form['Client secret']

    atlas = launch(client_id, client_secret, artist_querry)

    title_html = f'''
             <h3 align="center" style="font-size:16px"><b>{artist_name} - {track_name}</b></h3>
             '''

    atlas.get_root().html.add_child(folium.Element(title_html))
    return atlas.get_root().render()



if __name__ == "__main__":
    app.run(debug=True)