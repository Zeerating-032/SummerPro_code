from random import randint
import os, time

#prepare
start=time.time()
os.makedirs("./Question", 0o777, exist_ok=True)
os.makedirs("./CorrectAnswer/", 0o777, exist_ok=True)
file_name=[]
for i in range(1000):
	x=str(i)
	while len(x)<3:
		x="0"+x
	file_name.append(x)

num=[]
aim_list=[]
one_or_zero=[]

#make aim_list
def make_number():
	global num, aim_list, one_or_zero
	num=[[randint(1,19) for i in range(5)]for j in range(5)]
	aim_list=[0 for i in range(11)]
	one_or_zero=[[randint(0,1) for i in range(5)]for j in range(5)]
	for i in range(11):
		if i<5:
			for j in range(5):
				if bool(one_or_zero[j][i]):
					aim_list[i]+=num[j][i]
		if i==5:
			for j in range(5):
				if bool(one_or_zero[j][4-j]):
					aim_list[i]+=num[j][4-j]
		if i>5:
			for j in range(5):
				if bool(one_or_zero[i-6][j]):
					aim_list[i]+=num[i-6][j]

def len2(x):
    x=str(x)
    while len(x)<2:
        x="0"+x
    return x
    
def out_question(aim_list, num, txt):
    #first line
    for i in range(5):
        print(len2(aim_list[i]),end=' ', file=txt)
    else:
        print(len2(aim_list[5]), file=txt)
    #other
    for i in range(5):
        for j in range(5):
            print(len2(num[i][j]),end=' ', file=txt)
        else:
            print(len2(aim_list[i+6]), file=txt)
def out_answer(one_or_zero, txt):
    for i in range(5):
        for j in range(4):
            print(one_or_zero[i][j],end=' ', file=txt)
        else:
            print(one_or_zero[i][4], file=txt)
    txt.close()
#main
for i in file_name:
	make_number()
	q_txt=open("./Question/{}.txt".format(i), "w")
	co_ans=open("./CorrectAnswer/{}.txt".format(i), "w")
	out_question(aim_list,num,q_txt)
	out_answer(one_or_zero,co_ans)
	q_txt.close()
	co_ans.close()
print("完成，一千組花了{:.2f}秒".format(time.time()-start))
