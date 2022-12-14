from therapy_aid_tool.models.video import VideoBuilder
from pathlib import Path


ROOT = Path(__file__).parents[1].resolve()


def test_frames_count():
    # This video has 33 frames
    filepath = str(ROOT/"sample_data/quick_video_plusme.mp4")
    video = VideoBuilder(filepath).build()

    closeness = video.closeness
    interactions = video.interactions

    frames_count1 = len(list(closeness.values())[0])
    frames_count2 = len(list(interactions.values())[0])

    assert frames_count1 == 33
    assert frames_count2 == 33
