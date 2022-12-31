from therapy_aid_tool.models._video_inference import download_weights
from pathlib import Path


ROOT = Path(__file__).parents[1].resolve()


def test_download_weights_from_gh_release1():
    download_weights(ROOT/"full1-yolov5x-img256-bs1.pt")
    download_weights(ROOT/"full1-yolov5s-img256-bs1.pt")
    download_weights(ROOT/"full1-yolov5s-img512-bs16.pt")
    download_weights(ROOT/"full1-yolov5m-img256-bs1.pt")
    download_weights(ROOT/"full1-yolov5m-img512-bs1.pt")
    download_weights(ROOT/"full1-yolov5n6-img1280-bs1.pt")
    download_weights(ROOT/"full1-yolov5s-img640-bs1.pt")

    assert (ROOT/"full1-yolov5x-img256-bs1.pt").stat().st_size == 172971677
    assert (ROOT/"full1-yolov5s-img256-bs1.pt").stat().st_size == 14265589
    assert (ROOT/"full1-yolov5s-img512-bs16.pt").stat().st_size == 14328565
    assert (ROOT/"full1-yolov5m-img256-bs1.pt").stat().st_size == 42057005
    assert (ROOT/"full1-yolov5m-img512-bs1.pt").stat().st_size == 42119981
    assert (ROOT/"full1-yolov5n6-img1280-bs1.pt").stat().st_size == 6933717
    assert (ROOT/"full1-yolov5s-img640-bs1.pt").stat().st_size == 14370037

    (ROOT/"full1-yolov5x-img256-bs1.pt").unlink()
    (ROOT/"full1-yolov5s-img256-bs1.pt").unlink()
    (ROOT/"full1-yolov5s-img512-bs16.pt").unlink()
    (ROOT/"full1-yolov5m-img256-bs1.pt").unlink()
    (ROOT/"full1-yolov5m-img512-bs1.pt").unlink()
    (ROOT/"full1-yolov5n6-img1280-bs1.pt").unlink()
    (ROOT/"full1-yolov5s-img640-bs1.pt").unlink()
