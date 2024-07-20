#Import libraries
import pandas as pd
import pickle as pk
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#Load the dataset
filepath  = 'startup.csv'
data = pd.read_csv(filepath)
print(data.head(10))

#Select variable
data_copy = data.copy()
data_copy.columns = ['Research_And_Development', 'Administration', 'Marketing_Spend', 'State', 'Profit']
print(data_copy.head(10))

#Data cleaning (preprocessed)
y = data_copy ['Profit']
x = data_copy.drop(columns =['Profit']) 
categorical_features = ['State']
one_hot = OneHotEncoder(sparse_output=False, drop='first')
x_encoded = one_hot.fit_transform(x[categorical_features])
encoded_columns = one_hot.get_feature_names_out(categorical_features)
x_encoded_df = pd.DataFrame(x_encoded, columns=encoded_columns)
x_numeric = x.drop(columns = categorical_features)

x_preprocessed = pd.concat([x_encoded_df, x_numeric.reset_index(drop =True)], axis=1)

x_preprocessed.columns = x_preprocessed.columns.astype(str)
scaler  = StandardScaler()
x_scaled = scaler.fit_transform(x_preprocessed)
print(x_scaled)

#Train and test the model
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

#predict  model 
y_pred = model.predict(x_test)
print(y_pred)
print(y_test)

#check if model is good 
mse = mean_squared_error(y_test, y_pred, squared = False)
print(mse)

model_score = model.score (x_test, y_test)*100
print(model_score)

#Saving my model using pickle
with open('model.pkl', 'wb') as file:
    pk.dump(model, file)


