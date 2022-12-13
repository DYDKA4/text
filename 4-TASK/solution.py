import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

with open('knn.pkl', 'rb') as f:
    knn = pickle.load(f)

with open('tf_idf.pkl', 'rb') as f:
    tf_idf = pickle.load(f)

with open('X.pkl', 'rb') as f:
    X = pickle.load(f)

with open('y.pkl', 'rb') as f:
    y = pickle.load(f)


class Solution:
    def __init__(self):
        self.counter = 0
        self.new_text = []
        self.new_y = []
        self.X = X
        self.y = y
        self.tf_idf = tf_idf
        self.knn = knn

    def predict(self, text: str) -> str:
        normalized_text = tf_idf.transform([text])
        predicted = self.knn.predict(normalized_text)[0]
        self.counter += 1
        self.new_text.append(text)
        self.new_y.append(predicted)
        if self.counter % 100 == 0:
            self.X = np.concatenate((self.X, np.array(self.new_text)))
            self.new_text = []
            self.y = np.concatenate((self.y, np.array(self.new_y)))
            self.new_y = []
            test = self.tf_idf.transform(self.X)
            self.knn = KNeighborsClassifier(metric='cosine', n_neighbors=1, weights='uniform')
            self.knn.fit(test, self.y)

        return str(predicted)
