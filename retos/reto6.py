import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,roc_curve, auc
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
data = pd.read_csv("data/train.csv")

relevant_vars = ["CANAL","EDAD","DIASEM","HORA_AUX","DIAMES","FECHA","OFICINA_VIN","FECHA_VIN","Canal1","SEGMENTO"]
balanced_dataset = data[relevant_vars+["FRAUDE"]].dropna()


balanced_dataset.loc[balanced_dataset['CANAL'] == "ATM_INT", "CANAL"] = 100
balanced_dataset.loc[balanced_dataset['CANAL'] == "MCI", "CANAL"] = 200
balanced_dataset.loc[balanced_dataset['CANAL'] == "POS", "CANAL"] = 300

balanced_dataset.loc[balanced_dataset['Canal1'] == "ATM_INT", "Canal1"] = 100
balanced_dataset.loc[balanced_dataset['Canal1'] == "POS", "Canal1"] = 300

balanced_dataset.loc[balanced_dataset['SEGMENTO'] == "Preferencial", "SEGMENTO"] = 100
balanced_dataset.loc[balanced_dataset['SEGMENTO'] == "Personal Plus", "SEGMENTO"] = 200
balanced_dataset.loc[balanced_dataset['SEGMENTO'] == "Emprendedor", "SEGMENTO"] = 300
balanced_dataset.loc[balanced_dataset['SEGMENTO'] == "PYME", "SEGMENTO"] = 400
balanced_dataset.loc[balanced_dataset['SEGMENTO'] == "Personal", "SEGMENTO"] = 500
balanced_dataset.loc[balanced_dataset['SEGMENTO'] == "Empresarial", "SEGMENTO"] = 600

#balanced_dataset.loc[balanced_dataset['SEXO'] == "F", "SEXO"] = 0
#balanced_dataset.loc[balanced_dataset['SEXO'] == "M", "SEXO"] = 1
balanced_dataset["EDAD"] = balanced_dataset["EDAD"]*10
balanced_dataset["DIASEM"] = balanced_dataset["DIASEM"]*10
balanced_dataset["DIAMES"] = balanced_dataset["DIAMES"]*10
balanced_dataset["FECHA_VIN"] = balanced_dataset["FECHA_VIN"]//10000
balanced_dataset["HORA_AUX"] = balanced_dataset["HORA_AUX"]*10


X_train, X_test, y_train, y_test = train_test_split(balanced_dataset[relevant_vars],balanced_dataset["FRAUDE"],test_size=0.1)
knn_classifier = KNeighborsClassifier(n_neighbors=5,weights="distance",p=2,algorithm="brute")
knn_classifier.fit(X_train, y_train)
y_pred = knn_classifier.predict(X_test)
target = pd.read_csv("data/test.csv")

target.loc[target['CANAL'] == "ATM_INT", "CANAL"] = 100
target.loc[target['CANAL'] == "MCI", "CANAL"] = 200
target.loc[target['CANAL'] == "POS", "CANAL"] = 300

target["EDAD"] = target["EDAD"]*10
target["DIASEM"] = target["DIASEM"]*10
target["DIAMES"] = target["DIAMES"]*10
target["FECHA_VIN"] = target["FECHA_VIN"]//10000
target["HORA_AUX"] = target["HORA_AUX"]*10

target.loc[target['Canal1'] == "ATM_INT", "Canal1"] = 100
target.loc[target['Canal1'] == "POS", "Canal1"] = 300

#target.loc[target['SEXO'] == "F", "SEXO"] = 0
#target.loc[target['SEXO'] == "M", "SEXO"] = 1

target.loc[target['SEGMENTO'] == "Preferencial", "SEGMENTO"] = 100
target.loc[target['SEGMENTO'] == "Personal Plus", "SEGMENTO"] = 200
target.loc[target['SEGMENTO'] == "Emprendedor", "SEGMENTO"] = 300
target.loc[target['SEGMENTO'] == "PYME", "SEGMENTO"] = 400
target.loc[target['SEGMENTO'] == "Personal", "SEGMENTO"] = 500
target.loc[target['SEGMENTO'] == "Empresarial", "SEGMENTO"] = 600


possible_fraud = knn_classifier.predict(target[relevant_vars])
target["FRAUDE"] = possible_fraud
target.to_csv("reto6.csv")

accuracy = accuracy_score(y_test, y_pred)
y_probabilities = knn_classifier.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_probabilities)
roc_auc = auc(fpr, tpr)

print(f"Precisión del modelo: {accuracy}")
plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()
