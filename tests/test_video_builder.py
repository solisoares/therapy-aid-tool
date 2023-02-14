from therapy_aid_tool.models.video import VideoBuilder
from pathlib import Path
import requests

ROOT = Path(__file__).parents[1].resolve()


def download_quick_video():
    url = "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/quick_video_plusme.mp4"
    response = requests.get(url)
    with open(ROOT/"quick_video_plusme.mp4", "wb") as f:
        f.write(response.content)


def test_frames_count():
    download_quick_video()

    # This video has 33 frames
    filepath = str(ROOT/"quick_video_plusme.mp4")
    video = VideoBuilder(filepath).build()

    closeness = video.closeness
    interactions = video.interactions

    frames_count1 = len(list(closeness.values())[0])
    frames_count2 = len(list(interactions.values())[0])

    assert frames_count1 == 33
    assert frames_count2 == 33

    Path(ROOT/"quick_video_plusme.mp4").unlink()
