import yt_dlp, sys, os, urllib.request, json, subprocess
from packaging.version import Version
from mutagen.id3 import (
    ID3,
    ID3NoHeaderError,
    TIT1,
    TIT2,
    TIT3,
    TPE1,
    TPE2,
    TPE3,
    TPE4,
    TALB,
    TCOM,
    TEXT,
    TCON,
    TCOP,
    TDOR,
    TDRC,
    TENC,
    TFLT,
    TBPM,
    TKEY,
    TLEN,
    TLAN,
    TMED,
    TPOS,
    TPUB,
    TRCK,
    TSRC,
    TSSE,
    TMOO,
    TSST,
    TOAL,
    TOPE,
)

id3_frames = {
    "title": TIT2,
    "subtitle": TIT3,
    "grouping": TIT1,
    "artist": TPE1,
    "album artist": TPE2,
    "contributing artists": TPE1,
    "conductor": TPE3,
    "remixer": TPE4,
    "composer": TCOM,
    "lyricist": TEXT,
    "writer": TEXT,
    "album": TALB,
    "original album": TOAL,
    "original artist": TOPE,
    "track": TRCK,
    "track number": TRCK,
    "disc": TPOS,
    "disc number": TPOS,
    "genre": TCON,
    "year": TDRC,
    "date": TDRC,
    "recording date": TDRC,
    "original year": TDOR,
    "copyright": TCOP,
    "publisher": TPUB,
    "isrc": TSRC,
    "bpm": TBPM,
    "initial key": TKEY,
    "language": TLAN,
    "length": TLEN,
    "media type": TMED,
    "file type": TFLT,
    "encoding": TENC,
    "encoded by": TENC,
    "encoder settings": TSSE,
    "mood": TMOO,
    "set subtitle": TSST,
}

def resource_path(filename):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

def get_ffmpeg_path():
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return base_path

def get_latest_ytdlp_version():
    url = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "YouTubeDownloader"
        }
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)

    return data["tag_name"]

print("Hello! I can download any youtube video. (must be run in command prompt for livestreams to work right)")
print("")

if getattr(sys, 'frozen', False):
    print("Checking for updates...")
    try:
        current_version = Version(yt_dlp.__version__)
        if Version(get_latest_ytdlp_version()) > current_version:
            update = input("Can I update? y/n")
            while update.lower() != "y" and update.lower() != "n":
                update = input("Well? Can I update or not? y/n")
            if update.lower() == "y":
                subprocess.Popen([resource_path("updater.exe"), sys.executable])
                sys.exit()
            else:
                print("Fine, but I might break")
        else:
            print("Never mind, no updates")
    except Exception as error:
        print(error)

print("")
while True:
    mess_with_metadata = False
    video_type = input("Do you want to download a livestream, livestream audio, video, or audio?")
    while video_type.lower() != "livestream audio" and video_type.lower() != "livestream" and video_type.lower() != "video" and video_type.lower() != "audio":
        video_type = input("Well? Livestream, livestream audio, video, or audio?")
    url = input("What's the URL to the youtube video you want to download? (I can do playlists)")
    filetype = input("What file type should I save it as? (type the file extension without the period or press enter to keep the original audio file)")
    folder = input("Where do you want the file saved? (full path to folder, or press enter to save to the folder this file is in)")
    if folder == "":
        folder = os.getcwd()
    name = input("What should I name it? (type a name or press enter to use the youtube video's name. If it's a playlist, just click enter or I'll mess it up)")
    if video_type.lower() == "livestream audio" or video_type.lower() == "audio":
        mess_with_metadata = input("Should I mess with the metadata? (title, artist, album, year, etc) (if this is playlist, saying yes will throw an error) (only say yes if it's id3) y/n")
        while mess_with_metadata.lower() != "y" and mess_with_metadata.lower() != "n":
            mess_with_metadata = input("Well? Mess with metadata or not? y/n")
        if mess_with_metadata.lower() == "y":
            mess_with_metadata = True
            metadata_dict = {}
        else:
            mess_with_metadata = False
        if mess_with_metadata == True:
            while True:
                metadata = input("Type the names of the metadata you wanna set, seperated by commas (eg. title, contributing artists, year)")
                try:
                    metadata = [item.strip().lower() for item in metadata.split(",")]
                    break
                except Exception as e:
                    print(e)
            for data in metadata:
                if data == "title":
                    metadata_dict[data] = input(f"What should the {data} be? (press enter to use the filename)")
                else:
                    metadata_dict[data] = input(f"What should the {data} be?")
    print("downloading...")
    if video_type.lower() == "livestream" or video_type.lower() == "livestream audio":
        print("press Ctrl-C to stop (Will not work in IDLE)")
    try:
        ffmpeg_path = get_ffmpeg_path()
        if name == "":
            name = "%(title)s"
        filepath = os.path.join(
            folder,
            name,
        )
        if video_type.lower() == "audio":
            if filetype == "":
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": filepath,
                    "ffmpeg_location": ffmpeg_path,
                    "extractaudio": True,
                }
            else:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": filepath,
                    "ffmpeg_location": ffmpeg_path,
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": filetype,
                        "preferredquality": "320",
                    }],
                }
        elif video_type.lower() == "video":
            if filetype == "":
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "outtmpl": filepath,
                    "ffmpeg_location": ffmpeg_path,
                }
            else:
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "outtmpl": filepath,
                    "ffmpeg_location": ffmpeg_path,
                    "merge_output_format": filetype,
                }
        else:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "live_from_start": True,
                "outtmpl": filepath,
                "ffmpeg_location": ffmpeg_path,
                "hls_use_mpegts": True,
                "retries": float("inf"),
                "fragment_retries": float("inf"),
                "retry_sleep_functions": {
                    "http": lambda n: min(5 * n, 30),
                    "fragment": lambda n: min(5 * n, 30),
                },
            }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                filepath = ydl.prepare_filename(info)
                ydl.download([url])
        except KeyboardInterrupt:
            print("Download stopped. Converting...")
        if (video_type.lower() == "livestream audio" or video_type.lower() == "livestream") and filetype != "":
            filepath += ".ts"
            output_file = os.path.splitext(filepath)[0] + "." + filetype
            ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")
            if video_type.lower() == "livestream audio":
                command = [
                    ffmpeg_exe,
                    "-i", filepath,
                    "-vn",
                    output_file
                ]
            else:
                command = [
                    ffmpeg_exe,
                    "-i", filepath,
                    output_file
                ]
            result = os.system(" ".join(f'"{arg}"' for arg in command))
            if result == 0:
                os.remove(filepath)
            filepath = output_file
        if mess_with_metadata == True:
            try:
                audio = ID3(filepath)
            except ID3NoHeaderError:
                audio = ID3()

            for data, value in metadata_dict.items():
                data = data.lower().strip()

                if data in id3_frames:
                    if value != "":
                        audio.add(id3_frames[data](
                            encoding=3,
                            text=value
                        ))
                else:
                    print(f"Unknown metadata field: {data}")

            if "title" in metadata_dict and metadata_dict["title"] == "":
                title = os.path.splitext(os.path.basename(filepath))[0]
                audio.add(TIT2(
                    encoding=3,
                    text=title
                ))

            audio.save(filepath)
        print(f"Done! Saved in {folder}")
    except Exception as e:
        print(f"Error: {e}")
