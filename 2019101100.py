import csv
import math
import sys
import os
from collections import defaultdict


file=open("files/metadata.txt",'r')
l=file.readlines()
# print(l)

check_table=False
d1={}
d2={}
for i in l :
    i=i[:-1]
    i=i.lower()
    # print(i)
    if(i=="<end_table>"):
        d2[table]=vec
        check_table=False
        continue
    if(i=="<begin_table>"):
        vec=[]
        check_table=True
        continue
    if(check_table):
        table=i
        check_table=False
        continue
    d1[i]=table
    vec.append(i)


def groupby(arr,col,req,command):
    # print(arr,col,req,command)
    ops=['count','avg','sum','min','max']
    if('group' not in command):
        return [arr,col],command,False
    else:
        if('group' in command and command[0]=='group' and command[1]=='by'):
            command.remove('group')
            command.remove('by') 
            temp=command[0]
            command.pop(0)
            count=0
            # words=[]
            k=len(req)
            # for i in range(k+1):
            #     words=''
            words=['' for i in range(len(req)+1)]
            ind=0
            words[len(req)]=temp
            aggs_here=words.copy()
            for i in range(k):
                if(req[i][:5] in ops):
                    aggs_here[i]=req[i][:5]
                    words[i]=req[i][6:-1]
                elif(req[i][:3] in ops):
                    aggs_here[i]=req[i][:3]
                    words[i]=req[i][4:-1]
                else :
                    words[i]=req[i]
                    count+=1
                    ind=i
            if(count>1):
                print('multiple columns in group by')
            arr1=[[row[i] for row in arr] for i in range(len(arr[0]))]
            arr=[]
            #cols.append(temp)
            #print(cols)
            #print(req,aggs_here)
            for i in range(len(words)):
                for j in range(len(col)):
                    if(words[i]==col[j]):
                        arr.append(arr1[j])
                        break
            arr1=[[row[i] for row in arr] for i in range(len(arr[0]))]
            arr=arr1
            if(len(arr[0])!=len(words)):
                print('not found some column')
                quit()
            arr.sort(key=lambda x:x[len(req)])
            final=[]
            n=len(req)
            while(len(arr)!=0):
                m=len(arr)
                if(m==0):
                    break
                hell=arr[0][n]
                temp=[[]for i in range(len(req))]
                for i in range(m):
                    if(arr[0][n]==hell):
                        for j in range(n):
                            temp[j].append(arr[0][j])
                        arr.pop(0)
                here=[0 for i in range(n)]
                for i in range(n):
                    if(aggs_here[i]):
                        here[i]=operations(temp[i],aggs_here[i])
                    else :
                        here[i]=temp[i][0]
                final.append(here)
            temp=[]
            for i in range(len(words[:-1])):
                if(aggs_here[i]):
                    temp.append(aggs_here[i]+'('+words[i]+')')
                else:
                    temp.append(words[i])
            return [final,temp],command,True
            #arr=extract_table(arr,col,req)

def order(arr,cols,com):
    if('order' not in com):
        return [arr,cols],com
    com.pop(0)
    com.pop(0)
    flag=1
    main_flag=0
    here="asc"
    if(len(com)>1):
        here=com[1]
    # if():
    #     main_flag=1
    if(len(com)>1 and here=='desc'):
        flag=-1
    else :
        flag=1
    ele=com[0]
    # print("check order: ",ele)
    flag1=0
    for i in range(len(cols)):
        if(cols[i]==ele):
            flag1=1
            arr.sort(key=lambda x:flag*x[i])
    # print("check order1: ",arr)
    if(flag1==0):
        print('Sorry!,column not found in ordering:(')
        quit()
    return [arr,cols],com


def operations(arr,inp):
    if(inp=='min'):
        mi=min(arr)
        return mi
    elif (inp=='max'):
        ma=max(arr)
        return ma
    elif(inp=='sum'):
        su=sum(arr)
        return su
    elif (inp=='avg'):
        av=sum(arr)/len(arr)
        return av
    else :
        return len(arr)


def aggs(arr,cols,words):
    # print("check col: ",cols)
    #arr=> has list of elements in table
    # words => command given by user
    temp=0
    for i in range(len(words)):
        if('(' in words[i]):    
            temp=temp+1

    vari=0 # checker
    if(temp==len(words)):
        temp1=[[row[i] for row in arr] for i in range(len(arr[0]))]
        vari=1
        arr=temp1
    else :
        return [arr,cols]
    # filling zeroes to list of size n    
    n=len(words)
    lis=[0 for i in range(n)]

    for i in range(len(words)):
        main_flag=0
        flag=0
        if(words[i][3]=='('):
            for j in range(len(cols)):
                # print(cols[j],words[i][3])
                # words[i][4:-1] is a,b,c like cols => gives only single letter to cmp in max(a) or min(a)
                if(cols[j]==words[i][4:-1]):
                    # print("going:  ",arr[j],words[i][0:3])
                    lis[i]=operations(arr[j],words[i][0:3])
                    flag=1
                    main_flag=2
                    # print("check all aggs: ",lis[i])
                    break
        else :
            for j in range(len(cols)):
                if(cols[j]==words[i][6:-1] or words[i][6:-1]=='*'):
                    flag=1
                    main_flag=2
                    lis[i]=operations(arr[j],'count')
                    # print("check count:  ",lis[i])
                    break
        if(flag==0):
            print(words[i])
            print('column not present:(')
    return [[lis],words]




def convert_int(a,arr,words):
    try : 
        int(a)
        return int(a)
    except :
        k=len(words)
        for i in range(k):
            if(words[i]==a):
                return arr[i]
        print("Sorry!,the given column won't exist:/ \n")
        quit()


def where_com(arr,words,command):
    # print("check  ",check)
    k=len(command)
    if(k==0 or 'where' not in command):
        return [arr,words],command
    if(command[0]!="where"):
        print("where command not found:(\n")
        quit()
    command.remove("where")
    str1=""
    str2=""
    c1=0
    c2=0
    if('or' in command):
        c1=1
        le=len(command)
        for i in range(le):
            ss=command[0].lower()
            if(ss=='or'):
                command.pop(0)
                break
            str1=str1+command[0]
            command.pop(0)
        le1=len(command)
        for i in range(le1):
            ss1=command[0].lower()
            if(ss1=='group' or ss1=='order'):
                break
            str2=str2+command[0]
            command.pop(0)
    # check for and
    elif('and' in command):
        # print("welcome to and\n")
        c2=1
        le=len(command)
        # print("where check1\n",command)
        for i in range(le):
            ss=command[0].lower()
            if(ss=='and'):
                command.pop(0)
                break
            str1=str1+command[0]
            command.pop(0)
        # print("where check2\n",command)
        le1=len(command)
        for i in range(le1):
            ss1=command[0].lower()
            if(ss1=='group' or ss1=='order'):
                break
            str2=str2+command[0]
            command.pop(0)
    
    else:
        le1=len(command)
        c2=1
        for i in range(le1):
            ss1=command[0].lower()
            if(ss1=='group' or ss1=='order'):
                break
            str2=str2+command[0]
            command.pop(0)
        str1=str2
    # print("where check3\n",str1,str2,"\n")
    str3=''
    #11
    str4=''
    oper1=''
    ss2=len(str1)
    for i in range(ss2):
        stradd=str1[i]+str1[i+1]
        if(stradd =='<='):
            str3=str1[:i]
            str4=str1[i+2:]
            oper1='<='
            break
        if(stradd=='>='):
            str3=str1[:i]
            str4=str1[i+2:]
            oper1='>='
            break
        if(str1[i]=='<'):
            str3=str1[:i]
            oper1='<'
            str4=str1[i+1:]
            break
        if(str1[i]=='>'):
            oper1='>'
            str4=str1[i+1:]
            str3=str1[:i]
            break
        if(str1[i]=='='):
            str4=str1[i+1:]
            oper1='='
            str3=str1[:i]
            break
    str5='' 
    #21
    str6=''
    #22
    oper2=''
    ss3=len(str2)
    for i in range(ss3):
        stradd=str2[i]+str2[i+1]
        if(stradd =='<='):
            str5=str2[:i]
            str6=str2[i+2:]
            oper2='<='
            break
        if(stradd=='>='):
            str5=str2[:i]
            str6=str2[i+2:]
            oper2='>='
            break

        if(str2[i]=='<'):
            str6=str2[i+1:]
            str5=str2[:i]
            oper2='<'
            break
        if(str2[i]=='>'):
            str6=str2[i+1:]
            str5=str2[:i]
            oper2='>'
            break
        if(str2[i]=='='):
            str6=str2[i+1:]
            oper2='='
            str5=str2[:i]
            break
    # print("where check4:  ",str3,str4,str5,str6,oper1,oper2,"\n")
    lis=[]
    for i in range(len(arr)):
        ad=0
        t1=convert_int(str3,arr[i],words)
        t2=convert_int(str4,arr[i],words)
        # print("where check5:  ",t1,t2,t3,t4)
        if(oper1=='<=' and t1<=t2):
            ad+=1
        if(oper1=='>=' and t1>=t2):
            ad+=1
        if(oper1=='<' and t1<t2):
            ad+=1
        if(oper1=='>' and t1>t2):
            ad+=1
        if(oper1=='=' and t1==t2):
            ad+=1
        t3=convert_int(str5,arr[i],words)
        t4=convert_int(str6,arr[i],words)
        if(oper2=='<=' and t3<=t4):
            ad+=1
        if(oper2=='>=' and t3>=t4):
            ad+=1
        if(oper2=='<' and t3<t4):
            ad+=1
        if(oper2=='>' and t3>t4):
            ad+=1
        if(oper2=='=' and t3==t4):
            ad+=1
        if(c2==1):
            if(ad==2):
                lis.append(arr[i])
        if(c1==1):
            if(ad>0):
                lis.append(arr[i])
    # print("final:  ",arr)
    # print("where check6 :  ",t1,t2,t3,t4)
    # print("where check7 :  ",c2,c1,ad)
    # print("lis  ",lis,words)
    return [lis,words],command






def readdtable(command):
    arr=['where','order','group']
    strr=''
    k=len(command)
    while(len(command) and command[0] not in arr):
        strr=strr+command[0]
        command.pop(0)
    strr=strr.split(',')
    l=[]
    words=[]
    n=len(strr)
    for i in range(n):
        if(i==0):
            tab=strr[i]
            with open('./files/{0}.csv'.format(tab), 'r') as file:
                reader = csv.reader(file)
                dict_obj=defaultdict(list)
                for r in reader:
                    for i in range(len(r)):
                        dict_obj[d2[tab][i]].append(int(r[i]))
                table1=list([v[1] for v in dict_obj.items()])
                tab1=[[row[i] for row in table1] for i in range(len(table1[0]))]
                l=tab1
                # print("l:  ",l)
        else :
            tab=strr[i]
            with open('./files/{0}.csv'.format(tab), 'r') as file:
                reader = csv.reader(file)
                dict_obj=defaultdict(list)
                for r in reader:
                    for i in range(len(r)):
                        dict_obj[d2[tab][i]].append(int(r[i]))
                table1=list([v[1] for v in dict_obj.items()])
                tab1=[[row[i] for row in table1] for i in range(len(table1[0]))]
                m=tab1
            ll=[l[ii]+m[j] for ii in range(len(l)) for j in range(len(m))]
            # print("lll: \n",ll)
            l=ll
        words.extend(d2[tab])
    return [l,words],command


def select_com(arr,words,me):
    # print("sel  ",arr)
    out=[[row[i] for row in arr] for i in range(len(arr[0]))]
    ll=[]
    bhav=''
    if('select' in bhav):
        print("yes its there")
    for i in me:
        flag=0
        k=len(words)
        for j in range(k):
            if(words[j]==i):
                flag=1
                ll.append(out[j])
        if(flag==0):
            print('column not present to select')
            quit()
    out=[[row[i] for row in ll] for i in range(len(ll[0]))]
    # print(arr1)
    return [out,me]


def dis(arr):
    me=[ele for ind, ele in enumerate(arr) if ele not in arr[:ind]]
    return me



# .................................................start........................................

command=sys.argv[1]
# print("com:   ",command)
# checking last character,if semi colon is not present giving error and exit
if(command[-1]!=';'):
    print('semicolon error')
    quit()
#convert to lower case
command=command.lower()
# strip() method removes any spaces or specified characters at the start and end of a string
command=command.strip()
# print("com1   ",command)

command=command[:-1].split()
# print("com2   ",command)

k=len(command)
if(k==0):
	print("no command found")
	quit()

if(k<2):
	print("not a correct command")
	quit()

select=0
if(command[0]=='select'):
	select=1
if(select==0):
	print("no select keyword found")
	quit()
if command[0] == 'UNKNOWN':
    print("Query Syntax Error")
    exit(0)
if command[0] == 'UPDATE':
    print("Query not supported")
    exit(0)
if command[0] == 'CREATE':
    print("Query not supported")
    exit(0)
if command[0] == 'DELETE':
    print("Query not supported")
    exit(0)

command.remove('select')
# print(command)




distinct=0
if(command[0]=='distinct'):
	distinct=1
	command.remove('distinct')

if('from' not in command):
	print("not found from in command")
	quit()

word=''
for i in range(len(command)):
	if(command[0]=='from'):
		command.remove('from')
		break;
	word=word+command[0]
	command.pop(0)
# splitting the string using comma
word=word.split(',')
# print("word :",word)

if(len(word)==0):
	print("no keywords in command")
	quit()

# print("la ",command)
l,command=readdtable(command)
# print("table function",l[1],command)

if(word[0]=='*'):
    temp=l[1].copy()
    temp.extend(word[1:])
    word=temp

# print("*",word)
# print("go: ",l[0])





group_flag=False
# print("l[0]:   ",l[0]) integers in tables
# print("l[1]:   ",l[1]) a b c d e
l,command=where_com(l[0],l[1],command)

# print(l[0],command)
# print("check where:  ",l)
# print('command:   ',command)

# group
l,com,group_flag=groupby(l[0],l[1],word,command)
l,command=order(l[0],l[1],command)

# print("order check: ",l)

if(group_flag==False):
    l=aggs(l[0],l[1],word)

# print("CHECK aggs\n",l[0],l[1])

l=select_com(l[0],l[1],word)
# print("check select  \n",l)

if(distinct==1):
    l[0]=dis(l[0])

# print("CHECK dis\n",l[0])




# output formatting

def print_all(l):
    le =len(l[0][0])
    l,final=l[0],l[1]
    words=[]
    aggs=[]
    for i in range(le):
        le1=len(final[i])
        if(le1 >3 and final[i][3]=='('):
            aggs.append(final[i][0:3])
            words.append(final[i][4:-1])
        elif(len(final[i])>5 and final[i][5]=='('):
            aggs.append(final[i][0:5])
            words.append(final[i][6:-1])
        else :
            aggs.append('')
            words.append(final[i])

    for i in range(le):
        if(i==0):
            # print("aggs     ",aggs[i])
            if(aggs[i]):
                print(aggs[i],'(',words[i],')','.',d1[words[i]],sep='',end='')
            else:
                print(words[i],'.',d1[words[i]],sep='',end='')
        else :
            # print("aggs     ",aggs[i])
            if(aggs[i]):
                print(',',aggs[i],'(',words[i],')','.',d1[words[i]],sep='',end='')
            else:
                print(',',words[i],'.',d1[words[i]],sep='',end='')
    print()
    for i in range(len(l)):
        for j in range(le):
            if(j==0):
                print(l[i][j],sep='',end='')
            else :
                print(',',l[i][j],sep='',end='')
        print()

print_all(l)







