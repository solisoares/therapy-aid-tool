from therapy_aid_tool.video_parser import VideoParser


def test_frames_count():
    # This video has 33 frames
    in_video = "/home/alexandre/therapy-aid-tool/sample_data/quick_video_plusme.mp4"
    parser = VideoParser(in_video, n_classes=6)

    closeness = parser.closeness()
    interactions = parser.interactions()
    statistics = parser.interactions_statistics(interactions)

    frames_count1 = len(list(closeness.values())[0])
    frames_count2 = len(list(interactions.values())[0])

    assert frames_count1 == 33
    assert frames_count2 == 33
