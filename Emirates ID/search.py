import enchant
import sys
import numpy as np
from dateutil.parser import parse
#import str

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False


def word_check(name):
    dicti=enchant.PyPWL("words.txt")
    word_exists=dicti.check(name)
    if word_exists:
        print("Already there!!")
        return name
    if not word_exists:
        suggest=dicti.suggest(name)
        print("input: ",name)
        if len(suggest)>0:
            print("suggested: ",suggest[0])

            a=np.zeros([len(suggest[0])+1,len(name)+1])
        # print(a)
            a[0]=np.arange(len(name)+1)
            a[:,0]=np.arange(len(suggest[0])+1)
        # print(a)
            for i in range(1,len(suggest[0])+1):
                #print(i)
                for j in range(1,len(name)+1):
                    if suggest[0][i-1]==name[j-1]:
                        #print('Same')
                        a[i,j]=a[i-1,j-1]
                    else:
                        #print('different')
                        a[i,j]=min(a[i-1,j],a[i,j-1],a[i-1,j-1])+1
            #print(type(a[-1,-1]))
            n=float(a[-1,-1])
            #print(len(name))
            if n <= len(name)/2:
                print("lol")
                if not len(suggest[0]) in range(len(name),len(name)+2):
                    print("Suggested won't be implemented")
                    return name
                else:
                    print("Change accepted")
                    #str.replace(name,suggest[0])
                    return suggest[0]
                

            else:
                print("change rejected")
                return name
        
        else:
            return name

file=open('aratext.txt','r+')
content=file.readlines()
#content=content.split()
print(type(content))
for line in content:
    main_index=content.index(line)
    for name in line.split():
        if '/' in name:
            #if is_date(name):
                date_list=name.split('/')
                for num in date_list:
                    num_response = word_check(num)
                    #replace(num,num_response)
                    #line.replace(num,num_response)
                    ind=date_list.index(num)
                    date_list[ind]=num_response
                new_date='-'.join(date_list)
                #main_ind=line.index(name)
                #line[main_ind]=new_date
                line.replace(name,new_date)
                    
            #else:
                #response=word_check(name)
                #replace(name,response)
                #content.replace(num,num_response)
                #main_ind=content.index(name)
                #content[main_ind]=response

        elif '-' in name:
            #if is_date(name):
            date_list=name.split('-')
            for num in date_list:
                num_response = word_check(num)
                    #replace(num,num_response)
                ind=date_list.index(num)
                date_list[ind]=num_response
            new_date='-'.join(date_list)
            #main_ind=line.index(name)
            #line[main_ind]=new_date
            line.replace(name,new_date)
            #else:
                #word_list=name.split('-')
                #response=word_check(name)
                #replace(name,response)
                #content.replace(num,num_response)
                #main_ind=content.index(name)
                #content[main_ind]=response
        else:
            response=word_check(name)
            #content.replace(num,num_response)
            #main_ind=line.index(name)
            #line[main_ind]=response
            line.replace(name,response)
    
    content[main_index]=line

file1=open('edited.txt','w')
print(content)
content_write=" ".join(content)
file1.write(content_write)
file.close()
file1.close()