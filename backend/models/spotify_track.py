# models/spotify_track.py

class SpotifyTrack:
    def __init__(self, name, artist, album_image=None, spotify_url=None):
        self.name = name
        self.artist = artist
        self.album_image = album_image
        self.spotify_url = spotify_url

    @classmethod
    def from_spotify_json(cls, data):
        """
        Convert Spotify API track JSON into a SpotifyTrack object.
        """
        if not data:
            return None

        name = data.get("name")
        
        # Get first artist name safely
        artists = data.get("artists", [])
        artist = artists[0]["name"] if artists else None

        # Get album image URL safely
        album_image = None
        album = data.get("album")
        if album and "images" in album and len(album["images"]) > 0:
            album_image = album["images"][0].get("url")

        # Get Spotify track URL safely
        spotify_url = data.get("external_urls", {}).get("spotify")

        if not name or not artist:
            # Skip tracks without basic info
            return None

        return cls(name=name, artist=artist, album_image=album_image, spotify_url=spotify_url)
