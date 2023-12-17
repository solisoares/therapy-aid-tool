from therapy_aid_tool.ORM.models import Video


def test_video():
    x = Video(
        filepath="filepath",
        closeness="closeness",
        interactions="interactions",
        interactions_statistics="interactions_statistics",
    )
    assert x.filepath == "filepath"
    assert x.closeness == "closeness"
    assert x.interactions == "interactions"
    assert x.interactions_statistics == "interactions_statistics"
    print(x.__repr__())
