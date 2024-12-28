from attr import dataclass
from typing import List, Union
from pathlib import Path


@dataclass
class Config:
    profile: Union[str, None]
    path: Path
    data: dict


@dataclass
class ConfigProfile:
    name: str
    path: Path


@dataclass
class DownloadStatus:
    spotify_id: str
    deezer_id: str
    requested_isrc: str
    downloaded_isrc: str
    requested_url: str
    downloaded_url: str
    requested_bitrate: str
    downloaded_bitrate: str
    success: bool
    skipped: bool
    errors: List[str]
    download_path: str
    md5: str


@dataclass
class BackupManifest:
    profile: Union[str, None]
    spotify_user: str
    timestamp: str
    checksum: str


@dataclass
class BackupSnapshot:
    profile: Union[str, None]
    username: str
    config: Path
    spotify: Path
    processed: Path
    playlists: Path
    oauth: Path


@dataclass
class ProcessedSong:
    """Class for keeping track of an offline song."""

    spotify_title: str = None
    spotify_artist: str = None
    spotify_isrc: str = None
    spotify_url: str = None
    spotify_id: str = None
    deezer_title: str = None
    deezer_artist: str = None
    deezer_isrc: str = None
    deezer_url: str = None
    deezer_id: str = None
    matched: bool = None
    match_type: str = None
    match_message: str = None
    match_pending_download: bool = None
    downloaded: str = None
    download_isrc: str = None
    download_url: str = None
    download_path: str = None
    download_md5: str = None
    download_bitrate: str = None
    download_failed: bool = None
    download_failed_reason: str = None


class SpotifySong:
    def __init__(
        self,
        id_=None,
        artist=None,
        album=None,
        title=None,
        url=None,
        isrc=None,
        explicit=None,
    ):
        self.id_: id_
        self.artist: artist
        self.album: album
        self.title: title
        self.url: url
        self.isrc: isrc
        self.explicit: explicit

    def from_api(self, song: dict):
        # Safely get the 'track' dictionary or default to an empty dictionary
        track = song.get("track", {})
        
        if not track:
            # If 'track' is None or empty, initialize fields to default values
            self.id_ = None
            self.artist = None
            self.album = None
            self.title = None
            self.url = None
            self.isrc = None
            self.explicit = None
            return  # Exit early if no track data is available
        
        # Safely access each attribute within 'track'
        self.id_ = track.get("id", None)
        self.artist = (
            track.get("artists", [{}])[0].get("name", None) 
            if track.get("artists") else None
        )
        self.album = track.get("album", {}).get("name", None)
        self.title = track.get("name", None)
        self.url = track.get("external_urls", {}).get("spotify", None)
        self.isrc = track.get("external_ids", {}).get("isrc", None)
        self.explicit = track.get("explicit", None)

    def from_dict(self, dictionary: dict):
        self.id_ = dictionary["id_"]
        self.artist = dictionary["artist"]
        self.album = dictionary["album"]
        self.title = dictionary["title"]
        self.url = dictionary["url"]
        self.isrc = dictionary["isrc"]
        self.explicit = dictionary["explicit"]

    def is_valid(self):
        if self.id_ is not None and self.isrc is not None:
            return True

        return False
