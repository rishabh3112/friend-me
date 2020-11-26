from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report as rp
from sklearn.model_selection import train_test_split
from joblib import dump, load
import random
import numpy as np
import pandas as pd

# Age
age = []
for i in range(500):
    num = random.gauss(25, 3)
    num = int(num)
    age.append(num)

# Sports yes/no
sports = []
for i in range(500):
    sports.append(random.choice([0, 1]))

genre = ['action and adventure', 'comedy and drama',
         'horror', 'mystery and thriller']
movies = []
for i in range(500):
    movies.append(random.choice(genre))

# travel
travel = []
for i in range(500):
    travel.append(random.choice([0, 1]))


features = []
for i in range(500):
    features.append([age[i], movies[i], sports[i], travel[i]])

# Clustering
X = np.array(features)
df = pd.DataFrame(X, columns=['Age', 'Movie Genre',
                              'Sports Interest', 'Travel Interest'])
df_m = pd.get_dummies(df['Movie Genre'])
master = pd.concat([df, df_m], axis=1)

X = master.iloc[:, [0, 2, 3, 4, 5, 6, 7]].values

kmeans = KMeans(n_clusters=3, init='k-means++', random_state=0)
y_kmeans = kmeans.fit_predict(X)

A = [i for i in range(len(y_kmeans)) if y_kmeans[i] == 0]
B = [i for i in range(len(y_kmeans)) if y_kmeans[i] == 1]
C = [i for i in range(len(y_kmeans)) if y_kmeans[i] == 2]

group_dict = {0: 'A', 1: 'B', 2: 'C'}

mat = np.zeros((500, 1), 'int')
for j in B:
    mat[j] = 1
for k in C:
    mat[k] = 2

df['Group'] = mat

df['Group_label'] = df['Group'].map(group_dict)

# Classifier
x = master.iloc[:, [0, 2, 3, 4, 5, 6, 7]].values
y = df.iloc[:, 4].values

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(x_train, y_train)

dump(rfc, 'model.m')
