import streamlit as st
from pathlib import Path

# TODO: avoid using any Model or DAO in the View
from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    DATABASE,
)

PATH_TUT_IMGS = Path(__file__).parents[1] / "tutorial_images"

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Train your model"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="⚙️")

st.title(TITLE)
st.markdown(
    """
    This module provides an easy way of training your own model to analyze a video of a \
    therapy session with PlusMe and check statistics of performance for the model trained. \
    Learn more about how to use it in the following subsections.
    """)

st.markdown(
    """
    #### Downloading dataset from Labelbox

    To be able to train your own model, first you need a dataset. To load a dataset you can import it \
    (see "Import existing dataset") or, if you labeled your images using Labelbox, download it directly \
    from the app (recommended).

    In "Download dataset from Labelbox" the following parameters need to be provided:\n
    - **Dataset name:** An unique name to call your dataset.\n
    - **Labelbox API key**\n
    - **Project ID:** The ID of the Labelbox project that contains the images and labels to download.\n
    - Percentage of the dataset destined to **training**, **validation** and **test**.

    To generate a Labelbox API key, access your account on Labelbox and click on the account button → Workspace settings
    """)

st.image((str)(PATH_TUT_IMGS / "1.png"), use_column_width="always")

st.markdown(
    """
    In the page opened, access the API tab and generate the key by clicking on the "New API key" button.
    """)

st.image((str)(PATH_TUT_IMGS / "5.png"))

st.markdown(
    """
    To get the project ID, access the project of interest on Labelbox and copy the ID from the URL, \
    after "projects/" and spanning until the next "/" in the URL.
    """)

st.image((str)(PATH_TUT_IMGS / "10.png"), use_column_width="always")

st.markdown(
    """
    **NOTE:** In the current version of the app, only three labels are supported in the video analysis: \
    "toddler", "caretaker", and "plusme". Please, pay attention to only using these labels.
    """)

st.markdown(
    """
    #### Importing existing dataset

    To import an existing dataset, simply drag and drop a ZIP file containing the dataset in the format specified below:

    ```
    mydataset
        ├── data.yaml
        ├──train
            ├── images
            └── labels
        ├── valid
            ├── images
            └── labels
        └── test
            ├──images
            └──labels
    ```
    
    As shown in the example below, the data.yaml file must contain the path to the dataset, the paths inside \
    the dataset folder for the training, validation, and test images, the number of classes of labels, and the \
    names of the labels.

    ```
    data.yaml
    path: /home/user/Documents/mydataset
    train: train/images
    val: valid/images
    test: test/images
    nc: 3
    names: ['toddler','caretaker','plusme']
    ```
    
    The label file for each image must have the same name of the image, but with .txt extension, and must respect \
    the YOLOv5 format for this type of file. For more information, see the [YOLOv5 Docs](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/).

    **NOTE:** In the current version of the app, only three labels are supported in the video analysis: "toddler", \
    "caretaker", and "plusme". Please, pay attention to only using these labels.
    """)

st.markdown(
    """
    #### Training your model

    With a dataset already loaded in the app, we can finetune YOLOv5 base models to identify our objects of \
    interest (toddler, caretaker and PlusMe). To do so, in section "Train", select the dataset you desire to use \
    and type a name for your model.
    """
    )

st.image((str)(PATH_TUT_IMGS / "12.png"))

st.markdown(
    """
    Optionally, you can also improve your model by controlling some of the YOLOv5 parameters used in finetuning, \
    available at "Advanced settings" expander. For more information on these specifications, see the [YOLOv5 Docs](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/).
    """
    )

st.image((str)(PATH_TUT_IMGS / "13.png"))

st.markdown(
    """
    After configuring these parameters, you can train your model by clicking on the "Train" button and monitor \
    the training by the same terminal used to open the Therapy Aid Tool app.
    """
    )

st.markdown(
    """
    #### Model statistics

    In Therapy Aid Tool, after training your model, you have access to its statistics. They are separated into \
    three sections: "Model's overall performance", "Model's test performance", and "Label information".

    ##### Model's overall performance

    This page shows graphs generated during YOLOv5 training process that are important to evaluate the overall \
    performance of the model. The first one is a confusion matrix similar to the one shown below, that shows the \
    relation between the ground truth class of labels in the validation set and the labels predicted for them. In \
    the image below, for example, of all the bounding boxes classified as "toddler" in the validation set, 0.87% \
    of them were correctly predicted and 0.13% were wrongly predicted as "plusme" bounding boxes.
    """
    )

st.image((str)(PATH_TUT_IMGS / "15_confusion_matrix.png"))

st.markdown(
    """
    The next two are curves relating the precision and recall values, respectively, with different values of \
    confidence tested. Here, confidence related with confidence score of Non-Maximum Suppression (NMS) step executed \
    during detection of objects in an image. For a comprehensive explanation on NMS, access \
    [this tutorial](https://kikaben.com/object-detection-non-maximum-suppression/).

    Observe that as the value of precision increases, the value of recall decreases, and vice versa. This can be \
    observed in practice on the graphs above.
    """
    )

st.image((str)(PATH_TUT_IMGS / "20_P_curve.png"))
st.image((str)(PATH_TUT_IMGS / "25_R_curve.png"))

st.markdown(
    """
    As precision and recall depend on confidence, to compare both we need to fix a value for confidence. To do \
    it we use the F1 score, that combine precision and recall. The graph for such a metric is the next one shown \
    in the app. An example can be observed below.
    """
    )

st.image((str)(PATH_TUT_IMGS / "30_F1_curve.png"))

st.markdown(
    """
    Observe that the best of F1, as indicated in the subtitle, is 0.69, reached at 0.551 confidence. So, for the \
    next graph, that compares values of precision and recall, the value of confidence considered was 0.551.
    """
    )

st.image((str)(PATH_TUT_IMGS / "35_PR_curve.png"))

st.markdown(
    """
    The last graphs show the evolution through epochs for box, object, and class loss values with the training \
    and validation datasets, as well as precision, recall, mAP@0.5 and mAP@0.5:0.95.
    """
    )

st.image((str)(PATH_TUT_IMGS / "40_results.png"))

st.markdown(
    """
    ##### Model's test performance

    This section shows, in parallel, the bounding boxes detected by the trained model on images from the test \
    dataset passed during training of such a model and the ground truth bounding boxes for the same images, providing \
    information to understand how the training dataset can be improved. You can choose a model and navigate through \
    the dataset by a sliding bar or by the arrows right after it. 
    """
    )

st.image((str)(PATH_TUT_IMGS / "43.png"))

st.markdown(
    """
    ##### Label information

    This page shows graphs generated by YOLOv5 that summarize information about the bounding boxes of the training \
    dataset that can be useful for improving such a set. The first one presents the amount of bounding boxes for each \
    of the classes considered during labeling. The second figure summarizes the normalized sizes of each of these same \
    bounding boxes. 
    """
    )

container1 = st.container()
col_container1 = container1.columns(2)
col_container1[0].image((str)(PATH_TUT_IMGS / "45_labels.png"))
col_container1[1].image((str)(PATH_TUT_IMGS / "46_labels.png"))

st.markdown(
    """
    The information of the normalized bounding boxes size (width and height) and their normalized center localization \
    (x and y) is also summarized by the two heatmaps below.
    """
    )

container2 = st.container()
col_container2 = container2.columns(2)
col_container2[0].image((str)(PATH_TUT_IMGS / "47_labels.png"))
col_container2[1].image((str)(PATH_TUT_IMGS / "48_labels.png"))

st.markdown(
    """
    The last graphs show the distribution of normalized values for x, y, width, and height, separately. This can be \
    observed by the barplots above each of these features. Using the image below as an example, we can observe that \
    the values of y (in the second barplot from left to right) are more concentrated between 0.25 and 0.75.

    The heatmaps of the same image present the values of pairs of these features that appear more frequently in the \
    training dataset. For example, in the bottom right corner heatmap of the image below, it is possible to observe \
    that bounding boxes with smaller width commonly have also smaller height, and bounding boxes with bigger width \
    also have bigger height.
    """
    )

st.image((str)(PATH_TUT_IMGS / "50_labels_correlogram.jpg"))

st.markdown(
    """
    #### Exporting your model

    To export a model, in the "Export model" section of the app, simply choose the model you want to export and \
    click on the "Export" button. A ZIP file with model weights, statistics, size and other training information \
    will be generated and saved to the Therapy Aid Tool app directory.
    """
    )

st.image((str)(PATH_TUT_IMGS / "55.png"))
