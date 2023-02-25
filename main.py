from flask import Flask, render_template, request
from generate_map import launch

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
    artist_name = request.form['Artist']
    client_id = request.form['Client id']
    client_secret = request.form['Client secret']
    launch(client_id, client_secret, artist_name)
    return render_template('Test.html')


if __name__ == "__main__":
    app.run(debug=True)