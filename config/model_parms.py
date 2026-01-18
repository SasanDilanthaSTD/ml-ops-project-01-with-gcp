from scipy.stats import randint, uniform

LIGHTGBM_PARAM = {
    'n_estimators' : randint(100, 1000),
    'max_depth' : randint(5, 50),
    'learning_rate' : uniform(0.01, 0.3),
    'num_leaves' : randint(20, 300),
    'boosting_type' : ['gbdt', 'dart', 'goss'],
}

RANDOM_SEAECH_PARAMS = {
    'n_iter' : 5,
    'cv' : 5,
    'verbose' : 2,
    'random_state' : 42,
    'n_jobs' : -1,
    'scoring' : 'accuracy'
}