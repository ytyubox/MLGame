import pickle
with open("games/arkanoid/log/2020-02-08_11-36-37.pickle", "rb") as f:
	data_list = pickle.load(f)

Frame=[]
Status=[]
Ballposition=[]
PlatformPositon=[]
Bricks=[]
for i in range(0,len(data_list)):
	Frame  			.append(data_list[i].frame)
	Status 			.append(data_list[i].status)
	Ballposition	.append(data_list[i].ball)
	PlatformPositon .append(data_list[i].platform)
	Bricks 			.append(data_list[i].bricks)

import numpy as np
PlatX=np.array(PlatformPositon)[:,0][:, np.newaxis]
PlatX_next=PlatX[1:,:]
instruct=(PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5

Ballarray=np.array(Ballposition[:-1])
# --->
x=np.hstack((Ballarray,PlatX[0:-1,0][:,np.newaxis]))
y=instruct

from sklearn.model_selection import train_test_split
x_train, x_test,y_train, y_test = train_test_split(x,y,test_size = 0.2, random_state=41)

from sklearn.svm import SVC

from sklearn.metrics import accuracy_score

svm = SVC(gamma='auto')
svm.fit(x_train,y_train)

yp_svm=svm.predict(x_test)
acc_test=accuracy_score(yp_svm,y_test)
print("accuracy_score:",acc_test)