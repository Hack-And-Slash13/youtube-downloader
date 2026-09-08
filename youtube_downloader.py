import yt_dlp, sys, os

def get_ffmpeg_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

print("Hello! I can download any youtube video. (must be run in command prompt for livestreams to work right)")
while True:
    video_type = input("Do you want to download a livestream, livestream audio, video, or audio?")
    while video_type.lower() != "livestream audio" and video_type.lower() != "livestream" and video_type.lower() != "video" and video_type.lower() != "audio":
        video_type = input("Well? Livestream, livestream audio, video, or audio?")
    url = input("What's the URL to the youtube video you want to download?")
    filetype = input("What file type should I save it as? (type the file extension without the period or press enter to keep the original audio file)")
    folder = input("Where do you want the file saved? (full path to folder, or press enter to save to the folder this file is in)")
    if folder == "":
        folder = os.getcwd()
    name = input("What should I name it? (type a name or press enter to use the youtube video's name)")
    print("downloading...")
    if video_type == "livestream" or video_type == "livestream audio":
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
                    "postprocessors": [{
                        "key": "FFmpegVideoConvertor",
                        "preferredcodec": filetype,
                        "preferredquality": "320",
                    }],
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
        print(f"Done! Saved in {folder}")
    except Exception as e:
        print(f"Error: {e}")
