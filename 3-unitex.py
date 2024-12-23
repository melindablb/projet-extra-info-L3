import os
import shutil
import subprocess


if not os.path.exists("corpus-medical.txt"):
    raise FileNotFoundError("corpus-medical.txt is missing!")

if not os.path.exists("Alphabet.txt"):
    raise FileNotFoundError("Alphabet.txt is missing!")

if shutil.which(r"C:\Program Files (x86)\Unitex-GramLab\App\UnitexToolLogger.exe") is None:
    raise EnvironmentError("UnitexToolLogger is not installed or not in PATH.")

#on efface le repertoire s il existe deja
if os.path.exists("corpus-medical_snt"):
    shutil.rmtree("corpus-medical_snt")

os.mkdir("corpus-medical_snt")


try:
    subprocess.run(["UnitexToolLogger", "Normalize", "corpus-medical.txt", "-r", "Norm.txt"], check=True)

    subprocess.run(["UnitexToolLogger", "Tokenize", "corpus-medical.snt", "-a", "Alphabet.txt"], check=True)
    #Tokenisation (commande 'Tokenize') : definit les caracteres consideres comme des tokens.
    #Par exemple, si 'Alphabet.txt' inclut les lettres 'a-z' et 'A-Z', seuls ces caracteres seront reconnus.

    subprocess.run(["UnitexToolLogger", "Compress", "subst.dic"], check=True)

    subprocess.run(["UnitexToolLogger", "Dico", "-t", "corpus-medical.snt", "-a", "Alphabet.txt", "subst.bin", "Dela"], check=True)
    #Dictionnaires (commande 'Dico') : etablit un alphabet pour creer des automates
    #permettant de reconnaitre les mots du texte et les associer a leurs formes normales.

    subprocess.run(["UnitexToolLogger", "Grf2Fst2", "posologie.grf"], check=True)
    subprocess.run(["UnitexToolLogger", "Locate", "-t", "corpus-medical.snt", "posologie.fst2", "-a", "Alphabet.txt", "-L", "-I", "--all"], check=True)
    subprocess.run(["UnitexToolLogger", "Concord", "corpus-medical_snt/concord.ind", "-f", "Courrier new", "-s", "12", "-l", "40", "-r", "55"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed with error: {e}")
