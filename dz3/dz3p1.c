#include <stdio.h>
#include <stdlib.h>

//NAPOMENA: Datoteku koja se cita treba staviti u folder cmake-build-debug, inace se nece videti u CLion.
/*
UNETA OGRANICENJA:
1. Novi cvor se uvek ubacuje na najvise mesto, a "izbacuju" se samo menjanjem jedne promenljive (da li su aktivni ili ne),
 medjutim oni se ne brisu kako bi se olaksalo azuriranje grafa tj. liste grana.

UNETE PRETPOSTAVKE:
1. "Brisanje grafa iz memorije" odnosi se na vracanje na pocetno stanje, sa dim cvorova i bez grana,
   kako se program ne bi prekinuo (pominje se naredba za prekid programa) i zato odgovara istom zahtevu kao i "kreiranje prazne strukture podataka".
   S druge strane, naredba za prekid programa vri oslobadjanje memorije pre kraja programa.
2. "Ispis reprezentacije grafa", posto nije naveden ni BFS ni DFS, niti eventualna podela na grupe u vezi sa tim,
   a i jer nam je eksplicitno dat vektor cvorova, samo znaci ispisati sve cvorove koji do tad nisu izbaceni iz grafa.
*/
typedef struct graf
{
    int *grane; //spisak grana tj. onog drugog cvora
    struct cvor *cvorovi; //spisak cvorova
    int dim;
} Graf;

typedef struct cvor
{
    int broj;
    int aktivan;
    //aktivan == 1 - aktivan, 0 - markiran, izbrisan
} Cvor;

Graf *napraviPrazanGraf(int dim) {
    Graf *g = malloc(sizeof(Graf));
    g -> grane = NULL;
    g -> cvorovi = malloc((dim + 1) * sizeof(Cvor));
    for (int i = 0; i < dim; i++)
    {
        g->cvorovi[i].aktivan = 1;
        g->cvorovi[i].broj = 0;
    }
    g->cvorovi[dim].broj = 0;
    g->cvorovi[dim].aktivan = 0;
    g -> dim = dim;
    return g;
}

void ispisGrafa(Graf *g)
{
    for(int i = 0; i < g-> dim; i++)
    {
        if(g->cvorovi[i].aktivan == 1) printf("%d ", i);
    }
    putchar('\n');
}

void oslobodiGraf(Graf *g)
{
    free(g -> grane);
    free(g -> cvorovi);
    free(g);
}

void dodajCvor(Graf *g)
{
    //dodaje se na poslednje mesto (pretposlednje u nizu)

    g -> dim = g -> dim + 1;
    g -> cvorovi = realloc(g->cvorovi, (g->dim+1)*sizeof(Cvor));
    g -> cvorovi[g->dim].broj = g -> cvorovi[g->dim-1].broj;
    g -> cvorovi[g->dim].aktivan = 0;
    g -> cvorovi[g->dim-1].aktivan = 1;
}

void izbaciCvor(Graf *g, int indeks)
{
    g->cvorovi[indeks].aktivan = 0;
}

void dodajGranu(Graf *g, int jedan, int drugi)
{
    int nadjenaGrana = 0;
    for(int i = g->cvorovi[jedan].broj; i != g->cvorovi[jedan+1].broj; i++)
    {
        if(g->grane[i] == drugi)
        {
            nadjenaGrana = 1;
            break;
        }
    }
    if(nadjenaGrana == 0)
    {
        g->grane = realloc(g->grane, (g->cvorovi[g->dim].broj+1)*sizeof(int));
        g->grane[g->cvorovi[g->dim].broj] = drugi;
        int i;
        for(i = g->cvorovi[g->dim].broj; i != g->cvorovi[jedan+1].broj; i--)
        {
            g->grane[i] = g->grane[i-1];
        }
        g->grane[i] = drugi;
            
        for(i = jedan + 1; i<=g->dim; i++)
        {
            g->cvorovi[i].broj++;
        }
    }
}

void izbaciGranu(Graf *g, int jedan, int drugi)
{
    int nadjenaGrana = 0, edgeIndeksJednog;
    for(int i = g->cvorovi[jedan].broj; i != g->cvorovi[jedan+1].broj; i++)
    {
        if(g->grane[i] == drugi)
        {
            nadjenaGrana = 1;
            edgeIndeksJednog = i;
        }
    }
    if(nadjenaGrana == 1)
    {
        for(int i = edgeIndeksJednog; i != g->cvorovi[g->dim].broj-1; i++)
        {
            g->grane[i] = g->grane[i+1];
        }
        for(int i = jedan+1; i<=g->dim; i++)
        {
            g->cvorovi[i].broj--;
        }
        g->grane = realloc(g->grane, (g->cvorovi[g->dim].broj)*sizeof(int));
    }
}

int centralnostCvora(Graf *g, int indeks)
{
    int brojac = 0;
    for(int i = g->cvorovi[indeks].broj; i<g->cvorovi[indeks+1].broj; i++)
    {
        if(g->cvorovi[g->grane[i]].aktivan == 0) continue;
        if(g->grane[i] == i) brojac += 2;
        else brojac += 1;
    }
    return brojac;
}

int nadjiGranu(Graf *g, int jedan, int drugi)
{
    for(int i = g->cvorovi[jedan].broj; i != g->cvorovi[jedan+1].broj; i++)
    {
        if(g->grane[i] == drugi) return 1;
    }
    return 0;
}

void flojd(Graf *g, int **w, int **t)
{
    for (int k = 0; k< g->dim; k++)
    {
        for (int i = 0; i< g->dim; i++)
        {
            for (int j = 0; j< g->dim; j++)
            {
                if (w[i][k] != INT_MAX && w[k][j] != INT_MAX && w[i][j] > w[i][k] + w[k][j])
                {
                    t[i][j] = t[k][j];
                    w[i][j] = w[i][k] + w[k][j];
                }
            }
        }
    }
}

void ispisiPut(int **t, int i, int j)
{
    if(t[i][j] == -1) printf("%d: %s\n", j, "Nije dostizan");
    else
    {
        int* niz = malloc(sizeof(int));
        niz[0] = j;
        int brojacEl = 1;
        int k = j;
        while(i != k)
        {
            niz = realloc(niz, (brojacEl+1)*sizeof(int));
            brojacEl++;
            k = t[i][k];
            niz[brojacEl-1] = k;
        }
        brojacEl--;
        printf("%d: ", j);
        while(brojacEl > -1)
        {
            printf("%d", niz[brojacEl]);
            if(brojacEl > 0) printf("%s", " -> ");
            else putchar('\n');
            brojacEl--;
        }
        free (niz);
    }
}

double frag(Graf *g, int** w)
{
    double deljenik = 0;
    double delilac = 0;
    for (int i = 0; i< g->dim; i++)
    {
        for (int j = 0; j< g->dim; j++)
        {
            if(g->cvorovi[i].aktivan && g->cvorovi[j].aktivan)
            {
                delilac++;
                if(w[i][j] == 1) deljenik++;
            }
        }
    }
    return deljenik / delilac;
}

void main()
{
    puts("======================================");
    puts("==== ~ ASP1 3. domaci - GRAFOVI ~ ====");
    puts("======================================");

    puts("1. Unos sa std. ulaza, 2. Unos iz datoteke\nIzaberite: ");
    int ulaz;
    int tmp;
    while (1) {
        tmp = scanf("%d", &ulaz);
        if (tmp != 1 || ulaz < 1 || ulaz > 2) {
            puts("Greska u unosu.\nIzaberite: ");
        } else break;
    }

    FILE *input;
    char nazivDat[256];
    if (ulaz == 1)
    {
        input = stdin;
    }
    else
    {
        puts("Unesite naziv datoteke: ");
        while (1) {
            scanf("%s", nazivDat);
            input = fopen(nazivDat, "r");
            if (input == NULL) {
                puts("Greska. Datoteka ne postoji.\nUnesite naziv datoteke: ");
            } else break;
        }
    }
    int dim;
    puts("Upisati nenegativan broj cvorova: ");
    while (1) {
        tmp = fscanf(input, "%d", &dim);
        if (tmp != 1 || dim < 0) {
            puts("Greska u unosu.\nUpisati nenegativan broj cvorova: ");
        } else break;
    }

    int grane;
    Graf *g = napraviPrazanGraf(dim);
    puts("Upisati broj grana: ");
    while (1) {
        tmp = fscanf(input, "%d", &grane);
        if (tmp != 1 || grane < 0) {
            puts("Greska u unosu.\nUpisati broj grana: ");
        } else break;
    }

    for (int i = 0; i < grane; i++)
    {
        puts("Unesite dva cvora iz grafa. Numerisanje se vrsi od nule. ");
        int jedan, drugi;
        while(1)
        {
            tmp = fscanf(input,"%d %d", &jedan, &drugi);
            if(tmp != 2 || jedan < 0 || jedan >= dim || drugi < 0 || drugi >= dim ||
               g->cvorovi[jedan].aktivan == 0 || g->cvorovi[drugi].aktivan == 0)
            {
                puts("Greska u unosu (bar jedan cvor ne postoji ili nije u grafu).\nUnesite dva cvora iz grafa: ");
            }
            else break;
        }
        dodajGranu(g, jedan, drugi);
        if(jedan != drugi) dodajGranu(g, drugi, jedan);
    }
    while(1)
    {
        putchar('\n');
        putchar('\n');
        puts("1. dodavanje i 2. uklanjanje cvora,\n3. dodavanje i 4. uklanjanje grane,\n5. ispis reprezentacije grafa,\n"
             "6. brisanje grafa iz memorije i pravljenje novog bez grana,\n7. dostiznost cvora,\n8. fragmentacija grafa,\n9. centralnost cvora po stepenu,\n10. izlazak iz programa i brisanje grafa iz memorije.\nIzaberite: ");
        int izbor;

        while(1)
        {
            tmp = fscanf(input,"%d", &izbor);
            if(tmp != 1 || izbor < 1 || izbor > 10)
            {
                puts("Greska u unosu.\nIzaberite: ");
            }
            else break;
        }
        if(izbor == 1)
        {
            dodajCvor(g);
            dim++;
            puts("Novi cvor je dodat na najmanji raspolozivi indeks.");
        }
        else if(izbor == 2)
        {
            puts("Unesite jedan cvor iz grafa. Numerisanje se vrsi od nule. ");
            int indeks;
            while(1)
            {
                tmp = fscanf(input,"%d", &indeks);
                if(tmp != 1 || indeks < 0 || indeks >= dim || g->cvorovi[indeks].aktivan == 0)
                {
                    puts("Greska u unosu (cvor ne postoji ili nije u grafu).\nUnesite jedan cvor iz grafa: ");
                }
                else break;
            }
            izbaciCvor(g, indeks);
            puts("Trazeni cvor je izbacen.");
        }
        else if(izbor == 3)
        {
            puts("Unesite dva cvora iz grafa. Numerisanje se vrsi od nule. ");
            int jedan, drugi;
            while(1)
            {
                tmp = fscanf(input,"%d %d", &jedan, &drugi);
                if(tmp != 2 || jedan < 0 || jedan >= dim || drugi < 0 || drugi >= dim ||
                g->cvorovi[jedan].aktivan == 0 || g->cvorovi[drugi].aktivan == 0)
                {
                    puts("Greska u unosu (bar jedan cvor ne postoji ili nije u grafu).\nUnesite dva cvora iz grafa: ");
                }
                else break;
            }
            dodajGranu(g, jedan, drugi);
            if(jedan != drugi) dodajGranu(g, drugi, jedan);
        }
        else if(izbor == 4)
        {
            puts("Unesite dva cvora iz grafa. Numerisanje se vrsi od nule. ");
            int jedan, drugi;
            while(1)
            {
                tmp = fscanf(input,"%d %d", &jedan, &drugi);
                if(tmp != 2 || jedan < 0 || jedan >= dim || drugi < 0 || drugi >= dim ||
                g->cvorovi[jedan].aktivan == 0 || g->cvorovi[drugi].aktivan == 0)
                {
                    puts("Greska u unosu.\nUnesite dva cvora iz grafa: ");
                }
                else break;
            }
            izbaciGranu(g, jedan, drugi);
            if(jedan != drugi) izbaciGranu(g, drugi, jedan);
        }
        else if(izbor == 5)
        {
            puts("Graf sadrzi sledece cvorove: ");
            ispisGrafa(g);
        }
        else if(izbor == 6)
        {
            puts("Unesite pozitivan broj cvorova: ");
            while(1)
            {
                tmp = fscanf(input,"%d", &dim);
                if(tmp != 1 || dim < 1)
                {
                    puts("Greska u unosu.\nUnesite pozitivan broj cvorova: ");
                }
                else break;
            }
            oslobodiGraf(g);
            g = napraviPrazanGraf(dim);
            puts("Napravljen je prazan graf.\n");
        }
        else if(izbor == 7 || izbor == 8)
        {
            int **w = malloc(dim*sizeof(int*));
            int **t = malloc(dim*sizeof(int*));
            for(int i = 0; i<dim; i++)
            {
                w[i] = malloc(dim*sizeof(int));
                t[i] = malloc(dim*sizeof(int));
                for(int j = 0; j<dim; j++)
                {
                    w[i][j] = 0;
                    t[i][j] = 0;
                    if (g->cvorovi[i].aktivan == 0 || g->cvorovi[j].aktivan == 0) w[i][j] = INT_MAX;
                    else if(i == j) w[i][j] = 0;
                    else if(nadjiGranu(g, i,j) == 1) w[i][j] = 1;
                    else w[i][j] = INT_MAX;

                    if (g->cvorovi[i].aktivan == 0 || g->cvorovi[j].aktivan == 0) t[i][j] = INT_MAX;
                    else if(w[i][j] == INT_MAX) t[i][j] = -1;
                    else t[i][j] = i;
                }
            }

            flojd(g, w, t);

            if(izbor == 7)
            {
                puts("Unesite jedan cvor iz grafa. Numerisanje se vrsi od nule. ");
                int i;
                while(1)
                {
                    tmp = fscanf(input,"%d", &i);
                    if(tmp != 1 || i < 0 || i >= dim || g->cvorovi[i].aktivan == 0)
                    {
                        puts("Greska u unosu (cvor ne postoji ili nije u grafu).\nUnesite jedan cvor iz grafa: ");
                    }
                    else break;
                }
                for(int j = 0; j<dim; j++) if(i != j && g->cvorovi[j].aktivan == 1) ispisiPut(t, i, j);
            }
            if(izbor == 8)
            {
                printf("Fragmentacija grafa je: %lf.\n", frag(g, w));
            }
            for(int i = 0; i<dim; i++)
            {
                free(w[i]);
                free(t[i]);
            }
            free(w);
            free(t);
        }
        else if(izbor == 9)
        {
            puts("Unesite jedan cvor iz grafa. Numerisanje se vrsi od nule. ");
            int indeks;
            while(1)
            {
                tmp = fscanf(input,"%d", &indeks);
                if(tmp != 1 || indeks < 0 || indeks >= dim || g->cvorovi[indeks].aktivan == 0)
                {
                    puts("Greska u unosu (cvor ne postoji ili nije u grafu).\nUnesite jedan cvor iz grafa: ");
                }
                else break;
            }
            printf("Centralnost cvora %d po stepenu je %d.\n", indeks, centralnostCvora(g, indeks));
        }
        else
        {
            oslobodiGraf(g);
            puts("Napustate program. Dovidjenja!");
            fclose(input);
            break;
        }
    }
}