from flask import Flask, redirect, request
from api.spotify_client import SpotifyClient
from services.rec_service import RecommendationService

app = Flask(__name__)
spotify_client = SpotifyClient()
service = RecommendationService()


@app.route("/")
def index():
    return '<h2>Welcome!</h2><a href="/login">Login with Spotify</a>'


@app.route("/login")
def login():
    return redirect(spotify_client.get_auth_url())


@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_data = spotify_client.get_token(code)
    access_token = token_data.get("access_token")

    debug_html = ""

    # Get recent tracks
    tracks = service._get_recent_tracks(access_token)
    debug_html += f"<h3>Parsed Tracks:</h3><pre>{[(t.name, t.artist) for t in tracks]}</pre>"

    # Get recommendations + TasteDive debug
    recommendations, td_debug = service.recommend_movies(access_token)

    debug_html += "<h3>TasteDive Results:</h3><pre>"
    for track_name, movies in td_debug.items():
        debug_html += f"{track_name}: {movies}\n"
    debug_html += "</pre>"

    if recommendations:
        debug_html += "<h3>Recommendations:</h3>"
        for r in recommendations:
            debug_html += "<div style='margin-bottom: 20px;'>"
            debug_html += f"<strong>{r.based_on_song}</strong> → {r.movie_title}<br>"
            if r.details:
                debug_html += f"Year: {r.details.get('year')}, Genre: {r.details.get('genre')}<br>"
                debug_html += f"Plot: {r.details.get('plot')}<br>"
                poster_url = r.details.get("poster")
                if poster_url and poster_url != "N/A":
                    debug_html += f"<img src='{poster_url}' alt='Poster' width='200'><br>"
            debug_html += "</div>"
    else:
        debug_html += "<h3>No recommendations found.</h3>"

    return debug_html



if __name__ == "__main__":
    app.run(port=5000, debug=True)
