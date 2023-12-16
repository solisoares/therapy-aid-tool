<h1 align="center">Therapy Aid Tool</h1>
 
<h3 align="center">A Web App to aid in clinical and therapeutic decisions reducing analysis time for therapists</h3>

<p align="center">(The current version of this project aims to assist in decision making of Autism Spectrum Disorder (ASD) video sessions)</p>
<br>

# Table of Contents
* [How this app can help in treatment?](#how-can-help)
* [Publications](#pubs)
* [Quick demonstration video](#demo)
* [Current technologies and heuristics used](#techs)
* [App Overview](#overview)
* [Getting Started](#starting)
  * [Firefox Issue :warning:](#firefox-issue)
  * [Installation](#install)
  * [Default Usage](#default-usage)
  * [Custom Usage](#custom-usage)
 

<br>

<a name="how-can-help"></a>
## :thought_balloon: How this app can help in treatment?
The main goal is to provide a web aplication that is capable of filtering out relevant scenes of recorded therapy sessions to assist professionals in their analysis. With the use of Artificial Inteligence and Computer Vision this app is capable of:

* Handle large amounts of therapy session videos, storing and retrieving them as needed.<br>
    > :zap: Quickly store and access sessions with patient name and date.
* Filter relevant scenes according to medical professionals.
    * Point exactly in time where is happening an event of interest in the video. <br>
      > :zap: YouTube-like timeline of interactions
      
    * Reduce time for analysis of a whole video. <br>
      > :zap: In this test set we got an analysis time reduction from 9% to 90%. <br>
      > :zap: It means that a 60min therapy session can be converted to a 54min to 6min of manual analysis. <br>
      > :zap: This can be achieved by balancing Precision x Recall through the changing of internal configurations. <br>
      
* Assistance in clinical and therapeutic decisions throughout interactive search and statistical reports.
    * Summary of interactions in each session.
    * Progress of interactions for all sessions. <br> <br>
      > :zap: Getting sense of the patient's progress through interactions can aid in decision making.
<br>

<a name="pubs"></a>
## 📰 Publications
* Publication 1 (BRACIS Paper - Springer): [Event Detection in Therapy Sessions for Children with Autism](https://link.springer.com/chapter/10.1007/978-3-031-21689-3_17) <br>
* Publication 2 (Computer on the Beach Periodical - Free/Open): [Event detection in therapy sessions for children with Autism](https://periodicos.univali.br/index.php/acotb/article/view/19507/11309) <br>
* Undergrad Thesis (Free/Open - pt-br): [A Tool to aid Autism Spectrum Disorder therapies using Machine Learning](https://repositorio.ufsc.br/bitstream/handle/123456789/248134/tcc-alexandre-soli-soares.pdf)
<br>

<a name="demo"></a>
## ▶️ Quick demonstration video
> https://www.youtube.com/watch?v=S3w9jncUsQc
<br>

<a name="techs"></a>
## 📝 Current technologies and heuristics used

### Core
* For the task of object detection we use a [YOLOv5](https://github.com/ultralytics/yolov5) trained deep learning model. YOLO detects where the main actors of a therapy session are by generating bounding boxes (bboxes) around each one of them. For this **current version**, the main actors of a **ASD therapy session** are the *Toddler*, *Caretaker* and the interactive teddy bear called [*PlusMe*](https://dl.acm.org/doi/pdf/10.1145/3491101.3519716?casa_token=iWYoiTNsB90AAAAA:x8TOj1oPpZoqyLTIV3FUw1yAIFTEnD_roG12wpDYmsIsg6JVSIjzj4whC2ky2Pj7oSv4GAU3FyX3).

* These bboxes provide actors' location in the frame, and through the level of intersection (a flavor of IoU) of these bboxes we get a sense of how close they are to each other (closeness) and predict if an interaction is occuring.

* The interactions for a therapy session generate quantitative results like:
  * How many times happend a certain interaction.
  * Duration of the interactions.
  * The total time of interactions (also minimun, maximum and mean time).

### App
Currently we use the [Streamlit](https://github.com/streamlit/streamlit) Framework to glue together this detections and processings, this database in [SQLite](https://www.sqlite.org/index.html) and this CRUD operations. With Streamlit's easy to use aproach you can quicly spin up your own local server and render your app.

### Trained models
We trained several YOLOv5 models in our sibling repo [therapy-aid-nn](https://github.com/solisoares/therapy-aid-nn). You can find the models and a sample video in the [v1.0.0](https://github.com/solisoares/therapy-aid-nn/releases/tag/v1.0.0) release.  The default for this app is the small model on a 256x256 image size.  

<br>

<a name="overview"></a>
## :mag_right: App Overview
When the user uploads a video of a therapy session, YOLO do its magic and we generate statistical reports and a timeline of interactions in a "YouTube" style. Then the user can add the processed session to the database by providing a patient name and date. With more than one session added into the database for a patient, reports of progress are made.

<p align="center">
    <img src="https://user-images.githubusercontent.com/77312190/206078639-9248b569-7428-4120-b3d4-4e5262e18b92.png" height="200"/>
    <img src="https://user-images.githubusercontent.com/77312190/206079704-660a3095-0835-4dc2-b9bd-0ef4edb67715.png" height="200"/>
    <img src="https://user-images.githubusercontent.com/77312190/206078671-da1b3a26-5fdc-4ee5-9215-b3437a14c5d1.png" width="585"/>
</p>
<br>

<a name="starting"></a>
## 👋 Getting Started
You're gonna need [Python](https://www.python.org/) (3.8 or higher), [Pip](), [Git](https://git-scm.com/) (if you're gonna clone the repo) and a `Chromium-based Web Browser`.
<a name="firefox-issue"></a>
> :warning: Use Chromium-based browsers. In this v1.0.0, the timeline rendering occurs *bellow* the video playback, and not *inside* above the loading bar like YouTube does. Streamlit in Chromium-based browsers create the loading bar accross the whole video window, so the rendered timeline can be nicelly stretched. This is a visualization issue for Firefox for example, where the loading bar is just a section of the whole window lenght.

> :zap: To perform detection tasks we recommend a GPU with more than 4Gb VRAM

<a name="install"></a>
### Installation
Clone this repo (or download the zip file):</br>
```bash
git clone https://github.com/solisoares/therapy-aid-tool.git
```

Then install requirements:</br>
```bash
cd therapy-aid-tool
python -m venv venv
source venv/bin/activate
pip install -e .
```
<a name="default-usage"></a>
### Default Usage
This will run the app with the small YOLO model that can be used with a decent cpu.
```bash
streamlit run 👋_Welcome.py
```
> :zap: The first time you make a detection in the app, it will try to download the specified weights in the `detect.cfg` file from the `therapy-aid-nn` v1.0.0 release.

This will start a local `Streamlit` server and the app will open in a new tab in your default web browser (we recommend Chromium based browsers).

<a name="custom-usage"></a>
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
