import pandas as pd
#pip install -U scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import DBSCAN
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors


data = pd.read_csv("https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")
plot = data.plot.scatter(x='sepal_length', y='sepal_width')

dbscan = DBSCAN()
model = DBSCAN(eps = 0.4, min_samples = 10).fit(data)
dbscan.fit(data[['sepal_length', 'sepal_width']])
colors = model.labels_
plt.scatter(data["sepal_length"], data["sepal_width"], c = colors)
plt.show()


neigh = NearestNeighbors(n_neighbors=2)
nbrs = neigh.fit(data[['sepal_length', 'sepal_width']])
distances, indices = nbrs.kneighbors(data[['sepal_length', 'sepal_width']])


























#on doit d'abord créer un fichier json avec les données d'entrainement
# à faire 
# data = pd.read_json('')

# features = data[['frequency', 'temperature', 'humidity']]
# target = data['réponse']

# x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
# model = LinearRegression()
# model.fit(x_train, y_train)
# predictions = model.predict(x_test)

# erreur = mean_squared_error(y_test, predictions)
# print(f"Erreur: {erreur}")



# #entrer les valeurs du son à prédire

# input_string = input("Entrez les nouvelles fréquences séparéespar un espace: ")
# new_frequences  = input_string.split()
# temperature = input("Entrez la nouvelle température: ")
# new_temperature = []
# for i in new_frequences:
#     new_temperature.append(temperature)
# humidity = input("Entrez la nouvelle humidité: ")
# new_humidity = []
# for i in new_frequences:
#     new_humidity.append(humidity)



# new_sound = pd.DataFrame({
#     'frequency': new_frequences,  
#     'temperature': new_temperature,  # Température constante
#     'humidity': new_humidity  # Humidité constante
# })


# predicted_response = model.predict(new_sound)
# print(predicted_response)