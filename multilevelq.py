from queue import Queue,LifoQueue,PriorityQueue

q1=Queue()
q2=Queue()
q3=PriorityQueue()
mainqueue=Queue()


q1stats=[]
q2stats=[]
q3stats=[]

q1list=[]
q2list=[]
q3list=[]

mainqueue.put(q1)
mainqueue.put(q2)
#mainqueue.put(q3)


def createProcess(pid,at,bt,p):
    return {'ProcessID':pid,'ArrivalTime':at,'BurstTime':bt,'Priority':p}


with open("sample.txt","r") as f:
    for line in f.readlines():
        process,at,bt,priority=line.split(",")
        q1list.append(createProcess(process,int(at),int(bt),int(priority)))

with open("sample.txt","r") as f:
    for line in f.readlines():
        process,at,bt,priority=line.split(",")
        q2list.append(createProcess(process,int(at),int(bt),int(priority)))


def createProcessStats(process,CT):
    TT=CT-process['ArrivalTime']
    WT=TT-process['BurstTime']
    return {'ProcessID':process['ProcessID'],'ArrivalTime':process['ArrivalTime'],'BurstTime':process['BurstTime'],'Priority':process['Priority'],
            'CompletionTime':CT,'TurnAroundTime':TT,'WaitingTime':WT}


def printstats(qstats,avg=True):
    n=0
    TT=0
    WT=0
    for stat in sorted(qstats, key=lambda k: int(k['ProcessID'].split('P')[1])) :
        if not avg:
            for a in stat:
                print(a,stat[a])
            print(30*"*")
        n+=1
        TT+=stat['TurnAroundTime']
        WT+=stat['WaitingTime']
    if avg:
        print("Average Turn Around Time:",TT/n)
        print("Average Waiting Time:",WT/n,"\n")



def printqueue(q):
    for x in q.queue:
        print(x['ProcessID'],x['ArrivalTime'],x['BurstTime'])

def FIFO(q,time,show=True,it=0):
    t=-1
    while t<time and not (q.empty() and len(q2list)==0):
        templist=list(q.queue)
        for i in templist:
            if show:
                print("time:",t)
                printqueue(q)
                print(30*"*")
            if t>time:
                break
            if i['BurstTime']+t<time:
                t+=i['BurstTime']
                x=q.get()
                q2stats.append(createProcessStats(x,t+(time*it)))
            else:
                t+=1
                break
            for ele in q2list:
                if ele['ArrivalTime']<=t:
                    q.put(ele)
                    q2list.remove(ele)
            
        if q.empty():
            t+=1
            for ele in q2list:
                
                if ele['ArrivalTime']<=t:
                    q.put(ele)
                    q2list.remove(ele)

def roundrobin(q,time,tq,show=True,it=0):
    t=0
    while t<time and not (q.empty() and len(q1list)==0):
        templist=list(q.queue)
        for i in templist:
            if show:
                print("time:",t)
                printqueue(q)
                print(30*"*")
                
            t+=tq
            if t>time:
                break       
            i['BurstTime']-=tq
            if i['BurstTime']<=0:
                x=q.get()
                q1stats.append(createProcessStats(x,t+(time*it)))
            else:
                x=q.get()
                q.put(createProcess(x['ProcessID'],x['ArrivalTime'],x['BurstTime'],x['Priority']))
            for ele in q1list:
                if ele['ArrivalTime']<=t:
                    q.put(ele)
                    q1list.remove(ele)
            
        if q.empty() and len(q1list)!=0:
            t+=tq
            for ele in q1list:
                if ele['ArrivalTime']<=t:
                    q.put(ele)
                    q1list.remove(ele)


def SJF(q,time,show=True,it=0):
    q.sort(key=lambda  x:x["BurstTime"],reverse= False)
    in_time=0
    min_time_proc=q[0]
    count=0
    while in_time+min_time_proc["BurstTime"]<time and len(q) != 0:
        q.pop(0)
        in_time+=min_time_proc["BurstTime"]
        min_time_proc=q[0]






p1=40
p2=60
timequantum=2
totaltime=0
maxtotaltime=100
timejumps=20
it=0
while totaltime<maxtotaltime:
    roundrobin(q1,timejumps*p1/100,timequantum,show=False,it=it)
    FIFO(q2,timejumps*p2/100,show=False,it=it)
    totaltime+=timejumps
    it+=1

printstats(q1stats,avg=True)
printstats(q2stats,avg=True)