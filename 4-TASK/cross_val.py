import numpy as np
from collections import defaultdict


def kfold_split(num_objects, num_folds):
    """Split [0, 1, ..., num_objects - 1] into equal num_folds folds (last fold can be longer) and returns num_folds train-val
       pairs of indexes.

    Parameters:
    num_objects (int): number of objects in train set
    num_folds (int): number of folds for cross-validation split

    Returns:
    list((tuple(np.array, np.array))): list of length num_folds, where i-th element of list contains tuple of 2 numpy arrays,
                                       the 1st numpy array contains all indexes without i-th fold while the 2nd one contains
                                       i-th fold
    """
    index = np.arange(num_objects)
    lenArr = num_objects // num_folds
    result = []
    for arr_1_index in range(num_folds):
        arr_1_start = lenArr * arr_1_index
        if arr_1_index != num_folds - 1:
            arr_1_end = lenArr * (arr_1_index + 1)
        else:
            arr_1_end = len(index)
        arr_1 = index[arr_1_start:arr_1_end]
        arr_2 = [*index[0:arr_1_start], *index[arr_1_end:]]

        result.append((arr_2, arr_1))

    return result
    return folds


def knn_cv_score(X: np.array, y: np.array, parameters: dict, score_function, folds: list, knn_class: type) -> dict:
    answer = {}
    for normalizer in parameters['normalizers']:
        for n_neighbor in parameters['n_neighbors']:
            for metric in parameters['metrics']:
                for weight in parameters['weights']:
                    scores = []
                    for fold in folds:
                        score = 0

                        X_train = X[fold[0]]
                        y_train = y[fold[0]]

                        X_test = X[fold[1]]
                        y_test = y[fold[1]]

                        params = {'n_neighbors': n_neighbor, 'metric': metric, 'weights': weight}

                        if normalizer[0] is not None:
                            normalizer[0].fit(X_train)
                            X_train = normalizer[0].transform(X_train)
                            X_test = normalizer[0].transform(X_test)

                        model = knn_class(**params)
                        model.fit(X_train, y_train)
                        preds = model.predict(X_test)
                        score = score_function(y_test, preds)

                        scores.append(score)

                    answer[(
                        (normalizer[1],
                         n_neighbor,
                         metric,
                         weight
                         )
                    )] = np.mean(scores)

    return (answer)
