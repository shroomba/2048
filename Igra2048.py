NARAVA = 'narava'
IGRALEC = 'igralec'

import random
import time

class Igra:
    def __init__(self):
        self.zgodovina=[]
        self.polje=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score=0
        self.stevilo_potez=0
        self.na_potezi=IGRALEC
        self.novaigra()


    def novaigra(self):
        self.polje=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score=0
        self.zgodovina=[]
        self.stevilo_potez=0
        par=self.nakljucno()
        self.povleci_narava(par)
        par=self.nakljucno()
        self.povleci_narava(par)
        self.na_potezi=IGRALEC
        self.zacetek=time.time()
        self.igra()


    def igra(self):
        if self.konec():
            print("KONEC")
            print(time.time()-self.zacetek)
        elif self.na_potezi==IGRALEC:
            (poteza, vrednost)=self.minimax(3, 2)
            print(self.poteze_igralca(self.polje))
            print(poteza)
            self.score=self.zgodovina[-1][2]
            self.stevilo_potez+=1
            self.povleci_igralec(poteza)
            print(self.score)
            print(self.stevilo_potez)
            self.igra()
        elif self.na_potezi==NARAVA:
            par=self.nakljucno()
            self.povleci_narava(par)
            self.narisi()
            self.igra()

    def narisi(self):
        print("{0[0][0]:=5} {0[0][1]:=5} {0[0][2]:=5} {0[0][3]:=5}".format(self.polje))
        print("{0[1][0]:=5} {0[1][1]:=5} {0[1][2]:=5} {0[1][3]:=5}".format(self.polje))
        print("{0[2][0]:=5} {0[2][1]:=5} {0[2][2]:=5} {0[2][3]:=5}".format(self.polje))
        print("{0[3][0]:=5} {0[3][1]:=5} {0[3][2]:=5} {0[3][3]:=5}".format(self.polje))
        

    def poteze_igralca(self, polje_kopija):
        seznam_potez=[]
        polje=[vrstica[:] for vrstica in polje_kopija]
        gor=polje_kopija!=self.gor(polje)

        polje=[vrstica[:] for vrstica in polje_kopija]
        dol=polje_kopija!=self.dol(polje)

        polje=[vrstica[:] for vrstica in polje_kopija]
        levo=polje_kopija!=self.levo(polje)

        polje=[vrstica[:] for vrstica in polje_kopija]
        desno=polje_kopija!=self.desno(polje)

        trus=[gor, dol, levo, desno]
        poteze=["gor", "dol", "levo", "desno"]
        for i in range(4):
            if trus[i]==True:
                seznam_potez.append(poteze[i])
        return seznam_potez

    def konec(self):
        a=self.poteze_igralca(self.polje)
        if len(a)==0:
            return True
        else: return False

    def shrani_pozicijo(self, polje, poteza):
        polje_kopija=[vrstica[:] for vrstica in polje]
        a=self.score
        self.zgodovina.append((polje_kopija, poteza, a))

    def nakljucno(self):
        prazni_i=[]
        prazni_j=[]
        for i in range(4):
            for j in range(4):
                if self.polje[i][j]==0:
                    prazni_i.append(i)
                    prazni_j.append(j)
        ena=random.randint(0, len(prazni_i)-1)
        return [prazni_i[ena], prazni_j[ena]]

    def poln(self, seznam):
        m=0
        for i in range(4):
            for j in range(4):
                if self.polje[i][j]==0:
                    m+=1
        if m==0: return True
        return False

    def minimax(self, k, globina):
        if globina == 0 or self.konec():
            return (None, self.vrednost())
        elif len(self.poteze_igralca(self.polje))==1:
            return (self.poteze_igralca(self.polje)[0], self.vrednost())
        else:
            if self.na_potezi==IGRALEC:
                ocena=300000
                #print self.poteze_igralca(self.polje)
                for poteza in self.poteze_igralca(self.polje):
                    self.povleci_igralec(poteza)
                    (smt, vrednost) = self.minimax(k, globina-1)
                    if vrednost<ocena:
                        ocena=vrednost
                        potezni_par=(poteza, ocena)
                    #print (poteza, vrednost)
                    self.zgodovina.pop(-1)
                    self.polje=[vrstica[:] for vrstica in self.zgodovina[-1][0]]
                return potezni_par
            else:
                ocene=[]
                poteze=self.poteze_narave(k)
                if len(self.poteze_narave(k))==0:
                    a=self.vrednost()
                    return (None, a)
                for poteza in poteze:
                    self.polje[poteza[0]][poteza[1]]=2
                    (smt, vrednost2) = self.minimax(k, globina-1)
                    self.polje[poteza[0]][poteza[1]]=4
                    (smt, vrednost4) = self.minimax(k, globina-1)
                    a=0.9*int(vrednost2)+0.1*int(vrednost4)
                    ocene.append(a)
                    self.polje[poteza[0]][poteza[1]]=0
                self.na_potezi=IGRALEC
                v=sum(ocene)/len(ocene)
                return (None, v)

    def poteze_narave(self, k):
        prazni=[]
        for i in range(4):
            for j in range(4):
                if self.polje[i][j]==0:
                    prazni.append([i, j])
        if len(prazni)<k:
            return prazni
        else: return random.sample(prazni, k)
            

    def vrednost(self):
        prazni=2*self.vrednost_prazni()
        razlika=self.vrednost_razlika()
        povprecje=self.povprecna()
        pari=self.pari()
        ocena=razlika-povprecje-pari
        return ocena
        
    def vrednost_prazni(self):
        ocena=0
        for i in range(3):
            for j in range(3):
                if self.polje[i][j]==0:
                    if self.polje[i][j+1]!=0:
                        ocena+=1
                    if self.polje[i+1][j]!=0:
                        ocena+=1
                elif self.polje[i][j]!=0:
                    if self.polje[i][j+1]==0:
                        ocena+=1
                    if self.polje[i+1][j]!=0:
                            ocena+=1
        for i in range(3):
            if self.polje[i][3]==0 and self.polje[i+1][3]!=0:
                ocena+=1
            if self.polje[i][3]!=0 and self.polje[i+1][3]==0:
                ocena+=1
        for j in range(3):
            if self.polje[3][j]==0:
                if self.polje[3][j+1]!=0:
                    ocena+=1
            else:
                if self.polje[3][j+1]==0:
                    ocena+=1
        return ocena

    def vrednost_razlika(self):
        ocena=0
        for i in range(3):
            for j in range(3):
                if self.polje[i][j]!=0:
                    if self.polje[i][j+1]!=0:
                        ocena+=abs(self.polje[i][j]-self.polje[i][j+1])
                    elif self.polje[i+1][j]!=0:
                        ocena+=abs(self.polje[i][j]-self.polje[i+1][j])
        for j in range(3):
            if self.polje[3][j]!=0 and self.polje[3][j+1]!=0:
                ocena+=abs(self.polje[3][j]-self.polje[3][j+1])
        for i in range(3):
            if self.polje[i][3]!=0 and self.polje[i+1][3]!=0:
                ocena+=abs(self.polje[i][3]-self.polje[i+1][3])
        return ocena

    def povprecna(self):
        prazni=0
        ostali=0
        for i in range(4):
            for j in range(4):
                if self.polje[i][j]==0:
                    prazni+=1
                else:
                    ostali+=self.polje[i][j]
        return ostali/(16-prazni)

    def dodatna_razlika(self):
        ocena=0
        for i in range(3):
            pass

    def pari(self):
        ocena=0
        for i in range(3):
            for j in range(3):
                if self.polje[i][j]==self.polje[i][j+1]:
                    ocena+=self.polje[i][j]
                if self.polje[i][j]==self.polje[i+1][j]:
                    ocena+=self.polje[i][j]
        for j in range(3):
            if self.polje[3][j]==self.polje[3][j+1]:
                ocena+=self.polje[3][j]
        for i in range(3):
            if self.polje[i][3]==self.polje[i+1][3]:
                ocena+=self.polje[i][3]
        return ocena


    def povleci_narava(self, par):
        if random.randint(1, 10)<=2: a=4
        else: a=2
        self.polje[par[0]][par[1]]=a
        self.shrani_pozicijo(self.polje, NARAVA)
        self.na_potezi=IGRALEC

    def povleci_igralec(self, poteza):
        if poteza=="gor":
            self.gor(self.polje)
        elif poteza=="dol":
            self.dol(self.polje)
        elif poteza=="levo":
            self.levo(self.polje)
        elif poteza=="desno":
            self.desno(self.polje)
        self.shrani_pozicijo(self.polje, IGRALEC)
        self.na_potezi=NARAVA

    def gor(self, polje):
        self.premaknigor(polje)
        self.zdruzigor(polje)
        self.premaknigor(polje)
        return polje

    def dol(self, polje):
        self.premaknidol(polje)
        self.zdruzidol(polje)
        self.premaknidol(polje)
        return polje


    def desno(self, polje):
        self.premaknidesno(polje)
        self.zdruzidesno(polje)
        self.premaknidesno(polje)
        return polje

    def levo(self, polje):
        self.premaknilevo(polje)
        self.zdruzilevo(polje)
        self.premaknilevo(polje)
        return polje

    def premaknigor(self, polje):
        '''Premakne vse ploscice gor.'''
        for j in range(4):
            if polje[1][j]!=0:
                if polje[0][j]==0:
                    polje[0][j]=polje[1][j]
                    polje[1][j]=0

            if polje[2][j]!=0:
                if polje[0][j]==0:
                    polje[0][j]=polje[2][j]
                    polje[2][j]=0
                elif polje[1][j]==0:
                    polje[1][j]=polje[2][j]
                    polje[2][j]=0

            if polje[3][j]!=0:
                if polje[0][j]==0:
                    polje[0][j]=polje[3][j]
                    polje[3][j]=0
                elif polje[1][j]==0:
                    polje[1][j]=polje[3][j]
                    polje[3][j]=0
                elif polje[2][j]==0:
                    polje[2][j]=polje[3][j]
                    polje[3][j]=0

    def zdruzigor(self, polje):
        for i in range(3):
            for j in range(4):
                if polje[i][j]==polje[i+1][j]:
                    polje[i][j]=polje[i][j]*2
                    polje[i+1][j]=0
                    self.score+=polje[i][j]

    def premaknidol(self, polje):
        for j in range(4):
            if polje[2][j]!=0:
                if polje[3][j]==0:
                    polje[3][j]=polje[2][j]
                    polje[2][j]=0

            if polje[1][j]!=0:
                if polje[3][j]==0:
                    polje[3][j]=polje[1][j]
                    polje[1][j]=0
                elif polje[2][j]==0:
                    polje[2][j]=polje[1][j]
                    polje[1][j]=0

            if polje[0][j]!=0:
                if polje[3][j]==0:
                    polje[3][j]=polje[0][j]
                    polje[0][j]=0
                elif polje[2][j]==0:
                    polje[2][j]=polje[0][j]
                    polje[0][j]=0
                elif polje[1][j]==0:
                    polje[1][j]=polje[0][j]
                    polje[0][j]=0

    def zdruzidol(self, polje):
        for i in range(1,4):
            for j in range(4):
                if polje[4-i][j]==polje[3-i][j]:
                    polje[4-i][j]=2*polje[4-i][j]
                    polje[3-i][j]=0
                    self.score+=polje[4-i][j]

    def premaknilevo(self, polje):
        for i in range(4):
            if polje[i][1]!=0:
                if polje[i][0]==0:
                    polje[i][0]=polje[i][1]
                    polje[i][1]=0

            if polje[i][2]!=0:
                if polje[i][0]==0:
                    polje[i][0]=polje[i][2]
                    polje[i][2]=0
                elif polje[i][1]==0:
                    polje[i][1]=polje[i][2]
                    polje[i][2]=0

            if polje[i][3]!=0:
                if polje[i][0]==0:
                    polje[i][0]=polje[i][3]
                    polje[i][3]=0
                elif polje[i][1]==0:
                    polje[i][1]=polje[i][3]
                    polje[i][3]=0
                elif polje[i][2]==0:
                    polje[i][2]=polje[i][3]
                    polje[i][3]=0

    def zdruzilevo(self, polje):
        for j in range(3):
            for i in range(4):
                if polje[i][j]==polje[i][j+1]:
                    polje[i][j]=polje[i][j]*2
                    polje[i][j+1]=0
                    self.score+=polje[i][j]

    def premaknidesno(self, polje):
        for i in range(4):
            if polje[i][2]!=0:
                if polje[i][3]==0:
                    polje[i][3]=polje[i][2]
                    polje[i][2]=0

            if polje[i][1]!=0:
                if polje[i][3]==0:
                    polje[i][3]=polje[i][1]
                    polje[i][1]=0
                elif polje[i][2]==0:
                    polje[i][2]=polje[i][1]
                    polje[i][1]=0

            if polje[i][0]!=0:
                if polje[i][3]==0:
                    polje[i][3]=polje[i][0]
                    polje[i][0]=0
                elif polje[i][2]==0:
                    polje[i][2]=polje[i][0]
                    polje[i][0]=0
                elif polje[i][1]==0:
                    polje[i][1]=polje[i][0]
                    polje[i][0]=0

    def zdruzidesno(self, polje):
        for j in range(1, 4):
            for i in range(4):
                if polje[i][4-j]==polje[i][3-j]:
                    polje[i][4-j]=polje[i][4-j]*2
                    polje[i][3-j]=0
                    self.score+=polje[i][4-j]


Igra()
