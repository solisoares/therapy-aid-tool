from pathlib import Path
import subprocess
import shutil
from configparser import ConfigParser

import cv2
import yaml
from tqdm import tqdm
import pandas as pd
import numpy as np

from therapy_aid_tool.models._video_inference import (load_model, ROOT, MODELS_DIR, YOLO_VERSION)

def generate_test_images(dataset_path:Path, model_name:str):
    """
    Generate images with detected and ground truth bounding boxes, for the images from the test dataset.
    The images are saved in the model's folder.

    Args:
        dataset_path (Path): The path of the dataset to used in finetuning.
        model_name (str): The name of the finetuned model, that identifies the model in the app.
    """

    imgs_path = dataset_path / "test" / "images"
    labels_path = dataset_path / "test" / "labels"

    # Creates folders to save test images with bounding boxes
    test_imgs_bboxes_path = MODELS_DIR / model_name / "test_imgs"
    if not test_imgs_bboxes_path.exists():
        test_imgs_bboxes_path.mkdir()
    ground_truth_bboxes_path = test_imgs_bboxes_path / "ground_truth"
    if not ground_truth_bboxes_path.exists():
        ground_truth_bboxes_path.mkdir()
    detected_bboxes_path = test_imgs_bboxes_path / "detected"
    if not detected_bboxes_path.exists():
        detected_bboxes_path.mkdir()

    # Loads class names
    yaml_path = dataset_path / "data.yaml"
    class_names = []
    with open(yaml_path) as file:
        configs = yaml.safe_load(file)
        names = configs['names']
        class_names = dict(zip(range(len(names)), names))

    # Loads the model to be used
    model, model_size = load_model(model_name)

    # Gets the extension of the images
    img_path_split = (str)(list(imgs_path.rglob("*"))[0].name).split(".")
    images_ext = img_path_split[len(img_path_split)-1] # The extension of the images in the test dataset
    
    color = dict(zip(range(6), [(36,255,12),(243,22,1),(1,9,196),(247,1,233),(139,1,239),(59,253,254)]))
    # Draws bounding boxes on the images and saves them
    for image_path in tqdm(list(imgs_path.rglob("*")), desc="Generating test images"):
        img_rect = cv2.imread(image_path)
        # DETECTED BOUNDING BOXES
        results = model(img_rect, size=model_size) # Detect
        df_results = results.pandas().xyxy[0]
        for i in range(len(df_results)): # Access each of the bounding boxes
            xmin = (int)(df_results['xmin'][i])
            ymin = (int)(df_results['ymin'][i])
            xmax = (int)(df_results['xmax'][i])
            ymax = (int)(df_results['ymax'][i])
            class_id = df_results['class'][i]
            class_name = df_results['name'][i]
            # Draws bounding box
            img_rect = cv2.rectangle(img_rect, (xmin, ymin), (xmax, ymax), color[class_id], 2)
            text = class_name + " " + (str)(f'{df_results["confidence"][i].item():.2f}')
            img_rect = cv2.putText(img_rect, text, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color[class_id], 2)
        # Saves image
        img_rect_path = detected_bboxes_path / image_path.name
        cv2.imwrite(img_rect_path, img_rect)

        # GROUND TRUTH BOUNDING BOXES
        label_filename = labels_path / (image_path.name[:-(len(images_ext)+1)]+".txt")
        img_rect = cv2.imread(image_path)
        img_height, img_width = img_rect.shape[:2]
        with open(label_filename, 'r') as file: # Read labels from txt
            for line in file.readlines(): # Access each of the bounding boxes
                class_id, x, y, w, h = line.split(' ')
                class_id = (int)(class_id)
                x = (float)(x)
                y = (float)(y)
                w = (float)(w)
                h = (float)(h)
                xmin = (int)((x - (w/2)) * img_width)
                ymin = (int)((y - (h/2)) * img_height)
                xmax = (int)((x + (w/2)) * img_width)
                ymax = (int)((y + (h/2)) * img_height)
                # Draws bounding box
                img_rect = cv2.rectangle(img_rect, (xmin, ymin), (xmax, ymax), color[class_id], 2) 
                text = class_names[class_id]
                img_rect = cv2.putText(img_rect, text, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color[class_id], 2)
        # Saves image
        img_rect_path = ground_truth_bboxes_path / image_path.name
        cv2.imwrite(img_rect_path, img_rect)

def save_metrics_best_last(model_name:str):
    """
    Saves the training metrics of results.csv for the best and the last models generated.

    Args:
        model_name (str): The name of the finetuned model, that identifies the model in the app.
    """
    model_path = MODELS_DIR / model_name
    df_metrics = pd.read_csv(model_path / "results.csv")
    best_fitness = -1
    df_best = pd.DataFrame()
    weights = np.array([0.0, 0.0, 0.1, 0.9])  # weights for [P, R, mAP@0.5, mAP@0.5:0.95] to calculate fitness in YOLOv5
    for i in range(len(df_metrics)):
        precision = df_metrics[df_metrics.columns[4]][i]
        recall = df_metrics[df_metrics.columns[5]][i]
        map_05 = df_metrics[df_metrics.columns[6]][i]
        map_05_095 = df_metrics[df_metrics.columns[7]][i]
        fitness = (weights * np.array([precision, recall, map_05, map_05_095])).sum()
        if fitness > best_fitness:
            best_fitness = fitness
            df_best = df_metrics.iloc[i].squeeze()
    
    df_best.to_csv(model_path / "best_metrics.csv")

    df_last = df_metrics.loc[len(df_metrics)-1].squeeze()
    df_last.to_csv(model_path / "last_metrics.csv")

# TODO: To use only PyTorch (configuring the network architecture) to train YOLO
def finetune_yolo_model(dataset_path:Path, project_name:str, image_size:int=256, num_epochs:int=100, batch_size:int=1, base_model_name:str="yolov5m.pt") -> (bool,str):
    """Finetune a YOLOv5 model.

    Assumes that the dataset folder has the following format:\n
    data.yaml\n
    train\n
        images\n
        labels\n
    valid\n
        images\n
        labels\n
    test\n
        images\n
        labels\n

    Args:
        dataset_path (Path): The path of the dataset to be used in finetuning.
        project_name (str): The name of the finetuned model, that identifies the model in the app.
        image_size (int, optional): Size of the image to be used in finetuning.
        num_epochs (int, optional): Number of epochs to be used in finetuning.
        batch_size (int, optional): Size of the batch to be used in finetuning.
        base_model_name (str, optional): The YOLOv5 base model to be finetuned (i.e. yolov5m.pt, yolov5s.pt, yolov5m.pt, yolov5l.pt or yolov5x.pt).

    Returns:
        bool: True if the finetuning was a success.
        str: If finetuning was not successfull, a non-empty warning message with the error occurred.
    """
    
    # Update the path of the dataset in data.yaml to its current folder
    path_yaml_old = Path(dataset_path) / "data_old.yaml"
    path_yaml = Path(dataset_path) / "data.yaml"
    path_yaml.rename(path_yaml_old)
    old = open(path_yaml_old,'r')
    new = open(path_yaml,'w')
    for line in old:
        new_line = line
        contents = line.split(' ')
        label = contents[0]
        if label == "path:":
            new_line = label+" "+(str)(dataset_path)+"\n"
        new.write(new_line)
    old.close()
    new.close()
    path_yaml_old.unlink()

    # Download YOLOv5's repository if its folder does not exists already
    path = Path(__file__).resolve().parents[2] / "yolov5"
    if not path.exists():
        subprocess.run("cd "+(str)(Path(__file__).parent)+"; git clone https://github.com/ultralytics/yolov5", shell=True)
        path_src = Path(__file__).resolve().parent / "yolov5"
        path_dest = Path(__file__).resolve().parents[2]
        shutil.move(path_src, path_dest)
        subprocess.run("cd "+(str)(path)+"; git checkout -q tags/"+YOLO_VERSION, shell=True)
        subprocess.run("cd "+(str)(path)+"; pip3 install -r requirements.txt", shell=True)
        if not path.exists:
            return (False, "Error in cloning YOLOv5's repository.")
    
    # Clean the folder with previous trainings by YOLO
    path = ROOT / "yolov5" / "runs"
    if path.exists():
        path = path / "train"
        if path.exists():
            shutil.rmtree(path)

    # Execute the YOLO training with the parameters selected by the user
    path_yolov5 = ROOT / "yolov5"
    subprocess.run("cd "+(str)(path_yolov5)+"; python3 train.py --img "+(str)(image_size)+\
                                                        " --epochs "+(str)(num_epochs)+\
                                                        " --batch "+(str)(batch_size)+\
                                                        " --weights "+base_model_name+\
                                                        " --name "+project_name+\
                                                        " --data "+(str)(dataset_path)+"/data.yaml", shell=True)

    # Moves the trained model to the models folder
    path_src = path_yolov5 / "runs" / "train" / (str)(project_name)
    path_dest = MODELS_DIR / (str)(project_name)
    shutil.move(path_src, path_dest)

    # Creates a config file with the size of the images used in finetuning
    configs = ConfigParser()
    configs["model"] = {"size": (str)(image_size)}
    with open(path_dest / "model_configs.cfg", 'w') as file:
        configs.write(file)

    # Generates and saves images with detected and ground truth bounding boxes for comparison
    generate_test_images(dataset_path, project_name)

    # Saves the training metrics of results.csv for the best and the last models generated.
    save_metrics_best_last(project_name)
    
    return (True,"")