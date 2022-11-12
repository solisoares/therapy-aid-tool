from __future__ import annotations

from collections import defaultdict
from itertools import groupby

from therapy_aid_tool.models._video_inference import (
    load_model,
    preds_from_torch_results,
    MODEL_SIZE,
    BBox,
)

import cv2


class VideoBuilder:
    """Builder for the Video class

    Builds a Video instance containing the three main metrics for a Video
    (closeness, interactions and statistics about interactions), by extracting
    information about what is happening in each frame with the associated 
    bounding boxes for each class.
    """

    n_classes: int = 3
    CLOSENESS_THRESHOLD: float = 0.6

    def __init__(self, filepath: str) -> None:
        self.__fp = filepath
        self.__cap = cv2.VideoCapture(self.__fp)
        self.__total_frames = int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__fps = float(self.__cap.get(cv2.CAP_PROP_FPS))
        # Long initialization
        self.__bbs = self.__bboxes()
        self.__clos = self.__closeness()
        self.__inter = self.__interactions()
        self.__stat = self.__interactions_statistics(self.__inter)

    def __bboxes(self):
        """Return present bounding boxes for each frame

        The output is stored in a dictionary (defaultdict) with the
        keys being the actual classes of detection available, for
        now there are 3 classes (actors): toddler, caretaker and plusme

        Each bounding box, being a instance of a BBox, can be used to
        extract its coordinates and other parameters to detect how
        close actors are. It can be used also to detect if there are
        interactions happening, or to plot rectangular regions if desired.

        Returns:
            defaultdict: Bounding boxes for each frame. The keys are the
                classes and the values are arrays/lists contaning a BBox
                instance for that class key in that frame index.

                Return example: {
                    'td': [BBox0, BBox1, ...],
                    'ct': [BBox0, BBox1, ...],
                    'pm': [BBox0, BBox1, ...],
                    }
        """
        model = load_model()
        bbs = defaultdict(list)

        for i in range(self.__total_frames):
            _, frame = self.__cap.read()
            inference = model(frame[:, :, ::-1], size=MODEL_SIZE)
            preds = preds_from_torch_results(inference,
                                             self.n_classes)  # returns three preds

            bbs["td"].append(BBox(preds[0]))
            bbs["ct"].append(BBox(preds[1]))
            bbs["pm"].append(BBox(preds[2]))

        return bbs

    def __closeness(self):
        """Return how close actors' bounding box pairs are based on NIoU for each frame

        To measure how close two different objects are based on their bounding boxes we
        can use the Normalized Intersection over Union.

        This metric is measured for each pair of actors relation for each frame and
        return in form of a dictionary.

        This results can generate a "YouTube" like bar of "best" moments, or in our case,
        moments of closeness.

        Returns:
            defaultdict: How much close are the three main actors for each frame.
                The keys are the three relation classes available and the values
                are arrays/lists containing a float between 0~1 for that class key
                in that frame index

                Return example: {
                    'td_ct': [NIoU0(td, ct), NIoU1(td, ct), ...],
                    'td_pm': [NIoU0(td, pm), NIoU1(td, pm), ...],
                    'ct_pm': [NIoU0(ct, pm), NIoU1(ct, pm), ...]
                    }
        """
        closeness = defaultdict(list)
        bbs = self.__bbs

        for idx in range(self.__total_frames):
            closeness["td_ct"].append(bbs["td"][idx].niou(bbs["ct"][idx]))
            closeness["td_pm"].append(bbs["td"][idx].niou(bbs["pm"][idx]))
            closeness["ct_pm"].append(bbs["ct"][idx].niou(bbs["pm"][idx]))

        return closeness

    def __interactions(self):
        """Return whether or not there is an interaction present for each frame

        The interaction is predicted if the closeness is greater than a threshold
        Thus, the interaction is actually a prediction of interaction since we use
        a threshold of the closeness.
            Interaction: True if closeness > threshold, False otherwise
        
        Interaction indicates that one actors is engaging in physical touch
        with another. Like the toddler touching the plusme teddy bear or the caretaker
        showing the toddler how to play with the teddy bear.
        
        For each frame, return a Bool indicating if there is that respective interaction,
        making an array of bools for one interaction class

        Returns:
            defaultdict: The interactions for each frame.
                The keys are the three relation classes available and the values
                are arrays/lists containing a Bool for that class key in that frame index

                Return example: {
                    'td_ct': [Bool, Bool, ...],
                    'td_pm': [Bool, Bool, ...],
                    'ct_pm': [Bool, Bool, ...]
                    }
        """
        interactions = defaultdict(list)
        bbs = self.__bbs
        closeness = self.__clos

        for idx in range(self.__total_frames):
            interactions["td_ct"].append(
                True if (closeness["td_ct"][idx] >
                         self.CLOSENESS_THRESHOLD) else False
            )
            interactions["td_pm"].append(
                True if (closeness["td_pm"][idx] >
                         self.CLOSENESS_THRESHOLD) else False
            )
            interactions["ct_pm"].append(
                True if (closeness["ct_pm"][idx] >
                         self.CLOSENESS_THRESHOLD) else False
            )

        return interactions

    def __interactions_statistics(self, interactions: dict):
        """Return statistics for interactions in the video

        Args:
            interactions (dict): The interactions for each frame.
                The keys are the three relation classes available and the values
                are arrays/lists containing a Bool for that class key in that frame index

        Returns:
            dict: Statistics for all the interactions instances that happened in the video
                It can be used in a pandas.DataFrame to output a chart view.

                Return example: {
                    'td_ct': {n_interactions: int', total_time: float, ...},
                    'td_pm': {n_interactions: int', total_time: float, ...},
                    'ct_pm': {n_interactions: int', total_time: float, ...}
                }
        """
        frame_time = 1 / self.__fps  # time one frame takes to run

        data_template = {
            "n_interactions": int,
            "total_time": float,
            "min_time": float,
            "max_time": float,
            "mean_time": float,
        }
        statistics = {
            "td_ct": data_template.copy(),
            "td_pm": data_template.copy(),
            "ct_pm": data_template.copy(),
        }

        for key, interaction in interactions.items():
            # Groups of interaction and non interactions (1s and 0s)
            groups = groupby(interaction)

            # Generate metrics for interaction
            groups_of_interaction = []  # the chunks of 1s
            idxs = []  # start and end indexes of each chunk
            count = 0  # auxiliary to get indexes
            for k, group in groups:
                group = list(group)
                count += len(group)
                if k == 1:
                    idx1 = count - len(group)
                    idx2 = count
                    idxs.append((idx1, idx2))
                    groups_of_interaction.append(group)

            if groups_of_interaction:
                n_interactions = len(groups_of_interaction)
                total_time = interaction.count(1) * frame_time
                mean_time = total_time / len(groups_of_interaction)
                max_time = len(max(groups_of_interaction)) * frame_time
                min_time = len(min(groups_of_interaction)) * frame_time
            else:
                (n_interactions, total_time,
                 mean_time, max_time, min_time) = (None, None, None, None, None,)

            statistics[key]["n_interactions"] = n_interactions
            statistics[key]["total_time"] = total_time
            statistics[key]["min_time"] = min_time
            statistics[key]["max_time"] = max_time
            statistics[key]["mean_time"] = mean_time

        return statistics

    def build(self):
        return Video(self.__fp, self.__clos, self.__inter, self.__stat)


class Video:
    def __init__(self, filepath, closeness, interactions, interactions_statistics) -> None:
        self.filepath = filepath
        self.closeness = closeness
        self.interactions = interactions
        self.interactions_statistics = interactions_statistics

    def __repr__(self):
        return f"Video(filepath='{self.filepath}', closeness='{self.closeness}', interactions='{self.interactions}', interactions_statistics='{self.interactions_statistics}')"
