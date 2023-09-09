import ffmpeg
from pytube import YouTube
import time
import os

print("*" * 100)


def clean_filename(name):
    forbidden_chars = "\"*\\/'.|?:<>"
    filename = (
        ("".join([x if x not in forbidden_chars else "#" for x in name]))
        .replace("  ", " ")
        .strip()
    )
    if len(filename) >= 176:
        filename = filename[:170] + "..."
    return filename


def download_video(link, res_level="FHD"):
    ti = time.time()
    try:
        yt = YouTube(link)
    except Exception as e:
        print("An error occurred while fetching the video:", str(e))
        return

    print(
        yt.title,
        "|",
        yt.author,
        "|",
        yt.publish_date.strftime("%Y-%m-%d"),
        "|",
        yt.views,
        "|",
        yt.length,
        "sec",
    )

    if res_level == "4K":
        dynamic_streams = [
            "2160p",
            "1440p",
            "1080p",
            "720p",
            "720p",
            "480p",
            "480p",
        ]
    elif res_level == "FHD":
        dynamic_streams = [
            "1080p",
            "720p",
            "720p",
            "480p",
            "480p",
        ]
    for ds in dynamic_streams:
        try:
            stream = yt.streams.filter(res=ds, progressive=False).first()
            if stream:
                stream.download(filename="video.mp4")
                audio_stream = yt.streams.filter(only_audio=True, abr="160kbps").first()
                if audio_stream:
                    audio_stream.download(filename="audio.mp3")
                else:
                    print("Audio stream not available for", ds)
                break
        except Exception as e:
            print("An error occurred while downloading the video:", str(e))
            continue

    # Check if audio and video files exist before merging
    if os.path.exists("audio.mp3") and os.path.exists("video.mp4"):
        audio = ffmpeg.input("audio.mp3")
        video = ffmpeg.input("video.mp4")
        filename = "C:\\Users\\Admin\\Downloads\\" + clean_filename(yt.title)

        duplicated = [
            "",
            "1",
            "2",
            "3",
            "4",
            "5",
        ]  # if duplicated filename found, append with version number
        for dup in duplicated:
            try:
                ffmpeg.output(audio, video, filename + dup + ".mp4").run()
                break
            except Exception as e:
                print("An error occurred while merging audio and video:", str(e))
                continue

        print(ds, "video successfully downloaded from", link)
        print("Time taken: {:.0f} sec".format(time.time() - ti))
    else:
        print("Audio or video file not found. Merging skipped.")


# Replace 'your_youtube_link_here' with the actual YouTube video link you want to download.
video_link = "https://www.youtube.com/watch?v=bON-KPiiNCk&pp=ygUOc21hbGwgNGsgdmlkZW8%3D"

# Call the download_video function with the video link and desired resolution level.
download_video(video_link, res_level="4K")
