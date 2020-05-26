# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:03:41 2020

@author: U0047365
"""



### Trennschärfe gemessen AUC AR ###

def AUC_AR_gemessen(dataframe):
    
    
    # Filter out the defaulted ratings
    
    fs2=dataframe.dropna()
    ausgefall=fs2[(fs2.ST1>=22)&(fs2.ST2<=21)]
    aus=dict()
    for i in range(0,22):
        for j in ausgefall.ST2:
            if i==j:
                aus[i]=ausgefall[(ausgefall.ST2==j)].count()[1]
                break
            elif i!=j:
                aus[i]= 0
                 
            else :
                pass
             
    # Filter out  all ratings 
    
    lebende=fs2
    leb=dict()
    for i in range(0,22):
        for j in lebende.ST2:
            if i==j:
                leb[i]=lebende[(lebende.ST2==i)].count()[1]
                break
            elif i!=j:
                leb[i]=0
            else :
                pass
            
            
    aus_sum=sum(aus.values()) ##Summe der  Ausgefälle Defaulted
    leb_sum=sum(leb.values()) ##Summe von non-default und defaulted   
    sumcum = leb_sum+aus_sum  #Kumulative Summe der Kreditnehmer

    trenn_AR=[]
    hight=dict()
    deltax=dict()
    bol2=True
    last=0
    if aus_sum==0:
        
        auc=-1
    else:
        for key,i in aus.items():
            hight[key]=last+ ((i/aus_sum)/2) 
            
            for k,j in leb.items():
                if bol2 is False:
                    deltax[k] = ((j+i)/sumcum)
                else:
                    deltax[k]=(j/leb_sum)
            last+=(i/aus_sum)
            
        for j in range(0,22):     
            trenn_AR.append(deltax[j]*hight[j])
            
        
        auc=1-sum(trenn_AR)
        ar=(2*auc)-1
        print(auc,'\n',ar )
        
        return auc,ar


### Plot ROC Curve ###

def plot_curve(dataframe):
    
    import matplotlib.pyplot as plt
    import pandas as pd
    
    #ROC curve  
    # Filter out the defaulted ratings
    
    fs2=dataframe.dropna()
    ausgefall=fs2[(fs2.ST1>=22)&(fs2.ST2<=21)]
    aus=dict()
    for i in range(0,22):
        for j in ausgefall.ST2:
            if i==j:
                aus[i]=ausgefall[(ausgefall.ST2==j)].count()[1]
                break
            elif i!=j:
                aus[i]= 0
                 
            else :
                pass
            
    aus_sum=sum(aus.values())
    prozent_aus=dict()
    for key,i in aus.items():
        prozent_aus[key]=i/aus_sum
    
    
    # Filter out  all ratings 
    
    lebende=fs2
    leb=dict()
    for i in range(0,22):
        for j in lebende.ST2:
            if i==j:
                leb[i]=lebende[(lebende.ST2==i)].count()[1]
                break
            elif i!=j:
                leb[i]=0
            else :
                pass
            
    leb_sum=sum(leb.values())
    prozent_leb=dict()
    for key,i in leb.items():
        prozent_leb[key]=i/leb_sum
    
    a1=list(prozent_leb.values())
    a2=list(prozent_aus.values())
    a2.reverse()
    a2.insert(0,0)
    a1.insert(0,0)
    cum_leb=pd.Series(a1).cumsum()
    cum_aus=pd.Series(a2).cumsum()
    
    plotting=[ plt.figure(),plt.plot(cum_leb*100,cum_aus*100,\
    color='navy',lw=3), plt.plot([0.0, 100], [0.0, 100], color='grey',\
    lw=3, linestyle='--'), plt.xlim([0, 100]),plt.ylim([0, 102]),plt.xlabel\
    ('Kreditnehmer (%)'),plt.ylabel('Ausfälle (%)'),plt.title('ROC Curve')]

    return plotting



### Trennschärfe Optimalmodell (AR) ###



def AR_optimal_model(dataframe):

    fs2=dataframe.dropna()
    
    # Filter out the non-defaulted


    nondefault=fs2[(fs2.ST1<=21)&(fs2.ST2<=21)]
    nondef=dict()
    for i in range(0,22):
        for j in nondefault.ST2:
            if i==j:
                nondef[i]=nondefault[(nondefault.ST2==i)].count()[1]
                break
            elif i!=j:
                nondef[i]=0
            else :
                pass
            
        
    # Filter out the defaulted ratings
    
    
    ausgefall=fs2[(fs2.ST1>=22)&(fs2.ST2<=21)]
    aus=dict()
    for i in range(0,22):
        for j in ausgefall.ST2:
            if i==j:
                aus[i]=ausgefall[(ausgefall.ST2==j)].count()[1]
                break
            elif i!=j:
                aus[i]= 0
                 
            else :
                pass
             
    # Filter out  all ratings 
    
    lebende=fs2
    leb=dict()
    for i in range(0,22):
        for j in lebende.ST2:
            if i==j:
                leb[i]=lebende[(lebende.ST2==i)].count()[1]
                break
            elif i!=j:
                leb[i]=0
            else :
                pass
            
            
    aus_sum=sum(aus.values()) ##Summe der  Ausgefälle Defaulted
    leb_sum=sum(leb.values()) ##Summe von non-default und defaulted   
    sumcum = leb_sum+aus_sum  #Kumulative Summe der Kreditnehmer
    
    
    aus_anz_inKlassen=dict()
    leb_anz_inKlassen=dict()
    for  i in range(0,22):
        if i==1:
            aus_anz_inKlassen[i]=sum(aus.values())
        else:
            aus_anz_inKlassen[i]=0
            
    for i in range(0,22):
        if i==21:
             leb_anz_inKlassen[i]=sum(nondef.values())
        else:
            leb_anz_inKlassen[i]= 0
                
    
    trenn_AR=[]
    hight=dict()
    deltax=dict()
    bol2=True
    
    last=0
    if aus_sum==0:
        
        ar= -3

    else:
        for key,i in aus_anz_inKlassen.items():
            hight[key]=last+ ((i/aus_sum)/2) 
    
            for k,j in leb_anz_inKlassen.items():
                if bol2 is False:
                    deltax[k] = ((j+i)/sumcum)
                else:
                    deltax[k]=(j/leb_sum)
            last+=(i/aus_sum)
            
        for m in range(0,22):  
    
            trenn_AR.append(deltax[m]*hight[m])
            
        
        ar=sum(trenn_AR)
        print(ar)
        
        return ar


### Implizite Trennschärfe  (AR) ###

def AR_implizit(anz_klassen,pd_zu_stufe):
    
    alive=[]
    default=[]
    for i in range(0,22):
        alive.append(anz_klassen[i]*(1-pd_zu_stufe[i]))
        default.append(anz_klassen[i]*pd_zu_stufe[i])
        
    leb_sum2=sum(alive)
    aus_sum2=sum(default)
    sumcum2 = leb_sum2+aus_sum2    
        
    alive.reverse()
    default.reverse()
    
    last=0
    auc=0
    if aus_sum2==0:
        auc = -1
    else: 
        for h,i in enumerate(default):
            z=last+(i/aus_sum2)/2
            last+=i/aus_sum2
           
            for g,j in enumerate(alive):
                if h==g:
                    y=(j+i)/sumcum2
                else:
                    pass
            auc=auc+y*z 
            
            imp_AR=2*auc-1
    print(imp_AR)        
    return(imp_AR)
            


def heap(arr, n, i): 
    largest = i # Initialize largest as root 
    l = 2 * i + 1     # left = 2*i + 1 
    r = 2 * i + 2     # right = 2*i + 2 
    # See if left child of root exists and is 
    # greater than root 
    if l < n and arr[i] < arr[l]: 
        largest = l 
    # See if right child of root exists and is 
    # greater than root 
    if r < n and arr[largest] <arr[r] : 
        largest = r 
    if largest != i: 
        (arr[i],arr[largest]) = (arr[largest],arr[i]) 
        heap(arr, n, largest) 
 
# The main function 
def heapSortmin(arr): 
    n = len(arr) 
    for i in range(int(n/2)- 1,-1, -1): 
        heap(arr, n, i) 
        
    for i in range(n-1, 0, -1): 
        arr[i], arr[0] = arr[0], arr[i]  
        heap(arr, i, 0) 
    
#%%
def heapify(arr, n, i): 
    smallest = i # Initialize smalles as root  
    l = 2 * i + 1 # left = 2*i + 1  
    r = 2 * i + 2 # right = 2*i + 2  
 
    if l < n and arr[l] < arr[smallest]:  
        smallest = l  
    # If right child is smaller than  
    # smallest so far  
    if r < n and arr[r] < arr[smallest]:  
        smallest = r    
    if smallest != i:  
        (arr[i],arr[smallest]) = (arr[smallest], arr[i]) 
        heapify(arr, n, smallest) 
  
# main function to do heap sort  
def heapSort(arr): 
    n=len(arr)
    # Build heap (rearrange array)  
    for i in range(int(n / 2) - 1, -1, -1): 
        heapify(arr, n, i)  
    for i in range(n-1, -1, -1):           
        # Move current root to end # 
        arr[0], arr[i] = arr[i], arr[0] 
        heapify(arr, i, 0) 

if __name__ == '__main__': 
    heapSort()
    heapSortmin()
    AR_implizit()
    AR_optimal_model()
    AUC_AR_gemessen()
    plot_curve()
    
        

print("Completed.")
