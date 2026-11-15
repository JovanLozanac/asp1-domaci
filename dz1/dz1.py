"""
UNETA OGRANICENJA:
1. Dimenzije matrice, nxn, ne mogu biti 17x17 ili vise, zbog preglednosti ispisa. Dakle, n je 7,9,11,13 ili 15.

UNETE PRETPOSTAVKE:
1. Ako igrac dobije 6 i uvede figuricu u igru na svoje startno polje:
    a. Ako se na tom polju nalazi figurica ISTOG igraca, nova figurica NECE biti uvedena.
    b. Ako se na tom polju nalazi TUDJA figurica, ona ce biti pojedena a na njeno mesto dolazi nova figurica.
    c. Ako je prazno polje, nova figurica ce biti uvedena.
2. Nakon izvlacenja sestice, po tumacenju teksta:
    a. Ako taj igrac nema figurica na tabli, samo se ubacuje
    b. Ako ima, bira se unapred izmedju nove figurice i kretanja po tabli za 6 polja.

"""
class Node:
    def __init__(self, info=None):
        self.info = info
        self.next = None
    def __repr(self):
        return self.info
class Header:
    def __init__(self):
        self.info = None
        self.next = self
class List:
    def __init__(self):
        self.zaglavlje = Header()
        self.zaglavlje.next = self.zaglavlje
    def __repr__(self):
        if(self.brElemNakonZaglavlja() == 0): return ("Prazna lista")
        else:
            niz = ""
            tmp = self.zaglavlje.next
            while(tmp is not self.zaglavlje):
                niz += (str(tmp.info) + " ")
                tmp = tmp.next
            return niz
    def brElemNakonZaglavlja (self):
        br = 0
        tmp = self.zaglavlje.next
        while (tmp is not self.zaglavlje):
            br = br + 1
            tmp = tmp.next
        return br

    def dodajNaKraj(self, broj):
        p = Node (broj)
        p.next = self.zaglavlje
        if(self.brElemNakonZaglavlja() == 0):
            self.zaglavlje.next = p
        else:
            a = self.zaglavlje.next
            while(a.next is not self.zaglavlje):
                a = a.next
            a.next = p
        return

    def izbaciSaPocetka (self):
        if(self.brElemNakonZaglavlja() == 0): return "Prazna lista, nema vraćenog elementa"
        brisanje = self.zaglavlje.next
        broj = brisanje.info
        if (self.brElemNakonZaglavlja() == 1):
            self.zaglavlje.next = self.zaglavlje
        else:
            self.zaglavlje.next = self.zaglavlje.next.next
        del brisanje
        return broj
def generisiListe(brIgraca):
    listaListi = []
    for i in range (brIgraca):
        listaListi.append(List())
        for j in range (4):
            listaListi[i].dodajNaKraj(10 * (i+1) + j + 1)
    return listaListi

def izlistajListe (listaListi, broj):
    if (listaListi[broj-1].brElemNakonZaglavlja() == 0): print("Igrač {} nema figurica van talona.".format(broj))
    else: print("Igrač {0}: {1}".format(broj, listaListi[broj-1]))
    return
def parnost (br):
    brJedinica = 0
    while(br >= 1):
        if(br % 2 == 1): brJedinica += 1
        br = br // 2
        # br = br >> 1
    if(brJedinica % 2 == 1): return 1
    else: return 0

x = 16044
def kocka():
    p = 66107
    q = 58907
    while True:
        global x
        x = (x ** 2) % (p * q)
        x1 = parnost(x)
        x = (x ** 2) % (p * q)
        x2 = parnost(x)
        x = (x ** 2) % (p * q)
        x3 = parnost(x)
        if((x1 * 2 + x2) * 2 + x3 < 6): break;
    return (x1 * 2 + x2) * 2 + x3 + 1

def uslov(n, brIgraca, pokazivaciKol, redovi, podaci):
    #ova metoda testira da li postoji igrac cije su 4 figurice na ciljnim mestima
    for igrac in range(1, brIgraca+1):
        #igrac 1: dole levo
        if igrac == 1:
            pobeda = True
            for k in range (4):
                if(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-2-k, 1) is None):
                    pobeda = False
                    break
            if(pobeda): return 1
        #igrac 2: gore levo
        elif igrac == 2:
            pobeda = True
            for k in range (4):
                if(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 1, 1+k) is None):
                    pobeda = False
                    break
            if (pobeda): return 2
        #igrac 3: gore desno
        elif igrac == 3:
            pobeda = True
            for k in range (4):
                if(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 1+k, n-2) is None):
                    pobeda = False
                    break
            if (pobeda): return 3
        #igrac 4: dole desno
        else:
            pobeda = True
            for k in range (4):
                if(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-2, n-2-k) is None):
                    pobeda = False
                    break
            if (pobeda): return 4
    return 0

def ukloniEl (pokazivaciKol, redovi, podaci, broj):
    # ova metoda izbacuje iz retke matrice broj AKO nije default_elem
    # vraca nove vektore bez izbacenog broja
    if(postojiNaTalonuVrednost(pokazivaciKol, redovi, podaci, broj) is None): return pokazivaciKol, redovi, podaci
    i,j = postojiNaTalonuVrednost(pokazivaciKol, redovi, podaci, broj)

    nadjen = False
    (aelem, belem) = (0,0)
    for a in range(len(pokazivaciKol) - 1):
        for b in range(pokazivaciKol[a], pokazivaciKol[a + 1]):
            if (a == j and redovi[b] == i):
                nadjen = True
                aelem = a
                belem = b
                break
    if (nadjen == False): return pokazivaciKol, redovi, podaci
    for a in range(aelem+1, len(pokazivaciKol)):
        pokazivaciKol[a] = pokazivaciKol[a] - 1
    # redovi.pop(belem)
    # podaci.pop(belem)
    for a in range (belem,len(redovi)-1):
        redovi[a] = redovi[a+1]
        podaci[a] = podaci[a+1]
    del(redovi[-1])
    del(podaci[-1])

    return pokazivaciKol, redovi, podaci

def dodajEl(pokazivaciKol, redovi, podaci, broj, i, j):
    # ova metoda dodaje broj A[i,j] u retku matricu, najpre konvertujuci (i,j) u odgovarajuci format
    # vraca azurirane vektore
    if(postojiNaTalonuVrednost(pokazivaciKol,redovi,podaci, broj) is not None): return pokazivaciKol, redovi, podaci
    for a in range(j+1, len(pokazivaciKol)):
        pokazivaciKol[a] += 1

    redovi.append(i)
    podaci.append(broj)
    for a in range(len(redovi) - 1, pokazivaciKol[j], -1):
        redovi[a] = redovi[a - 1]
        podaci[a] = podaci[a - 1]
    redovi[pokazivaciKol[j]] = i
    podaci[pokazivaciKol[j]] = broj
    minIndeks = pokazivaciKol[j]
    maxIndeks = pokazivaciKol[j + 1] - 1

    if(maxIndeks > minIndeks + 1):
        for a in range(minIndeks, maxIndeks+1):
            minimum = a
            for b in range (a+1, maxIndeks+1):
                if(redovi[minimum] > redovi[b]):
                    minimum = b
            tmp = redovi[a]
            redovi[a] = redovi[minimum]
            redovi[minimum] = tmp
            tmp = podaci[a]
            podaci[a] = podaci[minimum]
            podaci[minimum] = tmp


    elif(maxIndeks == minIndeks + 1):
        if(redovi[minIndeks] > redovi[maxIndeks]):
            tmp = redovi[minIndeks]
            redovi[minIndeks] = redovi[maxIndeks]
            redovi[maxIndeks] = tmp
            tmp = podaci[minIndeks]
            podaci[minIndeks] = podaci[maxIndeks]
            podaci[maxIndeks] = tmp

    return pokazivaciKol, redovi, podaci

def postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, i, j):
    # ova metoda vraca broj na koordinatama AKO nije default_elem
    if redovi == []: return None
    for a in range(len(pokazivaciKol) - 1):
        for b in range(pokazivaciKol[a], pokazivaciKol[a + 1]):
            if (a == j and redovi[b] == i): return podaci[b]
    return None

def postojiNaTalonuVrednost(pokazivaciKol, redovi, podaci, broj):
    # ova metoda vraca koordinate broja AKO nije default_elem
    if broj not in podaci: return None
    i = redovi[podaci.index(broj)]
    for a in range(len(pokazivaciKol) - 1):
        if(pokazivaciKol[a] <= podaci.index(broj) < pokazivaciKol[a+1]):
            return i, a

def ispisMatrice(n, pokazivaciKol, redovi, podaci):
    for i in range(n+1):
        print("-" * (5*n+1), sep = "")
        if(i == n): break
        for j in range(n):
            print("|", end = "")
            if postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, i, j) is not None:
                print(" ", end = "")
                print(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, i, j), end = "")
                print(" ", end="")
            else: print("    ", end = "")
        print("|")
    return

def zauzetoPocetno(n, naPotezu, pokazivaciKol, redovi, podaci):
    # da li 0: igrac zauzima svoje pocetno mesto svojom figuricom
    # -1: ima slobodno mesto ili #ostalo: vraca protivnicku figuricu na tom mestu
    if (naPotezu == 1):
        if(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-1, 0) is None): return -1
        elif(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-1, 0) // 10 == 1): return 0
        else: return postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-1, 0)
    elif (naPotezu == 2):
        if(postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 0, 0) is None): return -1
        elif (postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 0, 0) // 10 == 2): return 0
        else: return postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 0, 0)
    elif (naPotezu == 3):
        if (postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 0, n-1) is None): return -1
        elif (postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 0, n-1) // 10 == 3): return 0
        else: return postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, 0, n-1)
    else:
        if (postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-1, n-1) is None): return -1
        elif (postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-1, n-1) // 10 == 4): return 0
        else: return postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, n-1, n-1)

def izracunajPomerajZaJedno(n, i, j, naPotezu):
    # poslednje ciljno polje
    if(naPotezu == 1 and (i,j) == (n-5,1)): return None
    if(naPotezu == 2 and (i,j) == (1,4)): return None
    if(naPotezu == 3 and (i,j) == (4,n-2)): return None
    if(naPotezu == 4 and (i,j) == (n-2,n-5)): return None

    #3, 2, i 1. ciljno polje, kao i ono pre njega
    if(naPotezu == 1 and j == 1 and n-1 >= i >= n-4): return (i-1, j)
    if(naPotezu == 2 and i == 1 and 3 >= j >= 0): return (i,j+1)
    if(naPotezu == 3 and j == n-2 and 3 >= i >= 0): return (i+1,j)
    if(naPotezu == 4 and i == n-2 and n-2 >= j >= n-5): return (i,j-1)

    #uobicajena polja
    if(i == 0 and j != n-1): return (i,j+1)
    if(j == n-1 and i != n-1): return (i+1,j)
    if(i == n-1 and j != 0): return (i,j-1)
    if(j == 0 and i != 0): return (i-1,j)

def startno(naPotezu, n):
    if(naPotezu == 1): return n-1, 0
    elif(naPotezu == 2): return 0, 0
    elif(naPotezu == 3): return 0, n-1
    else: return n-1, n-1

def postojiValidanPotezNakonBacanja(n, naPotezu, pokazivaciKol, redovi, podaci, brojSKocke, i, j):
    for k in range(brojSKocke):
        if(izracunajPomerajZaJedno(n,i,j, naPotezu) is None): return False
        i, j = izracunajPomerajZaJedno(n,i,j, naPotezu)
    if(postojiNaTalonuIndeksi(pokazivaciKol,redovi,podaci,i,j) is None): return True
    if (postojiNaTalonuIndeksi(pokazivaciKol,redovi,podaci,i,j) // 10 == naPotezu): return False
    return True

print("==================================================")
print("==== ~ ASP1 1. domaći - NE LJUTI SE, ČOVEČE ~ ====")
print("==================================================")

# unos podataka
print("Uneti dimenzije kvadratne table (7, 9, 11, 13 ili 15): ", end = "")
n = int(input())
while (n < 7 or n > 15 or n % 2 == 0):
    print("Greška u unosu. Uneti dimenzije kvadratne table (7, 9, 11, 13 ili 15): ", end = "")
    n = int(input())

print("Uneti broj igrača (2, 3 ili 4): ", end = "")
brIgraca = int(input())
while (brIgraca < 2 or brIgraca > 4):
    print("Greška u unosu. Uneti broj igrača (2, 3 ili 4): ", end = "")
    brIgraca = int(input())

# generisanje pomocnih struktura
# pravimo onoliko 1-struko ulancanih kruznih listi koliko ima igraca.
# konvencija za figurice: <redni broj igraca><broj figurice po igracu>. Na primer: 31, 1. figurica 3. igraca
listeFig = generisiListe (brIgraca)
print("Generisana je lista figurica van talona.")

# CSC
pokazivaciKol = [0] * (n+1)
redovi = []
podaci = []

print("Generisana je lista figurica u talonu.")

naPotezu = 1
while(True):
    #pobeda
    if (uslov(n, brIgraca, pokazivaciKol, redovi, podaci) != 0):
        print("Partija je završena pobedom igrača {}. Hvala na igranju.".format(uslov(n, brIgraca, pokazivaciKol, redovi, podaci)))
        break

    #ako partija jos traje
    print("Opcije:\n1 - Odigrati potez, \n2 - Ispis talona i svih figurica, \n3 - Izlaz iz programa.\nUneti broj: ", end = "")
    opcija = int(input())
    while(opcija > 3 or opcija < 1):
        print("Greška u unosu.\n1 - Odigrati potez, \n2 - Ispis talona i svih figurica, \n3 - Izlaz iz programa.\nUneti broj: ", end = "")
        opcija = int(input())

    if(opcija == 1):
        #igranje poteza
        print("Na redu je igrač {}.".format(naPotezu))
        novaFig = False
        if(listeFig[naPotezu-1].brElemNakonZaglavlja() == 4):
            if (zauzetoPocetno(n, naPotezu, pokazivaciKol, redovi, podaci) == 0): print("Igrač propušta red.")
            else:
                print("Igrač baca kockicu 3 puta da bi najviše jednom ubacio figuricu.")
                for i in range (3):
                    a = kocka()
                    print("Vrednost dobijena na kockici: {}".format(a))
                    if(a == 6):
                        novaFig = True
                        break
                if(novaFig == False): print("Igrač nije dobio novu figuricu.")

                else:
                    if(zauzetoPocetno(n, naPotezu, pokazivaciKol, redovi, podaci) == -1):
                        nova = listeFig[naPotezu-1].izbaciSaPocetka()
                        pokazivaciKol, redovi, podaci = dodajEl(pokazivaciKol,redovi,podaci,nova,*startno(naPotezu, n))
                        print("Nova figurica igrača {0}, {1}, ubačena je na njegovo startno polje.".format(naPotezu, nova))

                    else:
                        stara = postojiNaTalonuIndeksi(pokazivaciKol,redovi,podaci, *startno(naPotezu, n))
                        nova = listeFig[naPotezu - 1].izbaciSaPocetka()
                        pokazivaciKol, redovi, podaci = ukloniEl(pokazivaciKol,redovi,podaci, stara)
                        pokazivaciKol, redovi, podaci = dodajEl(pokazivaciKol, redovi, podaci, nova, *startno(naPotezu, n))
                        listeFig[stara//10 - 1].dodajNaKraj(stara)
                        print("Nova figurica igrača {0}, {1}, ubačena je na njegovo startno polje, a pojela je figuricu {2} igrača {3}.".format(naPotezu, nova, stara, stara // 10))

        else:
            a = kocka()
            if (listeFig[naPotezu - 1].brElemNakonZaglavlja() == 0 or zauzetoPocetno(n, naPotezu, pokazivaciKol, redovi, podaci) == 0):
                # novaFig = False
                print("Igrač ne može da ubaci novu figuricu.")

            else:
                print("Igrač baca kockicu i pomera željenu figuricu, osim ako dobije 6. Tada umesto pokreta, može da ubaci novu figuricu.")
                print("Nova figurica na 6?\nD - da\nN - ne")
                while True:
                    rec = input()
                    if(rec == "D" or rec == "d"):
                        novaFig = True
                        break
                    elif(rec == "N" or rec == "n"):
                        break
                    else: print("Greška u unosu. \nD - da\nN - ne")
            print("Vrednost dobijena na kockici: {0} ".format(a))
            if(a == 6 and novaFig == True):
                if (zauzetoPocetno(n, naPotezu, pokazivaciKol, redovi, podaci) == -1):
                    nova = listeFig[naPotezu - 1].izbaciSaPocetka()
                    pokazivaciKol, redovi, podaci = dodajEl(pokazivaciKol, redovi, podaci, nova, *startno(naPotezu, n))
                    print("Nova figurica igrača {0}, {1}, ubačena je na njegovo startno polje.".format(naPotezu, nova))
                else:
                    stara = postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, *startno(naPotezu, n))
                    nova = listeFig[naPotezu - 1].izbaciSaPocetka()
                    pokazivaciKol, redovi, podaci = ukloniEl(pokazivaciKol, redovi, podaci, stara)
                    pokazivaciKol, redovi, podaci = dodajEl(pokazivaciKol, redovi, podaci, nova, *startno(naPotezu, n))
                    listeFig[stara // 10 - 1].dodajNaKraj(stara)
                    print("Nova figurica igrača {0}, {1}, ubačena je na njegovo startno polje, a pojela je figuricu {2} igrača {3}.".format(naPotezu, nova, stara, stara // 10))
            else:
                figurice = [10*naPotezu + k for k in range(1,5)]
                figurice = list(filter(lambda x: postojiNaTalonuVrednost(pokazivaciKol, redovi, podaci, x) is not None, figurice))
                figurice = list(filter(lambda x: postojiValidanPotezNakonBacanja(n, naPotezu, pokazivaciKol, redovi, podaci, a, *postojiNaTalonuVrednost(pokazivaciKol, redovi, podaci, x)), figurice))
                if(len(figurice) == 0): print("Igrač nema mogućnosti za pokret i propušta red.")
                else:
                    if(len(figurice) == 1):
                        figuricaKojaSePomera = figurice[0]
                        print("Igrač jedino može igrati figuricom {}.".format(figuricaKojaSePomera))
                    else:
                        print("Igrač jedino može da pomeri sledeće figurice na talonu:", end = " ")
                        for fig in figurice:
                            print(fig, end = " ")
                        print()
                        print("Ukucati željeni broj figurice. ", end = "")
                        figuricaKojaSePomera = int(input())
                        while(figuricaKojaSePomera not in figurice):
                            print("Greška. Unesena nepostojeća figurica.\nUkucati željeni broj figurice: {}.".format(figurice))
                            figuricaKojaSePomera = int(input())
                    # prosto pomeranje figurice, najpre izracunavanje putanje, eventualno blokiranje ili jedenje na tom mestu
                    istaro, jstaro = postojiNaTalonuVrednost(pokazivaciKol,redovi,podaci,figuricaKojaSePomera)
                    inovo, jnovo = -1, -1
                    for k in range (a):
                        if k == 0:
                            inovo, jnovo = izracunajPomerajZaJedno(n,istaro, jstaro, naPotezu)
                        else:
                            inovo, jnovo = izracunajPomerajZaJedno(n,inovo, jnovo, naPotezu)
                    if(postojiNaTalonuIndeksi(pokazivaciKol,redovi,podaci,inovo,jnovo) is None):
                        #samo izbaci i ubaci
                        pokazivaciKol, redovi, podaci = ukloniEl(pokazivaciKol,redovi,podaci,figuricaKojaSePomera)
                        pokazivaciKol, redovi, podaci = dodajEl(pokazivaciKol,redovi,podaci,figuricaKojaSePomera, inovo, jnovo)
                        print("Figurica {0} prešla je sa polja ({1},{2}) na ({3},{4}).".format(figuricaKojaSePomera, istaro, jstaro, inovo, jnovo))
                    else:
                        # izbaci pojedenu figuricu i vrati je u listu
                        pojedena = postojiNaTalonuIndeksi(pokazivaciKol, redovi, podaci, inovo, jnovo)
                        pokazivaciKol, redovi, podaci = ukloniEl(pokazivaciKol, redovi, podaci, pojedena)
                        listeFig[pojedena // 10 - 1].dodajNaKraj(pojedena)
                        # izbaci i ubaci figuricu sto se krece
                        pokazivaciKol, redovi, podaci = ukloniEl(pokazivaciKol, redovi, podaci, figuricaKojaSePomera)
                        pokazivaciKol, redovi, podaci = dodajEl(pokazivaciKol, redovi, podaci, figuricaKojaSePomera, inovo, jnovo)
                        print("Figurica {0} prešla je sa polja ({1},{2}) na ({3},{4}) i tom prilikom pojela figuricu {5} igrača {6}".format(figuricaKojaSePomera, istaro, jstaro, inovo, jnovo, pojedena, pojedena // 10))
        naPotezu += 1
        if(naPotezu > brIgraca): naPotezu = 1
        print() # razdvajanje

    elif (opcija == 2):
        #ispis
        ispisMatrice(n, pokazivaciKol, redovi, podaci)

        print("Ispis figurica van talona. \n0 - ispisati za svakog igrača, \n[1, broj igrača] - ispisati za traženog igrača.\nUneti broj: ", end = "")
        zaIspis = int(input())
        while(zaIspis < 0 or zaIspis > brIgraca):
            print(
                "Greška u unosu. \n0 - ispisati za svakog igrača, \n[1, broj igrača] - ispisati za traženog igrača.\nUneti broj: ",
                end="")
            zaIspis = int(input())
        if(zaIspis == 0):
            for igrac in range (1, brIgraca+1):
                izlistajListe(listeFig, igrac)
        else: izlistajListe(listeFig, zaIspis)
        print()  # razdvajanje

    else:
        #kraj
        print("Hvala na igranju.")
        break