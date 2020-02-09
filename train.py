import pickle
with open("games/arkanoid/log/level_1.pickle", "rb") as f:
	data_list1 = pickle.load(f)

with open("games/arkanoid/log/level_2.pickle", "rb") as f:
	data_list2 = pickle.load(f)

with open("games/arkanoid/log/level_3.pickle", "rb") as f:
	data_list3 = pickle.load(f)

Frame=[]
Status=[]
Ballposition=[]
PlatformPositon=[]
Bricks=[]
for i in range(0,len(data_list1)):
	Frame.append(data_list1[i].frame)
	Status.append(data_list1[i].status)
	Ballposition.append(data_list1[i].ball)
	PlatformPositon.append(data_list1[i].platform)
	Bricks.append(data_list1[i].bricks)
for j in range(0,len(data_list2)):
	Frame.append(data_list2[j].frame)
	Status.append(data_list2[j].status)
	Ballposition.append(data_list2[j].ball)
	PlatformPositon.append(data_list2[j].platform)
	Bricks.append(data_list2[j].bricks)
for k in range(0,len(data_list3)):
	Frame.append(data_list3[k].frame)
	Status.append(data_list3[k].status)
	Ballposition.append(data_list3[k].ball)
	PlatformPositon.append(data_list3[k].platform)
	Bricks.append(data_list3[k].bricks)





import numpy as np
# PlatX為板子的初始X座標
PlatX=np.array(PlatformPositon)[:,0][:, np.newaxis]
# Plat_X為板子的下一步X座標
PlatX_next=PlatX[1:,:]
# 顯示板子的移動方向（+為往右，-為往左） (5為板子移動速度)
instruct=(PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5
# 球的座標集合
Ballarray=np.array(Ballposition[:-1])
ball_x=Ballarray[:,0]
ball_y=Ballarray[:,1]
# x 為球座標
x_history=[1]
platform_array=PlatX[0:-1,0]#[:,np.newaxis]
for index in range(1, len(ball_x)):
	ball_now_x = ball_x[index]
	ball_pre_x = ball_x[index-1]
	v = ball_now_x-ball_pre_x > 0
	if v > 0:
		x_history.append(1)
	if v == 0:
		x_history.append(0)
	if v < 0:
		x_history.append(-1)
x_is_Right_array=np.array(x_history)
print(ball_x)
print(ball_y)
print(platform_array)
print(x_is_Right_array)

x=np.array((
	ball_x,
	ball_y,
	platform_array,
	x_is_Right_array
	)).T
print("x",x)
print(x.shape)
# y 為板子的x座標
y=instruct

from sklearn.model_selection import train_test_split


x_train, x_test,y_train, y_test = train_test_split(x,y,test_size = 0.2, random_state=41)

from sklearn.svm import SVC

from sklearn.metrics import accuracy_score

svm = SVC(gamma='auto')
sav = svm.fit(x_train,y_train)

yp_svm=svm.predict(x_test)
acc_test=accuracy_score(yp_svm,y_test)
print("accuracy_score:",acc_test)
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# # scatter --> 等同excel上面的散佈圖
# x1 =  x[:,0]
# x2 = x[:,1]
# fig = plt.figure()
# ax = plt.subplot(111, projection='3d')
# ax.scatter(x1,x2,y,c='red',marker='D')
# # plt.scatter(x2,y,c='red',marker='D')
# # plt.legend(["x1","y"])
# # plt.title("ball movement")

# plt.show()

# filename = "games/arkanoid/ml/model.sav"
filename = "model.sav"
pickle.dump(sav,open(filename,'wb'))
