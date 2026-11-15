import os

"""
UNETA OGRANIČENJA:
1. Nemoguce je ispisati savrsen level-order, zbog nedostatka ljudskog faktora (dovoljno razmaka), nemogućnosti premeštanja kursora,
   i zbog toga što uglavnom čvor ima mnogo sinova, pa ne bi mogli da se prate potomci.
   Zato se ispiše broj nivoa, pa svi u tom nivou, jedni ispod drugog, sa napomenom koji je čiji sin.

UNETE PRETPOSTAVKE:
1. Igra se nasilno prekida ako se dođe do lista. Ako list nije rešenje, onda je to matrica iz koje slede samo ponavljanja brojeva.
"""

"""
jedinstvenoResenje: da li čvor predstavlja već viđeno rešenje ili vodi ka njemu, 1 ako je jedinstveno, 0 ako nije,
a ako uopšte ne vodi ka rešenju, -1
koriste ga funkcije za obilazak
"""
class Cvor:
    def __init__(self, mat, sinovi, otac = None):
        self.sinovi = sinovi # [] ili [...]
        self.mat = mat
        self.obidjen = False # sluzi pri generisanju
        self.otac = otac
        if otac is None:
            self.visina = 0
        else:
            self.visina = self.otac.visina + 1
        self.jedinstvenoResenje = -1
    def ispisiMat(self):
        for i in range(9):
            if (i % 2 == 0):
                print("-----------------")
            else:
                for j in range(9):
                    if (j % 2 == 0):
                        print("|", end="\n" if j == 8 else "")
                    else:
                        print(" {} ".format(self.mat[i // 2][j // 2]), end="")
        return


class Stablo:
    def __init__(self, cvor):
        self.koren = cvor

    def levelOrder(self):
        levelRed = Red()
        trenutniNivo = -1
        sledeci = self.koren
        trenutniOtac = sledeci.otac
        levelRed.insert(sledeci)
        while (levelRed.notEmpty()):
            sledeci = levelRed.delete()
            if (trenutniNivo != sledeci.visina):
                trenutniNivo += 1
                print("Nivo {}:\n".format(trenutniNivo))
            if(trenutniOtac != sledeci.otac):
                print("Sinovi oca")
                sledeci.otac.ispisiMat()
                print("su:")
                trenutniOtac = sledeci.otac
            sledeci.ispisiMat()
            for i in range(len(sledeci.sinovi)):
                levelRed.insert(sledeci.sinovi[i])
        return

    def ispisResenja(self):
        levelRed = Red()
        trenutniNivo = -1
        sledeci = self.koren
        trenutniOtac = sledeci.otac
        if(sledeci.jedinstvenoResenje == 1): levelRed.insert(sledeci)
        while (levelRed.notEmpty()):
            sledeci = levelRed.delete()
            if (trenutniNivo != sledeci.visina):
                trenutniNivo += 1
                print("Nivo {}:\n".format(trenutniNivo))
            if(trenutniOtac != sledeci.otac):
                print("Sinovi oca")
                sledeci.otac.ispisiMat()
                print("su:")
                trenutniOtac = sledeci.otac
            sledeci.ispisiMat()
            for i in range(len(sledeci.sinovi)):
                if(sledeci.sinovi[i].jedinstvenoResenje == 1): levelRed.insert(sledeci.sinovi[i])
        return

class Stek:
    def __init__(self):
        self.vektor = []

    def notEmpty(self):
        if(self.vektor == []): return False
        return True

    def pop (self):
        if (self.vektor == []): return None
        a = self.vektor[-1]
        self.vektor = self.vektor[:-1]
        return a

    def push (self, p):
        self.vektor.append(p)
        return

class Red:
    def __init__(self):
        self.vektor = []

    def notEmpty(self):
        if(self.vektor == []): return False
        return True

    def delete (self):
        if (self.vektor == []): return None
        p = self.vektor[0]
        self.vektor = self.vektor[1:]
        return p

    def insert (self, p):
        self.vektor.append(p)
        return

def generisiStablo (matZaKoren):
    koren = Cvor(matZaKoren, [], None)
    stek = Stek()
    nadjenaResenja = []
    stek.push(koren)
    while(stek.notEmpty()):
        trenutni = stek.pop()
        if(trenutni.obidjen == False):
            trenutni.obidjen = True
            stek.push(trenutni)
            listaSinova = []
            trenutniMat = iskopirajMat(trenutni.mat)
            for i in range (4):
                for j in range(4):
                    if(trenutniMat[i][j] == 0):
                        for k in range(1,5):
                            trenutniMat[i][j] = k
                            if(proveraPonavljanja(trenutniMat)):
                                listaSinova.append(Cvor(iskopirajMat(trenutniMat), [], trenutni))
                                stek.push(listaSinova[-1])
                        trenutniMat[i][j] = 0
            trenutni.sinovi = listaSinova
        else:
            if(trenutni.sinovi == []):
                if(punaMat(trenutni.mat)):
                    trenutni.jedinstvenoResenje = 1
                    for i in range(len(nadjenaResenja)):
                        if(jednakeMat(trenutni.mat, nadjenaResenja[i])):
                            trenutni.jedinstvenoResenje = 0
                            break
                    nadjenaResenja.append(trenutni.mat)
                else: trenutni.jedinstvenoResenje = -1
            else:
                trenutni.jedinstvenoResenje = maksimumBroj(trenutni.sinovi)

    return Stablo(koren)

def maksimumBroj (mat):
    broj = mat[0].jedinstvenoResenje
    for i in range(1, len(mat)):
        if(mat[i].jedinstvenoResenje > broj): broj = mat[i].jedinstvenoResenje
    return broj
def obradiUnos(linija):
    if(linija[-1] == '\n'): return linija[0:-1]
    else: return linija
def proveraPonavljanja (mat):
    """ Funkcija proverava ispravnost/ponavljanja jedne matrice, ignorisuci nule.
    Vraca True ako je dobro, False ako ima ponavljanja. """
    for i in range (2):
        for j in range(2):
            brojevi = [0, 0, 0, 0, 0]
            for x in range(2):
                for y in range (2):
                    brojevi[mat[2*i + x][2*j + y]] += 1
            for k in range(1,5):
                if brojevi[k] > 1: return False
    for i in range (4):
        brojevi = [0, 0, 0, 0, 0]
        for j in range (4):
            brojevi[mat[i][j]] += 1
        for j in range(1,5):
            if brojevi[j] > 1: return False
    for j in range (4):
        brojevi = [0, 0, 0, 0, 0]
        for i in range(4):
            brojevi[mat[i][j]] += 1
        for i in range(1,5):
            if brojevi[i] > 1: return False
    return True
def dobroPocetnoStanje (mat):
    """ Funkcija proverava da li ima dovoljno nenultih brojeva, bar 5, u matrici,
    da li je svaki broj izmedju 0 i 4 i da li su dimenzije dobre. """
    brojac = 0
    for i in range (4):
        if(len(mat[i]) != 4): return False
        for j in range (4):
            if(mat[i][j] > 4 or mat[i][j] < 0): return False
            if(mat[i][j] > 0): brojac += 1
            if(brojac > 4): return True
    return False

def punaMat (mat):
    """ Funkcija proverava da li ima uopste nula u matrici,
        vraca True ako nema. """
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == 0): return False
    return True

def jednakeMat(mat1, mat2):
    """ Funkcija proverava da li su brojevi na istim indeksima u dve matrice jednaki,
        vraca False ako bar na jednom indeksu nema poklapanja. """
    for i in range(4):
        for j in range(4):
            if(mat1[i][j] != mat2[i][j]): return False
    return True

def iskopirajMat(mat1):
    mat2 = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            mat2[i].append(mat1[i][j])
    return mat2

print("=========================================")
print("==== ~ ASP1 2. domaći - SUDOKU 4x4 ~ ====")
print("=========================================")

print("1. Unos sa std. ulaza, 2. Unos iz datoteke\nIzaberite: ")
ulaz = int(input())
while True:
    if(ulaz == 1 or ulaz == 2): break
    print("Greška u unosu.\nIzaberite: ", end="")
    ulaz = int(input())

n = 0
matZaKoren = [[], [], [], []]
if (ulaz == 1):
    print ("Unesite dimenziju matrice N: ",end = "")
    n = int(input())
    while True:
        if (n == 4): break
        print("Greška, dimenzija mora biti 4.\nUnesite dimenziju: ", end="")
        n = int(input())
    for i in range (4):
        print("Unesite brojeve jedne vrste bez razmaka: ", end="")
        red = input()
        for j in range(len(red)):
            matZaKoren[i].append(int(red[j]))
    while True:
        if(dobroPocetnoStanje(matZaKoren) and proveraPonavljanja(matZaKoren)): break
        elif proveraPonavljanja(matZaKoren): print("Greška u vrednosti matrice.")
        else: print("Greška, ponavljanje brojeva.")

        print("Unesite matricu još jednom.")
        matZaKoren = [[], [], [], []]
        for i in range(4):
            print("Unesite brojeve jedne vrste bez razmaka: ", end="")
            red = input()
            for j in range(len(red)):
                matZaKoren[i].append(int(red[j]))

else:
    print("Unesite naziv datoteke: ", end ="")
    datoteka = input()
    while(True):
        if os.path.exists(datoteka): break
        print("Greška. Nepostojeća datoteka. Unesite naziv datoteke: ", end = "")
        datoteka = input()
    f = open(datoteka, "r")
    n = int(obradiUnos(f.readline()))
    while True:
        if (n == 4): break
        n = int(obradiUnos(f.readline()))
    for i in range(4):
        red = obradiUnos(f.readline())
        for j in range(len(red)):
            matZaKoren[i].append(int(red[j]))
    while True:
        if (dobroPocetnoStanje(matZaKoren) and proveraPonavljanja(matZaKoren)): break

        matZaKoren = [[], [], [], []]
        for i in range(4):
            red = obradiUnos(f.readline())
            for j in range(len(red)):
                matZaKoren[i].append(int(red[j]))
    f.close()

if(proveraPonavljanja(matZaKoren) == False): print("Ova matrica nije validna i nema rešenja. Hvala na igranju.")
else:
    stablo = generisiStablo (matZaKoren)
    trenutniCvor = stablo.koren
    print("Generisano je stablo odlučivanja.")
    while True:
        if(trenutniCvor.sinovi == []):
            if(trenutniCvor.jedinstvenoResenje == -1):
                print("Ova matrica ne vodi ka rešenju, pa se igra zaustavlja. Hvala na igranju.")
            else:
                print("Došli ste do jednog od rešenja. Hvala na igranju.")
            break
        #igranje
        print("Opcije:\n1. Odigravanje poteza,\n2. Ispis matrice,\n3. Provera ima li rešenja,\n4. Pomoć (ako je ima)\n5. Ispis celog stabla,\n6. Ispis svih rešenja (ako ih ima),\n7. Izlaz iz igre")
        print("Izaberite opciju: ", end = "")
        opcija = int(input())
        while(True):
            if(0 < opcija < 8): break
            print("Greška u unosu. Unesite opciju: ", end = "")
            opcija = int(input())

        print()

        if (opcija == 1):
            # odigravanje
            # napraviti da ako dođe do ponavljanja, opet se unosi broj (tako samo do listova može doći)
            while(True):
                print("Uneti u jednom redu broj, vrstu i kolonu (od 0): ", end = "")
                red = input().split()
                sledeciBroj = int(red[0])
                sledeciVrsta = int(red[1])
                sledeciKolona = int(red[2])
                while(True):
                    if(len(red) == 3 and 0 < sledeciBroj < 5 and -1 < sledeciVrsta < 4 and -1 < sledeciKolona < 4): break
                    if(len(red) != 3): print("Greška. Unet neodgovarajuć broj brojeva.")
                    else: print ("Greška. Unete nedozvoljene vrednosti.")
                    print("Uneti u jednom redu broj, vrstu i kolonu (od 0):", end="")
                    red = input().split()
                    sledeciBroj = int(red[0])
                    sledeciVrsta = int(red[1])
                    sledeciKolona = int(red[2])

                if(matZaKoren[sledeciVrsta][sledeciKolona] == 0):
                    matZaKoren[sledeciVrsta][sledeciKolona] = sledeciBroj
                    postojiOvajCvor = False
                    for i in range (len(trenutniCvor.sinovi)):
                        if(jednakeMat(trenutniCvor.sinovi[i].mat, matZaKoren)):
                            trenutniCvor = trenutniCvor.sinovi[i]
                            postojiOvajCvor = True
                            break
                    if(postojiOvajCvor == True): break
                    else:
                        print("Greška u unosu u matricu; ponavljajući brojevi.")
                        matZaKoren[sledeciVrsta][sledeciKolona] = 0
                else: print("Greška u unosu u matricu na već popunjeno mesto.")


        elif(opcija == 2): trenutniCvor.ispisiMat()

        elif (opcija == 3): # provera
            if(trenutniCvor.jedinstvenoResenje != -1): print("Rešenje postoji; na dobrom ste putu.")
            else: print("Ne postoji rešenje.")

        elif (opcija == 4): # pomoć (ako je ima)
            if (trenutniCvor.jedinstvenoResenje != -1):
                for i in range(len(trenutniCvor.sinovi)):
                    if(trenutniCvor.sinovi[i].jedinstvenoResenje != -1):
                        for j in range(4):
                            nadjen = False
                            for k in range(4):
                                if(trenutniCvor.mat[j][k] != trenutniCvor.sinovi[i].mat[j][k]):
                                    print("Pomoć: Postaviti broj {0} na koordinate ({1},{2}) (indeksiranje od 0).".format(trenutniCvor.sinovi[i].mat[j][k],j,k))
                                    nadjen = True
                                    break
                            if(nadjen): break
                        break
            else:
                print("Ne postoji rešenje.")

        elif (opcija == 5): stablo.levelOrder()
        elif (opcija == 6): stablo.ispisResenja()
        else: print("Hvala na igranju.")