import pickle
with open("games/arkanoid/log/2020-02-08_11-18-24.pickle", "rb") as f:
	data_list = pickle.load(f)

Frame=[]
Status=[]
Ballposition=[]
PlatformPositon=[]
Bricks=[]
for i in range(0,len(data_list)):
	Frame.append(data_list[i].frame)
	Status.append(data_list[i].status)
	Ballposition.append(data_list[i].ball)
	PlatformPositon.append(data_list[i].platform)
	Bricks.append(data_list[i].bricks)

import numpy as np
# PlatX為板子的初始X座標
PlatX=np.array(PlatformPositon)[:,0][:, np.newaxis]
# Plat_X為板子的下一步X座標
PlatX_next=PlatX[1:,:]
# 顯示板子的移動方向（+為往右，-為往左） (5為板子移動速度)
instruct=(PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5

Ballarray=np.array(Ballposition[:-1])
print(Ballarray)
# --->
# x 為球座標
x=np.hstack((Ballarray,PlatX[0:-1,0][:,np.newaxis]))
# y 為板子的x座標
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