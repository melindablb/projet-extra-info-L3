import sys
import re
import locale

alphabet=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

if len(sys.argv) != 2:
    print("\nErreur: nombre incorrect d'arguments !\nUsage : python script.py arg1\n")
    sys.exit(1)

chemin_crp=f"{sys.argv[1]}"
chemin_dic="subst.dic"
chemin_dic_crp="subst_corpus.dic"

regex= r"^[-*Ø]?\s?(\w+)\s:?\s?(\d+|,|\d+.\d)+\s?:?(\s(mg\s|MG|UI|ml|mcg|amp|iu|flacon|g|sachet|un\s|1/j|/j)(.+|\n)|(g|/j)\n|(mg)\s.+)" #pattern du medoc
regvitamine=r"((vitamine|VITAMINE|Vitamine) [A-Za-b](\d| \d)*)" #pattern vitamine

L1=[] #ce que va contenir subst_corpus
L2=[] #L1 sans doublons


fcrp=open(chemin_crp,"r",encoding="utf-8") #ouverture du corpus
fdic=open(chemin_dic,"a+",encoding="utf-16") #ouverture du dic
fdic_crp=open(chemin_dic_crp,"w",encoding="utf-16") #ouverture du dic corpus

################################ creation du dictionnaire subst_corp

fcrp.seek(0) #remise du curseur au debut
lignes1=fcrp.readlines() #toutes les lignes de corpus



for i in lignes1:  #lignes de corpus une par une
    x=re.search(regex, i) #on cherche si il ya des medicament
    if x: #si un medoc existe sur la ligne
        #elimination des exceptions
        if x.group(1).lower() != 'vichy' \
                and x.group(1).lower() != 'mdz' \
                and x.group(1).lower() != 'vvp' \
                and x.group(1).lower() != 'hémoglobine' \
                and x.group(1).lower() != 'aspegic' \
                and x.group(1).lower() != 'kt' \
                and x.group(1).lower() != 'le' \
                and x.group(1).lower() != 'eau' \
                and x.group(1).lower() != 'puis':
                y=x.group(1) #extraction du nom du medoc uniquement
                L1.append(str(y)) #ajout du medoc a L1
    else :
        #cas vitamine
        x=re.search(regvitamine, i)
        if x:
            y = x.group(1)  # extraction du nom du medoc uniquement
            L1.append(str(y))  # ajout du medoc a L1


for i in range(len(L1)): #parcourt de toute la liste
    L1[i]=L1[i].lower() #rend les elm de la liste en min
    L1[i]=L1[i]+",.N+subst" #ajout de l info gram et semantique


chaine="\n".join(L1) #conversion de la liste en chaine de char
fdic_crp.write(chaine) #remplissage de subst_corp
fdic_crp.close()

################################ creation du fichier infos2.txt

L2=set(L1)
L2=list(L2) #L2 = L1 sans doublons

finf2=open("infos2.txt","w",encoding="utf-8") #ouverture d infos2
nbT=0 #cpt nombre total
cpt=0 #cpt pour chaque lettre
for l in alphabet:
    for i in L2:
        if i[0]== l:
            cpt=cpt+1 #incrementation pour la lettre courante
            nbT=nbT+1 #incrementation de nombre total

    chaine=f"Le nombre de medicaments issus du corpus pour la lettre {l} : "+str(cpt)+"\n"
    finf2.write(chaine)
    cpt=0

chaine="Le nombre total de medicaments issus du corpus : "+str(nbT)+"\n"
finf2.write(chaine)

finf2.close()

################################ creation du fichier infos3.txt

finf3=open("infos3.txt","w",encoding="utf-8")
f1=open(chemin_dic_crp,"r",encoding="utf-16")
f2=open(chemin_dic,"r",encoding="utf-16")

corp=f1.readlines()
subst=f2.readlines()

corp=list(set(corp))

cpt=0
nbT=0
b=0
#on doit trouver les elements de corpus qui ne sont pas dans subst
for l in alphabet: #on parcourt pour chaque lettre de l alphabet
    for i in corp: #on parcourt corpus
        for j in subst: #pour chaque element de corpus on verifie s il existe dans subst
            if i==j:
                b=1 #s il existe, on met le booleen a 1
        if b==1:
            b=0 #on remet le booleen a 0 pour les prochaines iterations
            break #on sort de l iteration courante afin de changer de mot
        if i[0]==l : #s il n existe pas, on verifie si sa premiere lettre est egale a la lettre courante
            cpt=cpt+1 #on incremente le compteur de la lettre
            nbT=nbT+1 #on incremente le compteur total

    chaine=f"le nombre de medicaments conserves pour l’enrichissement pour la lettre {l} : "+str(cpt)+"\n"
    finf3.write(chaine)
    cpt=0

chaine="Le nombre total de medicaments conserves pour l’enrichissement : "+str(nbT)+"\n"
finf3.write(chaine)

f1.close()
f2.close()
finf3.close()

################################ update de subst.dic

fdic=open(chemin_dic,"a+",encoding="utf-16") #ouverture du dic

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

L2= [element.strip() for element in L2] #on retire les \n des elm

fdic.seek(0)
L3=fdic.readlines()
L3= [element.strip() for element in L3] #on retire les \n des elm

L3=L3+L2 #concatenation des deux listes
L4=set(L3) #on retire les elements en commun
L3=sorted(L4,key=locale.strxfrm)  #on trie

fdic.close() #on ferme pour ouvrir en ecriture seulement afin d ecraser le contenu
fdic=open(chemin_dic,"w",encoding="utf-16") #ouverture du dic
fdic.write("\n".join(L3))
fdic.close()
