from therapy_aid_tool.interaction_detector import interaction_detector


def test_frames_count():
    # The following video has 33 frames
    in_video = "/home/alexandre/therapy-aid-tool/sample_data/quick_video_plusme.mp4"
    interactions = interaction_detector(in_video)
    frames_count = len(list(interactions.values())[0])
    assert frames_count == 33