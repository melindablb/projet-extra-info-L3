from bs4 import BeautifulSoup
import sys
maj=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
min=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

if len(sys.argv) != 2:
    print("\nErreur: nombre incorrect d'arguments !\nUsage : python script.py arg1\n")
    sys.exit(1)

fdic=open("subst.dic","a+",encoding="utf-16")
finfo=open("infos1.txt","a+",encoding="utf-8")

finfo.write("Le nombre d'entites medicales de type noms de medicaments par substance pour chaque lettre de l'alphabet:\n")

nb=0
cpt=0
nbT=0

for var1 in maj:

    var2=min[nb]
    nb=nb+1

    chemin = f"{sys.argv[1]}/vidal-Sommaires-Substances-{var1}.htm"  # nouveau chemin
    fsource=open(chemin,"r",encoding="utf-8") #ouverture du fichier html

    soup=BeautifulSoup(fsource,"html.parser") #soup contient le fichier ouvert a l aide de beautiful soup

    elm=soup.find(id=f"letter{var2}") #elm contient l element du fichier html dont l id = letter(var)

    if elm: #verifie si elm existe pour eviter les erreurs

        texte=elm.text #texte (de type str) contient tous les textes de l element elm

        liste=texte.split("\n") #split convertis la chaine texte en liste contenant uniquement les mots (sans \n)

        for i in liste: #ecriture de tous les elements de la meme lettre un par un
            if i!="": #verifie que i n est pas un mot vide
                fdic.write(i+",.N+subst\n")
                cpt=cpt+1 #compte le nbr de substances de la lettre courante
    chaine=f"Le nombre d’entites medicales de type noms de medicaments par substance active pour {var1} : "+str(cpt)+"\n"
    print(f"{sys.argv[1]}/vidal-Sommaires-Substances-{var1}.htm \nLe nombre  d’entites medicales pour la lettre {var1} est: " + str(cpt) + "\n")
    finfo.write(chaine) #ecriture du nb de d elm par lettre dans le fichier txt
    nbT=nbT+cpt #incrementation du nb total
    cpt=0 #reinitialisation a 0

    fsource.close()#fermeture du fichier source ouvert

finfo.write("Le nombre total d’entites medicales par substance active est: "+str(nbT)+"\n")
finfo.close()

fdic.seek(0)
all=fdic.readlines() #toutes les lignes dans all
last=all.pop() #derniere ligne retiree et mise dans b
conv=last.split() #conversion en liste de la derniere ligne (plus de \n)
last=str(conv[0]) #conversion en chaine
all.append(last) #ajout de b a la fin de la liste
total="".join(all) #cree une chaine qui contient tt les elm de la liste "all" separe par rien
fdic.close()
fdic=open("subst.dic","w",encoding="utf-16") #ouverture en ecriture seulement pour ecraser le contenu
fdic.write(total)
fdic.close()
