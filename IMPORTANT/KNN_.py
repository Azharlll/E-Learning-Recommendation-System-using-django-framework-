import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import model_selection
from sklearn.cross_validation import train_test_split #split the data into train and test data
import MySQLdb
mysql_cn= MySQLdb.connect(host='localhost',port=3306,user='work', password='work1234',db='demo9')

data=pd.read_sql('select * from Postprocessing_tab',con = mysql_cn)
n1=len(data)
l=list(data[0:0])
l1=l.index('Q1M5')

def model_KNN(qs,qe,st):
    KNN1=pd.DataFrame(data.iloc[0:n1,qs:qe])
    KNN2=pd.DataFrame(data.iloc[0:n1,st])
    X_train, X_test, y_train, y_test = train_test_split(KNN1, KNN2, test_size = 0.25, random_state = 0)
    clf = KNeighborsClassifier(n_neighbors=3)
    clf.fit(X_train,y_train.values.ravel())
    test=clf.predict(X_test)
    kfold = model_selection.KFold(n_splits=15)
    accuracy = model_selection.cross_val_score(clf,X_train,y_train.values.ravel(), cv=kfold)
    return test,accuracy.mean()*100

vocab=model_KNN(l1,l1+9,l1+63)
print("Vocabulary Section: ",vocab[0])
print("accuracy Vocabulary: ",vocab[1])

grammar=model_KNN(l1+9,l1+18,l1+64)
print("Grammar Section",grammar[0])
print("accuracy Vocabulary: ",grammar[1])

reading=model_KNN(l1+18,l1+30,l1+65)
print("Reading Section",reading[0])
print("accuracy Reading: ",reading[1])

Computer=model_KNN(l1+30,l1+35,l1+66)
print("Computer Section",Computer[0])
print("accuracy Computer: ",Computer[1])

writing=model_KNN(l1+35,l1+38,l1+67)
print("Writing Section",writing[0])
print("accuracy Writing: ",writing[1])

video=model_KNN(l1+38,l1+41,l1+68)
print("Video Section",video[0])
print("accuracy video: ",video[1])

audio=model_KNN(l1+41,l1+44,l1+69)
print("Audio Section",audio[0])
print("accuracy audio: ",audio[1])

PPT=model_KNN(l1+44,l1+47,l1+70)
print("PPT Section",PPT[0])
print("accuracy PPT: ",PPT[1])

mysql_cn.close()
