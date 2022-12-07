<h1 align="center">Therapy Aid Tool</h1>
 
<h3 align="center">A Web App to aid in clinical and therapeutic decisions reducing analysis time for therapists</h3>

<p align="center">(The current version of this project aims to assist in decision making of Autism Spectrum Disorder (ASD) video sessions)</p>
<br>

## How our app can help in treatment?
The main goal is to provide a web aplication that is capable of filtering out relevant scenes of recorded therapy sessions to assist professionals in their analysis. With the use of Artificial Inteligence and Computer Vision our app is capable of:

* Handle large amounts of therapy session videos, storing and retrieving them as needed.
* Filter relevant scenes according to medical professionals.
    * Point exactly in time where is happening an event of interest in the video.
    * Reduce time for analysis of a whole video.
* Assistance in clinical and therapeutic decisions throughout interactive search and statistical reports.
    * Summary of interactions in each session.
    * Progress of interactions for all sessions.
> Our BRACIS [Paper](https://link.springer.com/content/pdf/10.1007/978-3-031-21689-3.pdf?pdf=button#page=243)

<br>

## Current technologies and heuristics used

### Core
* For the task of object detection we use a [YOLOv5](https://github.com/ultralytics/yolov5) trained deep learning model. YOLO detects where the main actors of a therapy session are by generating bounding boxes (bboxes) around each one of them. For our **current version**, the main actors of a **ASD therapy session** are the *Toddler*, *Caretaker* and the interactive teddy bear called [*PlusMe*](https://dl.acm.org/doi/pdf/10.1145/3491101.3519716?casa_token=iWYoiTNsB90AAAAA:x8TOj1oPpZoqyLTIV3FUw1yAIFTEnD_roG12wpDYmsIsg6JVSIjzj4whC2ky2Pj7oSv4GAU3FyX3).

* These bboxes provide actors' location in the frame, and through the level of intersection (a flavor of IoU) of these bboxes we get a sense of how close they are to each other (closeness) and predict if an interaction is occuring.

* The interactions for a therapy session generate quantitative results like:
  * How many times happend a certain interaction.
  * Duration of the interactions.
  * The total time of interactions (also minimun, maximum and mean time).

### App
Currently we use the [Streamlit](https://github.com/streamlit/streamlit) Framework to glue together our detections and processings, our database in [SQLite](https://www.sqlite.org/index.html) and our CRUD operations. With Streamlit's easy to use aproach you can quicly spin up your own local server and render your app.

### Trained models
We trained several YOLOv5 models in our sibling repo [therapy-aid-nn](https://github.com/solisoares/therapy-aid-nn). You can find the models and a sample video in the [v1.0.0](https://github.com/solisoares/therapy-aid-nn/releases/tag/v1.0.0) release.  The default for this app is the small model on a 256x256 image size.  

<br>

## App Overview
When the user uploads a video of a therapy session, YOLO do its magic and we generate statistical reports and a timeline of interactions in a "YouTube" style. Then the user can add the processed session to the database by providing a patient name and date. With more than one session added into the database for a patient, reports of progress are made.

<p align="center">
    <img src="https://user-images.githubusercontent.com/77312190/206078639-9248b569-7428-4120-b3d4-4e5262e18b92.png" height="200"/>
    <img src="https://user-images.githubusercontent.com/77312190/206079704-660a3095-0835-4dc2-b9bd-0ef4edb67715.png" height="200"/>
    <img src="https://user-images.githubusercontent.com/77312190/206078671-da1b3a26-5fdc-4ee5-9215-b3437a14c5d1.png" width="585"/>
</p>
<br>

## Getting Started
You're gonna need [Python](https://www.python.org/) (3.8 or higher), [Pip](), [Git](https://git-scm.com/) (if you're gonna clone the repo) and a `Web Browser`.
> :zap: To perform detection tasks we recommend a GPU with more than 4Gb VRAM

### Installation
Clone this repo (or download the zip file):</br>
```bash
git clone https://github.com/solisoares/therapy-aid-tool.git
```

Then install requirements:</br>
```bash
cd therapy-aid-tool
pip install -e .  # or `pip install -r requirements.txt`
```

### Default Usage
This will run the app with the small YOLO model that can be used with a decent cpu.
```bash
streamlit run 👋_Welcome.py
```
> :zap: The first time you make a detection in the app, it will try to download the specified weights in the `detect.cfg` file from the `therapy-aid-nn` v1.0.0 release.

This will start a local `Streamlit` server and the app will open in a new tab in your default web browser (we recommend Chromium based browsers).

### Custom Usage
To change which YOLOv5 model and image size you want to make detections with, adjust the `detect.cfg` file accordingly.  
  
This file specifies the location of the model weights and the image size (it's recommended that the size is the same one YOLO was trained). You can generate new weights for your dataset or use the ones in the therapy-aid-nn v1.0.0 release (they are commented in the detect.cfg file)
  
In short, do this:

1. Put *your* weights in a folder of your choice (our pre trained models are [here](https://github.com/solisoares/therapy-aid-nn/releases/tag/v1.0.0))
2. In the `therapy_aid_tool/detect.cfg` set:

    ```bash
    [yolov5]
    weights=<your-weights-path>
    [model]
    size=<img-size>
    ```
