# Spotify_map_app

> This is a Python web application allows user to see map of markets where most popular track (according to spotify) of an artist that was given is available.
> 

### Usage:

Run this in your terminal

```powershell
...\Spotify_map_app> python main.py
```

You should see something like this

```powershell
* Serving Flask app 'main'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
* Debugger PIN: 109-893-471
```

Now go to your [localhost](http://127.0.0.1:5000) trough right port. You should see this on page.

![Untitled](Spotify_map_app%2099166f6ba5db43858889640fd1ac06f5/Untitled.png)

Enter relevant information, after some time ≈ 10s the map of markets should appear

![Untitled](Spotify_map_app%2099166f6ba5db43858889640fd1ac06f5/Untitled%201.png)

### Important Functions:

- **`create_map(markets)`** generates an HTML map of track markets using the **`folium`** library. The function takes a list of available markets as an argument, and returns the resulting map as a **`folium.Map`** object.
- **`launch(client_id, client_secret, search_artist)`** is the main function of the application. It calls several other functions from other Python modules to get the necessary data from the Spotify API, including the artist name, the most popular track name, and the list of available markets for that track. It then calls **`create_map()`** to generate the map of track markets, and returns the resulting map.
- **`home()`** is a Flask route function that renders the **`home.html`** template. This function is called when the user navigates to the root URL of the application.
- **`get_artist()`** is another Flask route function that is called when the user submits the search form on the **`home.html`** template. This function gets the artist name and the user's Spotify API credentials from the form, and calls **`launch()`** to generate the map of track markets. It then adds a custom HTML title to the map, and returns the rendered map to the user.

### **Credits**

This project was created by **[Ustym Hentosh](https://github.com/ustymhentosh)**.