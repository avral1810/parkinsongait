"""

|\\									B = C - A;
|A\B\  								F = 3.14 - D
|  \  \ 							G = 6.28 - (E + F + B)
|   \   \
|    \    \			C1				A = tan(C1.x/C1.y)		C = tan(C2.x/C2.y)
|____D\G    \						D = tan(C1.y/C1.x)
|      \      \
|       \       \
|        \        \
|         \         \
|_________D\F________E\	C2



"""
import statistics
import sys
import math
#import matplotlib.pyplot as plt
import numpy as np
from smooth import smoothListGaussian

def distance(C1, C2):
	dist = ((C1[0] - C2[0]) * (C1[0] - C2[0])) + ((C1[1] - C2[1]) * (C1[1] - C2[1]))
	dist = math.sqrt(dist)
	return dist


def remove_outliers(ele, t):
	ele1 = ele
	ele = np.array(ele)
	mean = np.mean(ele,axis = 0)
	sd = np.std(ele,axis = 0)
	if t == 'linear':
		fl = [x for x in ele1 if( x > mean -2 *sd)]
		fl = [x for x in fl if (x < mean + 2 * sd)]
		return fl

	elif t == 'variable':
		fl = [x for x in ele1 if( x > mean -2.5 *sd)]
		fl = [x for x in fl if (x < mean + 2.5 * sd)]
		return fl



def remove_outliers_v2(femer_list,tibia_list,time_list,hip_angle_list,leg_list,knee_angle_triangle_list, knee_angle_list, r_p):
	ele1 = np.array(femer_list)
	mean_femer = np.mean(ele1, axis = 0)
	sd_femer = np.std(ele1,axis = 0)
	ele1 = np.array(tibia_list)
	mean_tibia = np.mean(ele1, axis = 0)
	sd_tibia = np.std(ele1,axis = 0)

	#print(mean_femer)
	#print(sd_femer)

	i = int(0)
	iterations = len(time_list)
	while i < iterations: 
		if femer_list[i] > (mean_femer + r_p * sd_femer) or femer_list[i] < (mean_femer - r_p * sd_femer) or tibia_list[i] > (mean_tibia + r_p * sd_tibia) or tibia_list[i] < (mean_tibia - r_p * sd_tibia):
			del time_list[i]
			del femer_list[i]
			del tibia_list[i]
			del hip_angle_list[i]
			del leg_list[i]
			del knee_angle_triangle_list[i]
			del knee_angle_list[i]
			iterations = len(time_list)
			i -= 1
		i = i + 1

def angle(femer, tibia, leg):
	ret = (femer ** 2) + (tibia ** 2) - (leg ** 2)
	ret /= (2 * femer * tibia)
	ret = math.acos(ret)
	return ret * 57.2958



time_list = []
leg_list = []
femer_list = []
tibia_list = []
hip_angle_list = []
knee_angle_triangle_list= []
knee_angle_list = []
XXX = []
ZZZ = []
with open(sys.argv[2], 'r') as file:
	j = int(0)
	for e_line in file:
		name,height, B, G, R, time = e_line.split(':')
		B = B[1:-1]
		G = G[1:-1]
		R = R[1:-1]
		Bx, By = B.split(',')
		Gx, Gy = G.split(',')
		Rx, Ry = R.split(',')
		time = time[:-1]

		Bx = int(Bx)
		By = int(By)
		B = [Bx, By]

		Gx = int(Gx)
		Gy = int(Gy)
		G = [Gx,Gy]

		Rx = int(Rx)
		Ry = int(Ry)
		R = [Rx, Ry]
		ZZZ.append(Rx) 

		for i in range(0,2):
			R[i] -= B[i]
			G[i] -= B[i]
			B[i] = 0
		femer = distance(B,G)
		tibia = distance(R,G)
		leg = distance(B,R)
		XXX.append(R[0])
		
		vert = G[1]
		hori = G[0]
		hip_angle = 0
		try:
			hip_angle = angle(leg,vert,hori)
		except:
			try:
				hip_angle = hip_angle_list[-1]
			except:
				hip_angle = float(0)
		try:
			knee_angle_triangle = angle(femer,tibia,leg)
		except:
			try:
				knee_angle_triangle = knee_angle_triangle_list[-1]
			except:
				knee_angle_triangle = float(0)

		vert = R[1]
		hori = R[0]
		try:
			knee_angle = angle(leg,vert,hori)
		except:
			try:
				knee_angle = knee_angle_list[-1]
			except:
				knee_angle = float(0)


		time_list.append(time)
		hip_angle_list.append(hip_angle)
		leg_list.append(leg)
		femer_list.append(femer)
		tibia_list.append(tibia)
		knee_angle_list.append(knee_angle)
		knee_angle_triangle_list.append(knee_angle_triangle)


gait_time_list = []
peakTime = int(0)
for i in range(1,len(XXX)-1):
	if XXX[i] > XXX[i-1] and XXX[i] > XXX[i+1]:
		time_diff = int(time_list[i]) - peakTime 
		peakTime = int(time_list[i])
		if time_diff > 100 and time_diff < 100000:
			gait_time_list.append(time_diff)

"""plt.plot(time_list,XXX,color = "red")
plt.plot(time_list,ZZZ,color = "blue")"""

gait_cycle_time = statistics.median(gait_time_list)
outlier_limit = float(2.0)
remove_outliers_v2(femer_list,tibia_list,time_list,hip_angle_list,leg_list,knee_angle_triangle_list,knee_angle_list,outlier_limit)
if name == 'Zaid' or name == "ZZaid":
	uid = 1
elif name == "aru":
	uid = 2
elif name == "Aditya":
	uid = 3
else: print("New user")

try:
	if sys.argv[1] == "run":

		with open('dataFiles/test/' + 'someone' +'.csv', 'w') as writeFile:
			for (fl,tl,hal,ll,kal,katl) in zip(femer_list,tibia_list,hip_angle_list,leg_list,knee_angle_list,knee_angle_triangle_list):
				printLine = str(gait_cycle_time) + "," + str(fl) + "," + str(tl) + ","
				printLine += str(hal) + "," + str(ll) + "," + str(kal) + "," + str(katl) + "," + str(height) + "\n"	
				writeFile.write(printLine)

	elif sys.argv[2] == "train":

		with open('dataFiles/fortrain/' + str(uid) +'.csv', 'a') as writeFile:
			for (fl,tl,hal,ll,kal,katl) in zip(femer_list,tibia_list,hip_angle_list,leg_list,knee_angle_list,knee_angle_triangle_list):
				printLine = str(gait_cycle_time) + "," + str(fl) + "," + str(tl) + ","
				printLine += str(hal) + "," + str(ll) + "," + str(kal) + "," + str(katl) + "," + str(height) + ","
				printLine += str(uid) + "\n"
				writeFile.write(printLine)
except:
	print("Provide argument ")
