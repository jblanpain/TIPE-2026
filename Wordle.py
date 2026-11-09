#from getopt import long_has_args
from os import chdir
import random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import numpy as np
import simplejson

from fontTools.varLib.instancer import verticalMetricsKeptInSync # utilisé pour un retour coloré

chdir(r"C:\Users\jeanb\Documents\tipe")
#DBfile = open('Wordle5wordsCORRECT', 'r', encoding="utf8")
#ListDB = [e.strip()[:-1].lower() for e in DBfile.readlines()]
#DBfileoffi = open('DBoffi', 'r', encoding="utf8")
#motoublie=open('mot oubliés','r',encoding="utf8")
#DBfileoffi = open('dbof', 'r', encoding="utf8")
#print(DBfileoffi.readlines())
#ListDBoffi = [e.strip()[:-1].lower()[1:-1] for e in DBfileoffi.readlines()][1:-1]
#print(ListDBoffi)
#Listdbpi=[]
#for i in range(len(ListDBoffi)):
    #ListDBoffi[i]=ListDBoffi[i][1:]
#DBfileoffi = open('DBof', 'w', encoding="utf8")
#for e in ListDBoffi:
    #DBfileoffi.write(e+'\n')
#DBfileoffi.close()
#DBfileoffi = open('DBof', 'r', encoding="utf8")
#DBfileoub=open('DBoffi', 'r', encoding="utf8")
#ListDBoffi=[e.strip() for e in DBfileoffi.readlines()]
#ListDBoub=[e.strip() for e in DBfileoub.readlines()]
#ListDBoffi=ListDBoffi+ListDBoub
#DBfileoffi = open('DBoffi', 'r', encoding="utf8")
#for e in ListDBoffi:
    #DBfileoffi.write(e+'\n')
#DBfileoffi.close()
#ListDBoffi=[e.strip() for e in DBfileoffi.readlines()]
with open("ListDBoffi.json", "r", encoding="utf-8") as f:
    ListDBoffi = simplejson.load(f)
with open("dico_freq.json", "r", encoding="utf-8") as f:
    dico_freq4 = simplejson.load(f)
with open("list_lexique4.json", "r", encoding="utf-8") as f:
    LL4 = simplejson.load(f)
Listred=ListDBoffi[:1790]




##------jeu------##
def wordle(mot,reponse):
    if mot not in LL4:
        raise ValueError("pas un mot")
    dico_let_rep={}
    dico_let_mot={}
    list_retour=[]
    retour=""
    if mot == reponse :
        print("\033[32m" + mot + "\033[0m")
        print("Victoire")
        return [[mot[i],2] for i in range(5)]
    for k in range(5): #compte les lettres du mot secret et de l'essai
        if reponse[k] not in dico_let_rep:
            dico_let_rep[reponse[k]]=1
        else:
            dico_let_rep[reponse[k]]+=1
        if mot[k] not in dico_let_mot:
            dico_let_mot[mot[k]]=[[],[],[]] #pour vert,orange,rouge
    for i in range(5):#détecte les lettres vertes
        charrep=reponse[i]
        charmot=mot[i]
        if charrep==charmot:
            dico_let_mot[charmot][0].append(i)
            dico_let_rep[charrep]-=1
    for i in range(5):#détecte les lettres oranges
        charrep = reponse[i]
        charmot = mot[i]
        if charmot in reponse and dico_let_rep[charmot]!=0 and charrep!=charmot:
            dico_let_mot[charmot][1].append(i)
            dico_let_rep[charmot] -= 1
    for i in range(5):#détecte les lettres rouges
        charmot = mot[i]
        if charmot not in dico_let_rep or dico_let_rep[charmot]==0:
            if i not in dico_let_mot[charmot][0] and i not in dico_let_mot[charmot][1]:
                dico_let_mot[charmot][2].append(i)
    for i in range(5):#construit le retour
        charmot = mot[i]
        if i in dico_let_mot[charmot][0]:
            retour = retour + "\033[32m" + charmot + "\033[0m"
            list_retour.append([charmot,2])
        elif i in dico_let_mot[charmot][1]:
            retour = retour + "\033[33m" + charmot + "\033[0m"
            list_retour.append([charmot, 1])
        elif i in dico_let_mot[charmot][2]:
            retour = retour + "\033[31m" + charmot + "\033[0m"
            list_retour.append([charmot, 0])
    print(retour)
    return list_retour

def wordle_np(mot,reponse):
    if mot not in LL4:
        raise ValueError("pas un mot")
    dico_let_rep={}
    dico_let_mot={}
    list_retour=[]
    retour=""
    if mot == reponse :
        return [[mot[i],2] for i in range(5)]
    for k in range(5):
        if reponse[k] not in dico_let_rep:
            dico_let_rep[reponse[k]]=1
        else:
            dico_let_rep[reponse[k]]+=1
        if mot[k] not in dico_let_mot:
            dico_let_mot[mot[k]]=[[],[],[]]
    for i in range(5):
        charrep=reponse[i]
        charmot=mot[i]
        if charrep==charmot:
            dico_let_mot[charmot][0].append(i)
            dico_let_rep[charrep]-=1
    for i in range(5):
        charrep = reponse[i]
        charmot = mot[i]
        if charmot in reponse and dico_let_rep[charmot]!=0 and charrep!=charmot:
            dico_let_mot[charmot][1].append(i)
            dico_let_rep[charmot] -= 1
    for i in range(5):
        charmot = mot[i]
        if charmot not in dico_let_rep or dico_let_rep[charmot]==0:
            if i not in dico_let_mot[charmot][0] and i not in dico_let_mot[charmot][1]:
                dico_let_mot[charmot][2].append(i)
    for i in range(5):
        charmot = mot[i]
        if i in dico_let_mot[charmot][0]:
            retour = retour + "\033[32m" + charmot + "\033[0m"
            list_retour.append([charmot,2])
        elif i in dico_let_mot[charmot][1]:
            retour = retour + "\033[33m" + charmot + "\033[0m"
            list_retour.append([charmot, 1])
        elif i in dico_let_mot[charmot][2]:
            retour = retour + "\033[31m" + charmot + "\033[0m"
            list_retour.append([charmot, 0])
    return list_retour
##------autres------##
def hyper_naif():
    reponse=ListDBoffi[rd.randint(0, len(ListDBoffi) - 1)]
    mot= ListDBoffi[rd.randint(0, len(ListDBoffi) - 1)]
    c=0
    while wordle(mot,reponse)!=True :
        mot = ListDBoffi[rd.randint(0, len(ListDBoffi) - 1)]
        c+=1
    return c

def graph_hyper_naif(essais):
    x=[i for i in range(essais)]
    y=[]
    for k in range(essais):
        y.append(hyper_naif())

    plt.close()
    plt.bar(x,y)
    plt.show()

def comptage(mot):
    dico={}
    for l in mot :
        if l not in dico:
            dico[l]=1
        else :
            dico[l]+=1
    return dico

##------clean elementaire------##
def cleanDB(listDB, repwordle):
    clean = []
    vert = []
    lorange=[]
    orange =[]
    lvert=[]
    lrouge=[]
    rouge = []
    let_connu={}
    for k in range(len(repwordle)):#traitement de l'indice
        c = repwordle[k][1]
        l = repwordle[k][0]
        if c == 0:
            lrouge.append(l)
            rouge.append([l,k])
        elif c == 1:
            orange.append([l,k])
            lorange.append(l)
            if l not in let_connu:
                let_connu[l]=1
            else :
                let_connu[l]+=1
        elif c == 2:
            vert.append([l, k])
            lvert.append(l)
            if l not in let_connu:
                let_connu[l]=1
            else :
                let_connu[l]+=1
    for mot in listDB: #on teste la compatibilité de chaque mot avec les 5 critères
        let_mot=comptage(mot)
        garde=True
        for l in lrouge :
            if l not in lorange and l not in lvert : #si une lettre est rouge, pas verte et pas orange alors elle ne doit pas du tout être dans le mot
                if l in mot:
                    garde=False
            elif l not in let_mot or let_mot[l]!=let_connu[l]: #sinon c'est que la lettre est rouge mais qu'il existe aussi de cette même lettre en vert ou orange dans la réponse,alors le nb de cette lettre en orange ou verte que l'on connait doit être exactement égal au nb que l'on en as dans le mot.
                garde=False
                garde=False
        for L in vert :  ##il manque une lettre verte
            if mot[L[1]]!=L[0]:
                garde=False
        for L in orange :  #une orange est à la même place
            if mot[L[1]]==L[0]:
                garde=False
        for L in rouge :#on a remplacer une "fausse" rouge par une orange
            if mot[L[1]]==L[0]:
                garde=False
        for l in lorange : ##il manque une orange
            if l not in mot or let_connu[l]>let_mot[l]:
                garde=False
        if garde :
            clean.append(mot)
    return clean

##------clean->random------##
def clean_play_rec(list,reponse):
    mot=list[rd.randint(0, len(list) - 1)]
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec(cleanDB(list, pack), reponse)

def clean_play(list):
    reponse=list[rd.randint(0, len(list) - 1)]
    return clean_play_rec(list,reponse)

def bar_clean_ran(k):
    X=[]
    Y=[]
    Xp=[]
    Yp=[]
    S=0
    D={}
    for i in range(1,k+1):
        X.append(i)
        cp=clean_play(LL4)
        Y.append(cp)
        S=S+cp
    #plt.bar(X,Y)
    for e in X:
        nb=Y[e-1]
        if nb in D:
            D[nb]+=1
        else :
            D[nb]=1
    for e in list(D):
        Yp.append(D[e]/k*100)
        Xp.append(e)
    plt.xlabel("nombre d'essais")
    plt.ylabel("fréquence %")
    plt.bar(Xp,Yp)
    print("moy=" + str(S / k))
    plt.close()

def clean_ran_moy_essai(k):
    S=0
    Y=[]
    for i in range(1,k+1):
        cp=clean_play(LL4)
        S=S+cp
        Y.append(cp)
    print("moy="+str(S/k))
    print("ecart-type="+str(np.std(Y)))




##-------prob elementaire------##
def proba_let_ieme_place(i):
    n=len(LL4)
    let={}
    for mot in LL4:
        if mot[i] not in let :
            let[mot[i]]=1
        else :
            let[mot[i]]+=1
    proba_let={}
    for key in let:
        proba_let[key]=let[key]/n
    return proba_let

##------clean->prob->choisi le + probable-------##
def proba_mot(List):
    dico_prob_mot={}
    p0 = proba_let_ieme_place(0)
    p1 = proba_let_ieme_place(1)
    p2 = proba_let_ieme_place(2)
    p3 = proba_let_ieme_place(3)
    p4 = proba_let_ieme_place(4)
    for mot in List:
        prob=p0[mot[0]]*p1[mot[1]]*p2[mot[2]]*p3[mot[3]]*p4[mot[4]]
        dico_prob_mot[mot]=prob
    return dico_prob_mot

def cherche_meilleur_mot(List):
    maxi=0
    dico_prob_mot=proba_mot(List)
    for key in dico_prob_mot:
        if dico_prob_mot[key]>maxi:
            maxi=dico_prob_mot[key]
            motmax=key
    return motmax

def clean_play_rec_prob(List,reponse):
    mot=cherche_meilleur_mot(List)
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_prob(cleanDB(List, pack), reponse)

def clean_play_prob(List):
    reponse=List[rd.randint(0, len(List) - 1)]
    return clean_play_rec_prob(List,reponse)

def bar_clean_prob(k):
    X=[]
    Y=[]
    Xp=[]
    Yp=[]
    S=0
    D={}
    for i in range(1,k+1):
        X.append(i)
        cp=clean_play_prob(LL4)
        Y.append(cp)
        S=S+cp
    #plt.bar(X,Y)
    for e in X:
        nb=Y[e-1]
        if nb in D:
            D[nb]+=1
        else :
            D[nb]=1
    for e in list(D):
        Yp.append(D[e]/k*100)
        Xp.append(e)
    plt.xlabel("nombre d'essais")
    plt.ylabel("fréquence %")
    plt.bar(Xp,Yp)
    print("moy=" + str(S / k))
    plt.show()
    plt.close()

def bar_clean_ranvsprob(k):
    X=[]
    Yp=[]
    Yr=[]
    Dp={}
    Dr={}
    for i in range(1,k+1):
        cpp=clean_play_prob(LL4)
        cpr=clean_play(LL4)
        if cpp in Dp:
            Dp[cpp] += 1
        else:
            Dp[cpp] = 1
        if cpr in Dr:
            Dr[cpr] += 1
        else:
            Dr[cpr] = 1
    xmin=min(min(Dr.keys()),min(Dp.keys()))
    xmax=max(max(Dr.keys()),max(Dp.keys()))
    for x in range(xmin,xmax+1):
        X.append(x)
        if x in Dr:
            Yr.append(Dr[x]/k*100)
        else :
            Yr.append(0)
        if x in Dp:
            Yp.append(Dp[x]/k*100)
        else :
            Yp.append(0)
    plt.bar(np.array(X)-0.2,Yr,width=0.4,color="tab:blue",label="Aléatoire")
    plt.bar(np.array(X) + 0.2, Yp, width=0.4, color="#55A868", label="Score max")
    plt.xlabel("nombre d'essais")
    plt.ylabel("fréquence %")
    legend_elements = [
        Patch(facecolor="tab:blue", label="Aléatoire"),
        Patch(facecolor="#55A868", label="Score max")
    ]

    plt.legend(handles=legend_elements)
    plt.show()
    plt.close()

def clean_prob_moy_essai(k):
    S=0
    Y=[]
    for i in range(1,k+1):
        cp=clean_play_prob(ListDBoffi)
        S=S+cp
        Y.append(cp)
    print("moy="+str(S/k))
    print("ecart-type="+str(std(Y)))


##------clean->prob->choisi la proba mediane/moyenne------##
def prob_mot_et_moy(list):
    n=len(list)
    dico_prob_mot = {}
    p0 = proba_let_ieme_place(0)
    p1 = proba_let_ieme_place(1)
    p2 = proba_let_ieme_place(2)
    p3 = proba_let_ieme_place(3)
    p4 = proba_let_ieme_place(4)
    moy=0
    for mot in list:
        prob = p0[mot[0]] * p1[mot[1]] * p2[mot[2]] * p3[mot[3]] * p4[mot[4]]
        dico_prob_mot[mot] = prob
        moy=moy+prob
    moy=moy/n
    return dico_prob_mot,moy

def cherche_moy_mot(list):
    E=1
    dico_prob_mot=prob_mot_et_moy(list)[0]
    moy=prob_mot_et_moy(list)[1]
    for key in dico_prob_mot:
        if abs(dico_prob_mot[key]-moy)<E:
            motmoy=key
            E=abs(dico_prob_mot[key]-moy)
    return motmoy

def clean_play_rec_prob_moy(List,reponse):
    mot=cherche_moy_mot(List)
    pack=wordle_np(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_prob_moy(cleanDB(List, pack), reponse)

def clean_play_prob_moy(list):
    reponse=list[rd.randint(0, len(list) - 1)]
    return clean_play_rec_prob_moy(list,reponse)

def bar_clean_prob_moy(k):
    X=[]
    Y=[]
    S=0
    for i in range(1,k+1):
        X.append(i)
        cp=clean_play_prob_moy(ListDBoffi)
        Y.append(cp)
        S=S+cp
        plt.bar(X,Y)
    print("moy=" + str(S / k))
    plt.show()
    plt.close()

def clean_prob_moy_moy_essai(k):
    S=0
    Y=[]
    for i in range(1,k+1):
        cp=clean_play_prob_moy(ListDBoffi)
        S=S+cp
        Y.append(cp)
    print("moy="+str(S/k))
    print("ecart-type="+str(std(Y)))

def cherche_med_mot(list):
    n = len(list)
    list_prob_mot=[]
    p0 = proba_let_ieme_place(0)
    p1 = proba_let_ieme_place(1)
    p2 = proba_let_ieme_place(2)
    p3 = proba_let_ieme_place(3)
    p4 = proba_let_ieme_place(4)
    for mot in list:
        prob = p0[mot[0]] * p1[mot[1]] * p2[mot[2]] * p3[mot[3]] * p4[mot[4]]
        list_prob_mot.append([prob,mot])
    list_prob_mot.sort(reverse=True)
    return list_prob_mot[int(n/2)][1]

def clean_play_rec_prob_med(list,reponse):
    mot=cherche_med_mot(list)
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_prob_med(cleanDB(list, pack), reponse)

def clean_play_prob_med(list):
    reponse=list[rd.randint(0, len(list) - 1)]
    return clean_play_rec_prob_med(list,reponse)

def clean_prob_med_moy_essai(k):
    S=0
    Y=[]
    for i in range(1,k+1):
        cp=clean_play_prob_med(ListDBoffi)
        S=S+cp
        Y.append(cp)
    print("moy="+str(S/k))
    print("ecart-type="+str(std(Y)))

##------clean->prob->choisi la pire proba------##
def cherche_pire_mot(list):
    min=1
    dico_prob_mot=proba_mot(list)
    for key in dico_prob_mot:
        if dico_prob_mot[key]<min:
            min=dico_prob_mot[key]
            motmin=key
    return motmin

def clean_play_rec_prob_pire(list,reponse):
    mot=cherche_pire_mot(list)
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_prob_pire(cleanDB(list, pack), reponse)

def clean_play_prob_pire(list):
    reponse=list[rd.randint(0, len(list) - 1)]
    return clean_play_rec_prob_pire(list,reponse)

def bar_clean_prob_pire(k):
    X=[]
    Y=[]
    S=0
    for i in range(1,k+1):
        X.append(i)
        cp=clean_play_prob_pire(ListDBoffi)
        Y.append(cp)
        S=S+cp
        plt.bar(X,Y)
    print("moy=" + str(S / k))
    plt.show()
    plt.close()

def clean_prob_pire_moy_essai(k):
    S=0
    Y= []
    for i in range(1,k+1):
        cp=clean_play_prob_pire(ListDBoffi)
        S=S+cp
        Y.append(cp)
    print("moy="+str(S/k))
    print("ecart-type="+str(std(Y)))

##------clean->prob->choisi meilleur ->last------##

def clean_play_rec_prob_last(list,reponse,repwordle=0):
    if repwordle==0 or len(list)==1:
        mot =cherche_meilleur_mot(list)
    else :
        c=0
        for k in range(len(repwordle)):
            if repwordle[k][1]==2:
                c+=1
            else :
                indice_der=k
        if c!=4 or len(list)==1:
            mot=cherche_meilleur_mot(list)
        else:
            l_possible=[]
            for mot in list:
                l_possible.append(mot[indice_der])
            maxi=0
            for motglob in ListDBoffi:
                c2=0
                for l in l_possible:
                    if l in motglob:
                        c2+=1
                if c2>maxi:
                    maxi=c2
                    mot_max=motglob
            mot=mot_max
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_prob_last(cleanDB(list, pack), reponse,pack)

def clean_play_prob_last(list):
    reponse = list[rd.randint(0, len(list) - 1)]
    return clean_play_rec_prob_last(list,reponse)

def clean_prob_last_moy_essai(k):
    S = 0
    Y = []
    for i in range(1, k + 1):
        cp = clean_play_prob_last(ListDBoffi)
        S = S + cp
        Y.append(cp)
    print("moy=" + str(S / k))
    print("ecart-type=" + str(std(Y)))

##------recherche du mot reduisant le plus la db------##
def redu(List1,List2): ##List 1 :liste des mots à essayer en 1er mot ##List 2 :liste des réponses à essayer
    n=len(List2)
    dico={}
    for mot in List1 :
        S=0
        for sol in List2:
            S+=len(cleanDB(List2,wordle_np(mot,sol)))
            dico[mot]=S/n
    return dico

##------last for all-----##
def clean_play_rec_lastforall(list,reponse,strat,crit,critlen,predef="",repwordle=0,bool=False,):#crit:à partir de cb de lettre non trouve la methode commence #le bool indique si lessai davant a deja mis en place la strat lastforall
    if strat=="ran":                                                                         #strat :srategie mise en place parmis :(ran,max,mid,med,min,predef-max)
        choix=list[rd.randint(0, len(list) - 1)]
    elif strat=="max":
        choix=cherche_meilleur_mot(list)
    elif strat=="mid":
        choix=cherche_moy_mot(list)
    elif strat=="med":
        choix=cherche_med_mot(list)
    elif strat=="min":
        choix=cherche_pire_mot(list)
    elif repwordle==0 and strat=="predef-max":
        choix=predef
    elif strat=="predef-max":
        choix=cherche_meilleur_mot(list)
    if repwordle==0:
        mot=choix
    else :
        vert=[]
        ind_restant=[]
        for i in range(len(repwordle)):
            if not repwordle[i][1]==2:
                ind_restant.append(i)#vert.append([repwordle[i][0],i])
        c=len(ind_restant)
        if len(list)<=critlen:  # a partir de cb de mot dans la base de donne restante la methode nest pas appliquer
            bool=False
            mot = choix
        elif c>crit or bool:  #a partir de cb de lettre non trouve la methode commence
            bool=False
            mot = choix
        else :
            bool=True
            l_possible=[]
            for mot_c in list:
                for i in ind_restant:
                    l_possible.append(mot_c[i])
            maxi=0
            for motglob in ListDBoffi :
                c2=0
                for l in motglob:
                    if l in l_possible:
                        c2+=1
                if c2>maxi:
                    maxi=c2
                    mot=motglob
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_lastforall(cleanDB(list, pack), reponse,strat,crit,critlen,predef,pack,bool)

def clean_play_lastforall(list,strat,crit,critlen,predef=""):
    reponse = list[rd.randint(0, len(list) - 1)]
    return clean_play_rec_lastforall(list,reponse,strat,crit,critlen,predef)

def clean_lastforall_moy_essai(k,strat,crit,critlen,predef=""):
    S = 0
    Y = []
    for i in range(1, k + 1):
        cp = clean_play_lastforall(ListDBoffi,strat,crit,critlen,predef)
        S = S + cp
        Y.append(cp)
    moy=S/k
    e=std(Y)
    print("moy=" + str(moy))
    print("ecart-type=" + str(e))
    return moy,e

def clean_lastforall_moy_essaibis(strat,crit,critlen,predef=""):
    S = 0
    Y = []
    for r in ListDBoffi:
        cp = clean_play_rec_lastforall(ListDBoffi,r,strat,crit,critlen,predef)
        S = S + cp
        Y.append(cp)
    moy=S/len(ListDBoffi)
    return moy



#clean_lastforall_moy_essai(100,"predef-max",3,3,"tarie")

##------graphique comparaison criteres lastforall-----##
def graph_comp_crit_lastforall(essai):  #meilleur crit=2
    plt.close()
    MOY=[]
    E=[]
    for crit in range(0,6):
        L=[]
        nb_esssai={}
        x=[]
        y=[]
        for k in range(1,essai+1):
            cp=clean_play_lastforall(ListDBoffi,"max",crit,)
            L.append(cp)
            if cp in nb_esssai:
                nb_esssai[cp]+=1
            else:
                nb_esssai[cp]=1
        for key in nb_esssai:
            x.append(key)
        x.sort()

        for e in x:
            y.append(nb_esssai[e]/essai)
        MOY.append(float(mean(L)))
        E.append(float(std(L)))
        plt.plot(x,y,label="crit="+str(crit))
    print(MOY,E)
    plt.legend()
    plt.show()

def graph_comp_lastforall(essai,critlenlim):
    plt.close()
    MOY=[]
    E=[]
    for crit in [2,3]:
        x = []
        moy = []
        e = []
        for critlen in range(1,critlenlim):
            S=0
            L=[]
            for k in range(1,essai+1):
                print(crit,critlen)
                cp=clean_play_lfa_double_predef(ListDBoffi,"predef-max",crit,critlen,"parie")
                L.append(cp)
                S+=cp
            x.append(critlen)
            moy.append(S/essai)
            MOY.append([(crit,critlen),S/essai])
            E.append([(crit, critlen),float(std(L))])
            e.append(float(std(L)))
        plt.figure("moyennes")
        plt.plot(x,moy,label="crit 1="+str(crit))
        plt.figure("écart-type")
        plt.plot(x, e, label="crit 1=" + str(crit))
    print(MOY,E)
    plt.figure("moyennes")
    plt.xlabel("crit 2")
    plt.ylabel("moyennes")
    plt.figure("écart-type")
    plt.xlabel("crit 2")
    plt.ylabel("écart-type")
    plt.legend()
    plt.show()



##------comparaison du 2eme critere lastforall(taille de la liste pour commencer la meth)-----##
def graph_comp_critlen_lastforall(essai):##meilleur critlen=3
    plt.close()
    MOY=[]
    E=[]
    for critlen in range(0,10):
        L=[]
        nb_esssai={}
        x=[]
        y=[]
        for k in range(1,essai+1):
            cp=clean_play_lastforall(ListDBoffi,2,critlen)
            L.append(cp)
            if cp in nb_esssai:
                nb_esssai[cp]+=1
            else:
                nb_esssai[cp]=1
        for key in nb_esssai:
            x.append(key)
        x.sort()

        for e in x:
            y.append(nb_esssai[e]/essai)
        MOY.append(float(mean(L)))
        E.append(float(std(L)))
        plt.plot(x,y,label="critlen="+str(critlen))
    print(MOY,E)
    plt.legend()
    plt.show()##

#graph_comp_critlen_lastforall(10)

##------recherche meilleur mot sans repetition-------##
def sans_rep():
    listtest=ListDBoffi.copy()
    c=0
    while c<5:
        c=0
        mot=cherche_meilleur_mot(listtest)
        dico=comptage(mot)
        for key in dico:
            if dico[key]>1:
                listtest.remove(mot)
            else:
                c+=1
        print(mot)

##-------volonte d'opti le last(pas fonctionnelle)-------- ##
def cindrestant_lpossible_clposstot(list):
    dico_l_possible={}
    cindrestant=0
    clposstot=0
    for i in range(len(list[0])):
        lettres={}
        for mot in list:
            l=mot[i]
            if l not in lettres:
                lettres[l]=1
            else :
                lettres[l]+=1
        if len(lettres)>1:#alors tous les mots de la liste n'ont opas la meme lettre en i
            cindrestant+=1
            for key in lettres:
                clposstot+=lettres[key]
                if key in dico_l_possible:
                    dico_l_possible[key]+=lettres[key]
                else :
                    dico_l_possible[key]=lettres[key]
    return cindrestant,dico_l_possible,clposstot

def clean_play_rec_betterlastforall(list,reponse,strat,crit,critlen,repwordle=0,bool=False,listtot=ListDBoffi.copy()):#crit:à partir de cb de lettre non trouve la methode commence #le bool indique si lessai davant a deja mis en place la strat lastforall
    if strat=="ran":                                                                         #strat :srategie mise en place parmis :(ran,max,mid,med,min)
        choix=list[rd.randint(0, len(list) - 1)]
    elif strat=="max":
        choix=cherche_meilleur_mot(list)
    elif strat=="mid":
        choix=cherche_moy_mot(list)
    elif strat=="med":
        choix=cherche_med_mot(list)
    elif strat=="min":
        choix=cherche_pire_mot(list)
    if repwordle==0 or len(list)<=critlen:# critlen:a partir de cb de mot dans la base de donne restante la methode nest pas appliquer
        bool=False
        mot=choix
    else :
        c,dico_l_possible,c_l_possible=cindrestant_lpossible_clposstot(list)
        if c>crit or bool:  #a partir de cb de lettre non trouve la methode commence
            bool=False
            mot = choix
        else :#ici commence le last
            bool=False
            maxi=0
            mots_max=[]
            for motglob in listtot :
                c2=0
                for l in motglob:
                    if l in dico_l_possible:
                        c2+=1
                if c2>maxi:
                    maxi=c2
                    mots_max=[motglob]
                elif c2==maxi:
                    mots_max.append(motglob)
            list_prob_last=[]
            for e in mots_max:
                prob=1
                for l in e:
                    if l in dico_l_possible:
                        prob=prob*dico_l_possible[l]/c_l_possible
                list_prob_last.append([prob,e]) ##attention au eventuelles repetitions de lettre qui favoriserai la monte de la prob dun mot
            list_prob_last.sort(reverse=True)
            mot=list_prob_last[0][1]
            listtot.remove(mot)
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_betterlastforall(cleanDB(list, pack), reponse,strat,crit,critlen,pack,bool)

def clean_play_betterlastforall(list,strat,crit,critlen):
    reponse = list[rd.randint(0, len(list) - 1)]
    return clean_play_rec_betterlastforall(list,reponse,strat,crit,critlen)

def clean_betterlastforall_moy_essai(k,strat,crit,critlen):
    S = 0
    Y = []
    for i in range(1, k + 1):
        cp = clean_play_betterlastforall(ListDBoffi,strat,crit,critlen)
        S = S + cp
        Y.append(cp)
    moy=S/k
    e=std(Y)
    print("moy=" + str(moy))
    print("ecart-type=" + str(e))
    return moy,e

#------cherche meilleur predef------#
def premier_mot():
    mot_min=LL4[0]
    min=100
    for e in LL4:
        moy=clean_lastforall_moy_essaibis("predef-max",3,3,e)
        if moy<min:
            mot_min=e
            min=moy
    return mot_min,min

def premier_mot_predef():#vachement trop long
    mot_min=LL4[0]
    min=100
    memo={}
    dico_predef={}
    for e in LL4:
        S = 0
        for rep in LL4:
            cp = rec_play_lfa_memoisation(LL4, rep, "predef-max", 2, 3, e, memo)
            S = S + cp
        moy = S / len(LL4)
        dico_predef[e]=moy
        if moy<min:
            mot_min=e
            min=moy
    print(mot_min)
    print(min)
    print(dico_predef)
    return mot_min,m

##------Distance de Levenshtein------##
def d_lev(c1,c2):
    n=len(c1)
    m=len(c2)
    c1t=c1[1:]
    c2t=c2[1:]
    if min([n,m])==0:
        return max([n,m])
    elif c1[0]==c2[0]:
        return d_lev(c1t,c2t)
    else:
        return 1+min([d_lev(c1t,c2),d_lev(c1,c2t),d_lev(c1t,c2t)])
    ##c'est nul ca compte juste le nb de lettre pas verte

##-------double predef-------##

def clean_play_rec_lfa_double_predef(list,reponse,strat,crit,critlen,predef=["",""],n=0):
    if strat=="ran":                                                                         #strat :srategie mise en place parmis :(ran,max,mid,med,min,predef-max,double-predef-max)
        choix=list[rd.randint(0, len(list) - 1)]                                             #avant jamais 2 last d'affiler mais ca a changer
    elif strat=="max":
        choix=cherche_meilleur_mot(list)
    elif strat=="mid":
        choix=cherche_moy_mot(list)
    elif strat=="med":
        choix=cherche_med_mot(list)
    elif strat=="min":
        choix=cherche_pire_mot(list)
    elif n==0 and strat=="predef-max":
        choix=predef
    elif strat=="predef-max":
        choix=cherche_meilleur_mot(list)
    elif strat=="double-predef-max":
        if n==0:
            choix=predef[0]
        elif n==1:
            choix=predef[1]
        else:
            choix=cherche_meilleur_mot(list)
    if n==0:
        mot=choix
    else :
        ind_restant=[]
        lvert=[]
        for i in range(5):
            l=list[0][i]
            lettre_verte=True
            ind=0
            while (lettre_verte==True) and ind<len(list) :
                if list[ind][i]!=l:
                    ind_restant.append(i)
                    lettre_verte=False
                ind+=1
            if lettre_verte:
                lvert.append(l)
        c=len(ind_restant)      # c compte le nb de lettre pas vertes
        anagramme=True #si list=["etape","epate"] et quon essaie petit pour le last on tourne en rond
        m=0
        while anagramme==True and m<len(list)-1:
            if comptage(list[m])!=comptage(list[m+1]):
                anagramme=False
            m+=1
        if len(list)<=critlen or len(list)==1 or anagramme:  # a partir de cb de mot dans la base de donne restante la methode nest pas appliquer
            mot = choix
        elif c>crit :  #a partir de cb de lettre non trouve la methode commence
            mot = choix
        else :
            l_possible=[]
            for mot_c in list:
                for i in ind_restant:
                    l_possible.append(mot_c[i])
            maxi=0
            for motglob in LL4 :
                c2=0
                l_possiblebis=l_possible.copy()
                lvertbis = lvert.copy()
                for l in motglob:
                    if l in l_possiblebis:
                        if l in lvertbis:
                            lvertbis.remove(l)
                        else:
                            c2+=1
                            while l in l_possiblebis:
                                l_possiblebis.remove(l)
                if c2>maxi:
                    maxi=c2
                    mot=motglob
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+clean_play_rec_lfa_double_predef(cleanDB(list, pack), reponse,strat,crit,critlen,predef,n+1)

def clean_play_lfa_double_predef(list,strat,crit,critlen,predef=["",""]):
    reponse = list[rd.randint(0, len(list) - 1)]
    return clean_play_rec_lfa_double_predef(list,reponse,strat,crit,critlen,predef)

def clean_lfa_double_predef_moy_essai(k,list,strat,crit,critlen,predef=["",""]):
    S = 0
    Y = []
    for i in range(1, k + 1):
        cp = clean_play_lfa_double_predef(list,strat,crit,critlen,predef)
        S = S + cp
        Y.append(cp)
    moy=S/k
    e=std(Y)
    print("moy=" + str(moy))
    print("ecart-type=" + str(e))
    return moy,e

def moyenne_abs(strat,crit,critlen,predef=["",""]):##on entend par moyenne absolue le fait de tester tout les mots donc le moy abs est tjr la meme avec les meme entrees
    S = 0
    Y = []
    for rep in LL4:
        cp = clean_play_rec_lfa_double_predef(LL4,rep, strat, crit, critlen, predef)
        S = S + cp
        Y.append(cp)
    moy = S / len(LL4)
    e = std(Y)
    print("moy=" + str(moy))
    print("ecart-type=" + str(e))
    return moy, e

##------force brut couple ------##
def force_brut_double_predef():#alors ça marche surement mais le temps de calcul est estimé autour de 44 233 jours peut etre utile en def m1="parie" alors environ 8jours
    moy_min=50
    couple_min=("","")
    for m1 in ListDBoffi:
        for m2 in ListDBoffi:
            S=0
            for r in ListDBoffi:
                partie=clean_play_rec_lfa_double_predef(ListDBoffi,r,"double-predef-max",2,3,[m1,m2])
                S=S+partie
            moy=S/len(ListDBoffi)
            if moy<moy_min:
                moy_min=moy
                couple_min=(m1,m2)
    return moy_min,couple_min

##------fonction qui joue sur la page officiel------##

def rec_play_web(list,strat,crit,critlen,driver,main,body,predef=["",""],n=0):
    if strat=="ran":                                                                         #strat :srategie mise en place parmis :(ran,max,mid,med,min,predef-max,double-predef-max)
        choix=list[rd.randint(0, len(list) - 1)]
    elif strat=="max":
        choix=cherche_meilleur_mot(list)
    elif strat=="mid":
        choix=cherche_moy_mot(list)
    elif strat=="med":
        choix=cherche_med_mot(list)
    elif strat=="min":
        choix=cherche_pire_mot(list)
    elif n==0 and strat=="predef-max":
        choix=predef
    elif strat=="predef-max":
        choix=cherche_meilleur_mot(list)
    elif strat=="double-predef-max":
        if n==0:
            choix=predef[0]
        elif n==1:
            choix=predef[1]
        else:
            choix=cherche_meilleur_mot(list)
    if n==0:
        mot=choix
    else :
        ind_restant=[]
        for i in range(5):
            l = list[0][i]
            lettre_verte = True
            ind = 0
            while (lettre_verte == True) and ind < len(list):
                if list[ind][i] != l:
                    ind_restant.append(i)
                    lettre_verte = False
                ind += 1
        c=len(ind_restant)
        if len(list)<=critlen:  # à partir de cb de mot dans la base de donne restante la methode nest pas appliquer
            mot = choix
        elif c>crit:  #à partir de cb de lettre non trouve la methode commence
            mot = choix
        else :
            l_possible=[]
            for mot_c in list:
                for i in ind_restant:
                    l_possible.append(mot_c[i])
            maxi=0
            for motglob in ListDBoffi :
                c2=0
                l_possiblebis=l_possible.copy()
                for l in motglob:
                    if l in l_possible:
                        c2+=1
                        while l in l_possiblebis: #pour eviter de valoriser assis parce que il a plein de s par ex#
                            l_possiblebis.remove(l)
                if c2>maxi:
                    maxi=c2
                    mot=motglob
    body.send_keys(mot + Keys.ENTER)
    #victoire=main.find_elements("class name","endgame-modal")
    lettres = main.find_elements("id", "letter-container")
    L = []
    loose=True
    for i in range(len(lettres)):
        lettre = lettres[i]
        if lettre.get_attribute('class') == "has-letter validated correct":
            L.append([lettre.text.lower(), 2])
        elif lettre.get_attribute('class') == "has-letter validated incorrect":
            L.append([lettre.text.lower(), 0])
        elif lettre.get_attribute('class') == "has-letter validated partial":
            L.append([lettre.text.lower(), 1])
        else:
            loose=False
    vic = True
    for e in L[len(L)-5:]:
        if e[1]!=2:
            vic=False
    if vic:
        return 1
    elif loose:
        print("Défaite")
        input()
        quit()
    else:
        pack=L[len(L)-5:]
        return 1+rec_play_web(cleanDB(list, pack),strat,crit,critlen,driver,main,body,predef,n+1)

def play_web(list,strat,crit,critlen,predef=["",""]):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://wordle.louan.me/")
    body = driver.find_element("tag name", "body")
    header=body.find_element("tag name", "header")
    main = body.find_element("tag name", "main")
    close = main.find_element("class name", "close-btn")
    close.click()
    archive=header.find_element("class name", "archives")
    archive.click()
    previous=header.find_element("class name", "archives-date-previous")
    n=rd.randint(0,100)
    for i in range(n):
        ()
        previous.click()
    essai=rec_play_web(list,strat,crit,critlen,driver,main,body,predef)
    input()
    driver.quit()
    return essai

#play_web(Listred,"predef-max",3,3,"parie")
#clean_play_rec_lfa_double_predef(ListDBoffi,"sones","predef-max",1,0,"parie",)
#graph_comp_lastforall(10000,5)
#l1=cleanDB(ListDBoffi,[['p',0],['a',0],['r',0],['i',0],['e',2]])
#l2=cleanDB(l1,[['c',0],['o',1],['l',0],['e',0],['e',2]])
#l3=cleanDB(ListDBoffi,[['z',0],['o',2],['n',2],['e',2],['s',2]])
#print(l3)


#['cones', 'lones', 'gones', 'sones', 'nones','zones']

##au dernieres nouvellles meilleur crit,critlen pour predef-max parie =3,3

#le temps de calcul sur les last crit 3 est exessif faut opti ou definir un critlenmax cad on fait pas le last si ya trop de mot deans la db

##------evolution de la moyenne par rapportr a la lo    ngeur de la DB------##
def evo_long_DB(list,pas,essai,strat,crit,critlen,predef=["",""]):
    plt.close()
    X=[]
    Y=[]
    for long in range(pas,len(list),pas):
        listact=sample(list,long)
        moy=clean_lfa_double_predef_moy_essai(essai,listact,strat,crit,critlen,predef)[0]
        Y.append(moy)
        X.append(long)
    plt.plot(X,Y)
    plt.show()

#evo_long_DB(ListDBoffi,100,100,"predef-max",2,3,"parie") pas hyper utile ca fait un truc qui ressmble grossiermeent a un ln er

##avec crit=3 ca prend des plombes quand coup 1 il trouve 2 lettre(souvent) il recherche tjr le meme last et cest long faurdait stocker les last deja trouver

##--------memoisation pour le last-------##
def rec_play_lfa_memoisation(list,reponse,strat,crit,critlen,predef=["",""],memo={},n=0):

    if strat=="ran":         #strat :srategie mise en place parmis :(ran,max,mid,med,min,predef-max,double-predef-max)
        choix=list[rd.randint(0, len(list) - 1)]
    elif strat=="max":
        choix=cherche_meilleur_mot(list)
    elif strat=="mid":
        choix=cherche_moy_mot(list)
    elif strat=="med":
        choix=cherche_med_mot(list)
    elif strat=="min":
        choix=cherche_pire_mot(list)
    elif n==0 and strat=="predef-max":
        choix=predef
    elif strat=="predef-max":
        choix=cherche_meilleur_mot(list)
    elif strat=="double-predef-max":
        if n==0:
            choix=predef[0]
        elif n==1:
            choix=predef[1]
        else:
            choix=cherche_meilleur_mot(list)
    if n==0: #pas de last au premier coups
        mot=choix
    else :
        ind_restant=[]
        lvert=[]
        for i in range(5):
            l=list[0][i]
            lettre_verte=True
            ind=0
            while (lettre_verte==True) and ind<len(list) :
                if list[ind][i]!=l:
                    ind_restant.append(i)
                    lettre_verte=False
                ind+=1
            if lettre_verte:
                lvert.append(l)
        c=len(ind_restant)      # c compte le nb de lettre pas vertes
        anagramme=True #si list=["etape","epate"] et que l'on essaie petit pour le last on tourne en rond alors on ne doit pas faire le last
        m=0
        while anagramme==True and m<len(list)-1: #on verifie si la situation ne possède que des anagrammes
            if comptage(list[m])!=comptage(list[m+1]):
                anagramme=False
            m+=1
        if len(list)<=critlen or len(list)==1 or anagramme:  # critlen:a partir de cb de mot dans la base de donne restante la methode nest pas appliquer
            mot = choix
        elif c>crit :  #crit: à partir de cb de lettre non trouvé la méthode commence
            mot = choix
        else :#à partir d'ici on applique le last
            l_possible=[]
            for mot_c in list: #on complète l'ensemble des lettres possibles
                for i in ind_restant:
                    if mot_c[i] not in l_possible:
                        l_possible.append(mot_c[i])
            t_ind_restant=tuple(ind_restant)
            t_l_possible=tuple(l_possible)
            if (t_ind_restant,t_l_possible) in memo: #on regarde si cette recherche de last a déjà été traitée
                mot=memo[(t_ind_restant,t_l_possible)]
                print("used")
            else:
                maxi=0 #on cherche le mot regroupant le plus de lettre possible
                for motglob in LL4 :
                    c2=0
                    l_possiblebis=l_possible.copy()
                    lvertbis = lvert.copy()
                    for l in motglob:
                        if l in l_possiblebis:
                            if l in lvertbis:
                                lvertbis.remove(l)
                            else:
                                c2+=1
                                while l in l_possiblebis:#on évite de favoriser les mots avec plusieurs fois la même lettre
                                    l_possiblebis.remove(l)
                    if c2>maxi:
                        maxi=c2
                        mot=motglob
                memo[(t_ind_restant,t_l_possible)]=mot
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+rec_play_lfa_memoisation(cleanDB(list, pack), reponse,strat,crit,critlen,predef,memo,n+1)

def play_lfa_memoisation(list,strat,crit,critlen,predef=["",""]):#sert pas à grand chose car la mémoisation est utile si on joue plusieurs fois
    reponse = list[rd.randint(0, len(list) - 1)]
    return rec_play_lfa_memoisation(list,reponse,strat,crit,critlen,predef)

def moyenne_abs_memo(list,strat,crit,critlen,predef=["",""]):##on entend par moyenne absolue le fait de tester tout les mots donc le moy abs est tjr la meme avec les meme entrees
    S = 0
    Y = []
    memo={}
    for rep in list:
        cp = rec_play_lfa_memoisation(list,rep, strat, crit, critlen,predef,memo)
        S = S + cp
        Y.append(cp)
    moy = S / len(list)
    e = std(Y)
    print("moy=" + str(moy))
    print("ecart-type=" + str(e))
    return moy, e

#regarder si on a vrm gagner du temps mais jpense que oui

def bar_paslastvslast(k):
    X=[]
    Yl=[]
    Y=[]
    Dl={}
    D={}
    for i in range(1,k+1):
        cpl=clean_play_lfa_double_predef(LL4,"predef-max",2,3,"parie")
        cp=clean_play_prob(LL4)
        if cpl in Dl:
            Dl[cpl] += 1
        else:
            Dl[cpl] = 1
        if cp in D:
            D[cp] += 1
        else:
            D[cp] = 1
    xmin=min(min(D.keys()),min(Dl.keys()))
    xmax=max(max(D.keys()),max(Dl.keys()))
    for x in range(xmin,xmax+1):
        X.append(x)
        if x in D:
            Y.append(D[x]/k*100)
        else :
            Y.append(0)
        if x in Dl:
            Yl.append(Dl[x]/k*100)
        else :
            Yl.append(0)
    plt.bar(np.array(X)-0.2,Y,width=0.4,color="tab:blue",label="Sans le last")
    plt.bar(np.array(X) + 0.2, Yl, width=0.4, color="#55A868", label="Avec le last")
    plt.xlabel("nombre d'essais")
    plt.ylabel("fréquence %")
    legend_elements = [
        Patch(facecolor="tab:blue", label="Sans le last"),
        Patch(facecolor="#55A868", label="Avec le last")
    ]

    plt.legend(handles=legend_elements)
    plt.show()
    plt.close()


##------attribution d'une frequence de tirage a chaque mot-------## (abandonné)

def caractere_bzr(doc):
    ouvrage = open(doc, 'r', encoding="utf8")
    l_bzr=[]
    for mot in ouvrage.readlines():
        for l in mot.lower() :
            if l not in list("abcdefghijklmnopqrstuvwxyz") and l not in l_bzr :
                l_bzr.append(l)
    return l_bzr

def etablir_freq_mots():
    ouvrage= open('Ouvrage 1 Dico.txt', 'r', encoding="utf8")
    frequence=open('frequence mot', 'w', encoding="utf8")
    dico={'à':'a', 'â':'a', 'é':'e', 'è':'e', 'î':'i', 'ê':'e', 'û':'u', 'ô':'o', 'ç':'c', 'ï':'i', 'ë':'e', 'A':'a', 'ü':'u', 'E':'e', 'F':'f', 'G':'g', 'U':'u', 'T':'t', 'D':'d', 'H':'h', 'I':'i', 'S':'s', 'P':'p', 'L':'l', 'ä':'a', 'M':'m', 'ö':'o', 'N':'n', 'O':'o', 'ù':'u', 'Q':'q', 'R':'r', 'V':'v', 'W':'w'}
    for mot in ouvrage.readlines():
        if len(mot)==6:#car ya un \n
            for i in range(len(mot)):
                if mot[i] in ['à', 'â', 'é', 'è', 'î', 'ê', 'û', 'ô', 'ç', 'ï', 'ë', 'A', 'ü', 'E', 'F', 'G', 'U', 'T', 'D', 'H', 'I', 'S', 'P', 'L', 'ä', 'M', 'ö', 'N', 'O', 'ù', 'Q', 'R', 'V', 'W'] :
                    mot = mot[:i] + dico[mot[i]] + mot[i+1:]
            if '-' not in mot:
                frequence.write(mot)
    mots=[] #pour enlever les doubles
    freq_mots={}
    frequence=open('frequence mot', 'r', encoding="utf8")
    for ligne in frequence:
        mot=ligne.strip()
        if mot not in mots:
            mots.append(mot)
    frequence=open('frequence mot', 'w', encoding="utf8")
    for mot in mots:
        frequence.write(mot+"\n")
        freq_mots[mot]=1/len(mots)
    n=len(freq_mots)
    return n,freq_mots

def contribution_culturelle(doc,ntot=0,freq_preced={}):
    ouvrage = open(doc, 'r', encoding="utf8")
    l_bzr=caractere_bzr(doc)
    n,freq_mot=etablir_freq_mots()
    if freq_preced!={}:
        freq_mot=freq_preced
        n=ntot
    mots=[]
    motf=[]
    dico={'à':'a', 'â':'a','é':'e', 'é':'e', 'è':'e', 'î':'i', 'ê':'e', 'û':'u', 'ô':'o', 'ç':'c', 'ï':'i', 'ë':'e', 'ü':'u', 'ä':'a', 'ö':'o','ù':'u','œ':'oe','æ':'ae'}
    for ligne in ouvrage.readlines():
        mots=mots+ligne.split()
    for mot in mots:
        keep=True
        for i in range(len(mot)):
            if mot[i] in l_bzr and mot[i] not in ['.',',','à', 'â', 'é', 'è', 'î', 'ê', 'û', 'æ', 'œ', 'ô', 'ç', 'ï', 'ë', 'ü', 'ä', 'ö', 'ù'] :
                keep=False
            elif mot[i] in ['à', 'â','é','è', 'î', 'ê', 'û', 'æ', 'œ', 'ô', 'ç', 'ï', 'ë', 'ü', 'ä', 'ö', 'ù']:
                mot = mot[:i] + dico[mot[i]] + mot[i + 1:]
        mot = mot.lower()
        mot= "".join(c for c in mot if c.isalpha())
        if len(mot)==5 and keep==True :
            motf.append(mot)
    tot_mot_ouvrage = len(motf)
    for mot in freq_mot:
        if mot not in motf :
            nb_app_ouvrage=0
        else:
            nb_app_ouvrage=motf.count(mot)
        freq_mot[mot]=(freq_mot[mot]*n+nb_app_ouvrage)/(n+tot_mot_ouvrage)
    n=n+tot_mot_ouvrage
    return n,freq_mot

def dico_max(dico):
    cle_max = None
    val_max = -float("inf")
    for k, v in dico.items():
        if v > val_max:
            val_max = v
            cle_max = k
    return(cle_max, val_max)


#---utilisation des fréquence lexicale----#
def cherche_meilleur_mot_lex(List,p):#p est le poids accordé au score initial
    maxi=0
    dico_prob_mot=proba_mot(List)
    for key in dico_prob_mot:
        if (dico_prob_mot[key])**p*dico_freq4[key]>=maxi:
            maxi=(dico_prob_mot[key])**p*dico_freq4[key]
            motmax=key
    return motmax

def rec_play_lfa_memoisation_lex(list,reponse,strat,crit,critlen,p,predef=["",""],memo={},n=0):
    if strat=="ran":                                                                         #strat :srategie mise en place parmis :(ran,max,mid,med,min,predef-max,double-predef-max)
        choix=list[rd.randint(0, len(list) - 1)]                                             #avant jamais 2 last d'affiler mais ca a changer
    elif strat=="max":
        choix=cherche_meilleur_mot_lex(list,p)
    elif strat=="mid":
        choix=cherche_moy_mot(list)
    elif strat=="med":
        choix=cherche_med_mot(list)
    elif strat=="min":
        choix=cherche_pire_mot(list)
    elif n==0 and strat=="predef-max":
        choix=predef
    elif strat=="predef-max":
        choix=cherche_meilleur_mot_lex(list,p)
    elif strat=="double-predef-max":
        if n==0:
            choix=predef[0]
        elif n==1:
            choix=predef[1]
        else:
            choix=cherche_meilleur_mot(list)
    if n==0:
        mot=choix
    else :
        ind_restant=[]
        lvert=[]
        for i in range(5):
            l=list[0][i]
            lettre_verte=True
            ind=0
            while (lettre_verte==True) and ind<len(list) :
                if list[ind][i]!=l:
                    ind_restant.append(i)
                    lettre_verte=False
                ind+=1
            if lettre_verte:
                lvert.append(l)
        c=len(ind_restant)      # c compte le nb de lettre pas vertes
        anagramme=True #si list=["etape","epate"] et quon essaie petit pour le last on tourne en rond alors on ne doit pas faire le last
        m=0
        while anagramme==True and m<len(list)-1:
            if comptage(list[m])!=comptage(list[m+1]):
                anagramme=False
            m+=1
        if len(list)<=critlen or len(list)==1 or anagramme:  # a partir de cb de mot dans la base de donne restante la methode nest pas appliquer
            mot = choix
        elif c>crit :  #a partir de cb de lettre non trouve la methode commence
            mot = choix
        else :#on fait le last
            l_possible=[]
            for mot_c in list:
                for i in ind_restant:
                    if mot_c[i] not in l_possible:
                        l_possible.append(mot_c[i])
            maxi=0
            t_ind_restant=tuple(ind_restant)
            t_l_possible=tuple(l_possible)
            if (t_ind_restant,t_l_possible) in memo:
                mot=memo[(t_ind_restant,t_l_possible)]
                print("used")
            else:
                for motglob in LL4 :
                    c2=0
                    l_possiblebis=l_possible.copy()
                    lvertbis = lvert.copy()
                    for l in motglob:
                        if l in l_possiblebis:
                            if l in lvertbis:
                                lvertbis.remove(l)
                            else:
                                c2+=1
                                while l in l_possiblebis:
                                    l_possiblebis.remove(l)
                    if c2>maxi:
                        maxi=c2
                        mot=motglob
                memo[(t_ind_restant,t_l_possible)]=mot
    pack=wordle(mot,reponse)
    if mot==reponse:
        return 1
    else:
        return 1+rec_play_lfa_memoisation_lex(cleanDB(list, pack), reponse,strat,crit,critlen,p,predef,memo,n+1)

def play_lfa_memoisation_lex(liste,strat,crit,critlen,p,predef=["",""]):#sert pas à grand chose car la mémoisation est utile si on joue plusieurs fois
    reponse = rd.choices(list(dico_freq4.keys()), weights=list(dico_freq4.values()), k=1)[0]
    return rec_play_lfa_memoisation_lex(liste,reponse,strat,crit,critlen,p,predef)

def moyenne_memo_lex(liste,k,strat,crit,critlen,p,predef=["",""]):##on entend par moyenne absolue le fait de tester tout les mots donc le moy abs est tjr la meme avec les meme entrees
    S = 0
    Y = []
    memo={}
    d=0
    for i in range(k):
        rep=rd.choices(list(dico_freq4.keys()), weights=list(dico_freq4.values()), k=1)[0]
        cp = rec_play_lfa_memoisation_lex(liste,rep, strat, crit, critlen,p,predef,memo)
        if cp>6:
            d+=1
        S = S + cp
        Y.append(cp)
    moy = S / k
    e =np.std(Y)
    print("moy=" + str(moy))
    print("ecart-type=" + str(e))
    print("nombre de défaites="+str(d))
    return moy, e



def comparaison_p(deb,fin,pas,k):
    Y=[]
    X=linspace(deb,fin,int((fin-deb)//pas+1))
    for p in X:
        Y.append(moyenne_memo_lex(LL4,k,"predef-max",2,3,p,"parie")[0])
    plt.plot(X,Y)
    plt.xlabel("p")
    plt.ylabel("nombre moyen d'essai")
    plt.show()

def bar_lex(k):
    X=[]
    Y=[]
    Xp=[]
    Yp=[]
    S=0
    D={}
    for i in range(1,k+1):
        X.append(i)
        cp=play_lfa_memoisation_lex(LL4,"predef-max",2,3,0,"parie")
        Y.append(cp)
        S=S+cp
    for e in X:
        nb=Y[e-1]
        if nb in D:
            D[nb]+=1
        else :
            D[nb]=1
    for e in list(D):
        Yp.append(D[e]/k*100)
        Xp.append(e)
    plt.xlabel("nombre d'essais")
    plt.ylabel("fréquence %")
    plt.bar(Xp,Yp)
    print("moy=" + str(S / k))
    plt.show()
    plt.close()


def repartition_freq():
    mots_tries = sorted(dico_freq4, key=dico_freq4.get, reverse=True)
    X=[i for i in range(len(LL4))]
    Y=[dico_freq4[x]*100 for x in mots_tries]
    plt.plot(X,Y)
    plt.ylabel("fréquence lexicale %")
    plt.xlabel("indice dans la liste triée")
    plt.show()











































































