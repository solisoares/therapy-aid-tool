from therapy_aid_tool.models.video import Video

closeness = {
    'td_ct': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    'td_pm': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    'ct_pm': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
}


interactions = {
    'td_ct': [True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, ],
    'td_pm': [True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, ],
    'ct_pm': [True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, ],
}


statistics = {
    'td_ct': {"n_interactions": 10, "total_time": 20, "min_time": 2, "max_time": 10, "mean_time": 7.5},
    'td_pm': {"n_interactions": 10, "total_time": 20, "min_time": 2, "max_time": 10, "mean_time": 7.5},
    'ct_pm': {"n_interactions": 10, "total_time": 20, "min_time": 2, "max_time": 10, "mean_time": 7.5},
}

_video = Video("xxx", closeness, interactions, statistics)