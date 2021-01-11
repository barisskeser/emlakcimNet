import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pandas import Series
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

veriler=pd.read_csv('emlakson.csv')
counter=0
fiyat=veriler['fiyat']
print(veriler.columns)



X=veriler.drop(['fiyat'],axis=1)
print(X.head())
X=pd.get_dummies(X,drop_first=True)#varsa dummy variable olusturmak
print(X.head())
X=X.assign(const=1)
y = veriler.iloc[:, 13].values
from sklearn import preprocessing
scaler=preprocessing.StandardScaler()
X_scaled=scaler.fit_transform(X)#olcekleme islemi
y =scaler.fit_transform(y.reshape(-1, 1))

from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
X_yeni = mms.fit_transform(X_scaled)#normalizasyon islemi
y_yeni= mms.fit_transform(y)

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score




xtrain, xtest, ytrain, ytest = train_test_split(X_yeni, y_yeni, test_size=0.15)

xgbr = xgb.XGBRegressor(verbosity=0)
print(xgbr)
xgbr.fit(xtrain, ytrain)
score = xgbr.score(xtrain, ytrain)   
print("Training score: ", score) 
# - cross validataion 
scores = cross_val_score(xgbr, xtrain, ytrain, cv=5)
print("Mean cross-validation score: %.2f" % scores.mean())
kfold = KFold(n_splits=10, shuffle=True)
kf_cv_scores = cross_val_score(xgbr, xtrain, ytrain, cv=kfold )
print("K-fold CV average score: %.2f" % kf_cv_scores.mean())


ypred = xgbr.predict(xtest)
mse = mean_squared_error(ytest, ypred)
print("MSE: %.2f" % mse)
print("RMSE: %.2f" % (mse**(1/2.0)))
print("mean abs percentage:")
print(mean_absolute_percentage_error(ytest,ypred))
x_ax = range(len(ytest))
plt.scatter(x_ax, ytest, s=5, color="blue", label="original")
plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
plt.legend()
plt.show()