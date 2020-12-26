import time

file_name=[]
for i in range(1000):
    x=str(i)
    while len(x)<3:
        x="0"+x
    x=x+".txt"
    file_name.append(x)
start=time.time()
correct=0

for file in file_name:
    corr=open("./CorrectAnswer/"+file)
    out=open("./Output/"+file)
    a=corr.read()
    b=out.read()
    if a==b:
        correct+=1
    else:
        print(file)

print("{}%為正確的，花費時間{:.2f}秒".format(correct/10, time.time()-start))