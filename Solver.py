#-*-coding='UTF8'-*-
import os, time
from itertools import combinations
from copy import deepcopy

os.makedirs("./Output/", 0o777, exist_ok=True)
out_path="./Output/"
file_name=[]
for i in range(1000):
    x=str(i)
    while len(x)<3:
        x="0"+x
    x=x+".txt"
    file_name.append(x)

aim_list, num, ans=[],[],[]
has_collect=0

def read_in_question(which_file):
    global aim_list, num
    q_path="./Question/"
    q_file=open(q_path+which_file, "r")
    x=q_file.readlines()
    each_element=[]
    for i in x:
        line_split=i.strip().split()
        for j in line_split:
            each_element.append(int(j))
	#first line
    for i in range(6):
        aim_list[i]=each_element[i]
	#the other line
    for i in range(5):
        for j in range(6):
            if j<5:
                num[i][j]=each_element[(i+1)*6+j]
            else:
                aim_list[i+j+1]=each_element[5+6*(i+1)]
def initialization():
    global aim_list, num, ans
    aim_list=[None for i in range(11)]
    num=[[None for i in range(5)] for j in range(5)]
    ans=deepcopy(num)
#找所有index
def findall_in_list(aim, lis):
    fit=[]
    for i in range(len(lis)):
        if lis[i]==aim:
            fit.append(i)
    return fit #a list
#找位置以string list回傳
def find_target_pos(ind):
    if ind<5: #find what position of numbers would sum to aim
        num_pos=[str(r)+str(ind) for r in range(5)]
    elif ind==5:
        num_pos=[str(r)+str(4-r) for r in range(5)]
    elif ind>5:
        num_pos=[str(ind-6)+str(r) for r in range(5)]
    return num_pos #index str list ex."02","03"
#找出真正未湊齊的數，做process_dict
def make_process(aim, target_num_pos):
    global has_collect
    process_dict={}
    for pos in target_num_pos:
        ans_at_pos=ans[int(pos[0])][int(pos[1])]
        if ans_at_pos==1:
            aim=aim-num[int(pos[0])][int(pos[1])]
            has_collect+=num[int(pos[0])][int(pos[1])]
        elif ans_at_pos==0:
            continue
        else:
            process_dict[pos]=num[int(pos[0])][int(pos[1])]
    return aim, process_dict #pos(str) : value
#組合吧，然後尋找
def combine(real_aim, process_dict):
    process_key, process_value=[], []
    combine_key, combine_value=[], []
    for i in process_dict.items():
        process_key.append(i[0])
        process_value.append(i[1])
    for i in range(1,len(process_key)+1):
        for j in combinations(process_key,i):
            combine_key.append("". join(j))
        for j in combinations(process_value, i):
            combine_value.append(sum(j))
    fit=findall_in_list(real_aim, combine_value)
    fit_pos=[combine_key[i] for i in fit]
    return fit_pos #all pos string list
#從位置對應
def set_1_0(fit_pos, process_dict):
    global ans, aim_list, ind, aim_sort, has_collect
    if len(fit_pos)==1:
        for i in process_dict.keys():
            if i in fit_pos[0]:
                ans[int(i[0])][int(i[1])]=1
                has_collect+=num[int(i[0])][int(i[1])]
            else:
                ans[int(i[0])][int(i[1])]=0
    else:#尋找共同
        same=[]
        for i in process_dict.keys():
            for sol in fit_pos:
                if not i in sol:
                    break
            else:
                same.append(i)
        for i in same:
            ans[int(i[0])][int(i[1])]=1
            has_collect+=num[int(i[0])][int(i[1])]
            
    #最後整理
    x=str(aim_list[ind])
    aim_sort.pop()
    if int(x)-has_collect!=0:
        aim_sort.insert(0, x)
    else:
        aim_list[ind]="0" #string就不會再被搜到
    has_collect=0
def output(txt):
    txt=open(out_path+txt, 'w')
    for i in range(5):
        for j in range(4):
            print(ans[i][j],end=' ', file=txt)
        else:
            print(ans[i][4], file=txt)
    txt.close()

#main
start=time.time()
front_round_time=time.time()
for file in file_name:
    initialization()
    read_in_question(file)
    aim_sort=sorted(aim_list)
    while len(aim_sort)!=0:
        #跳過
        round_time=time.time()
        if round_time-front_round_time>0.1:
            print(file)
            output(file)
            break
        #檢查
        if type(aim_sort[-1])==type("str"):
            for x in range(len(aim_sort)):
                aim_sort[x]=int(aim_sort[x])
            for y in range(len(aim_list)):
                aim_list[y]=int(aim_list[y])
        #開始計算
        aim=aim_sort[-1]
        all_index=findall_in_list(aim, aim_list)
        for ind in all_index:
            all_target_num_pos=find_target_pos(ind)
            real_aim, process_dict=make_process(aim, all_target_num_pos)
            if real_aim!=0:
                fit_pos=combine(real_aim, process_dict)
                set_1_0(fit_pos, process_dict)
            else:#已湊齊之後設定0
                for pos in all_target_num_pos:
                    if ans[int(pos[0])][int(pos[1])]==None:
                        ans[int(pos[0])][int(pos[1])]=0
                has_collect=0
                aim_list[ind]="0" #string就不會再被搜到
                aim_sort.pop()
    output(file)
    front_round_time=round_time
print("完成，一千個檔案花了{:.2f}秒".format(time.time()-start))