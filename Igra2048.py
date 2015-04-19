NARAVA = 'narava'
IGRALEC = 'igralec'

import random
import time

class Igra:
    def __init__(self):
        self.zgodovina=[]
        self.polje=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score=0
        self.s=0
        self.na_potezi=IGRALEC
        par=self.nakljucno()
        self.polje[par[0]][par[1]]=2
        par=self.nakljucno()
        self.povleci_narava(par)
        self.narisi()
        self.zgodovina.append((self.polje, NARAVA))
        self.igra()

    def novaigra(self):
        self.polje=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score=0
        self.s=0
        par=self.nakljucno()
        self.povleci_narava(par)
        par=self.nakljucno()
        self.povleci_narava(par)
        self.na_potezi=IGRALEC
        self.igra()


    def igra(self):
        if self.konec():
            print("KONEC")
        elif self.na_potezi==IGRALEC:
            #(poteza, vrednost)=self.minimax(3, 2)
            a=self.minimax(3, 2)
            poteza=a[0]
            print(poteza)
            self.povleci_igralec(poteza)
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
        self.zgodovina.append((polje_kopija, poteza))

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
            return None, self.vrednost()
        else:
            if self.na_potezi==IGRALEC:
                ocena=30000
                for poteza in self.poteze_igralca(self.polje):
                    self.povleci_igralec(poteza)
                    (smt, vrednost) = self.minimax(k, globina-1)
                    print(poteza+" "+str(vrednost))
                    if vrednost<ocena:
                        ocena=vrednost
                        potezni_par=(poteza, ocena)
                    self.zgodovina.pop(-1)
                    self.polje=[vrstica[:] for vrstica in self.zgodovina[-1][0]]
                return potezni_par
            else:
                ocene=[]
                poteze=self.poteze_narave(k)
                if len(self.poteze_narave(k))==0:
                    a=self.vrednost()
                    return a
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
        prazni=self.vrednost_prazni()
        razlika=self.vrednost_razlika()
        #plosca=self.vrednost_plosce()
        ocena=prazni+razlika #-plosca
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
                ocena+=abs(self.polje[i][j]-self.polje[i][j+1])
        return ocena
                
    def vrednost_plosce(self):
        ocena=0
        for i in range(4):
            for j in range(4):
                ocena+=self.polje[i][j]
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


    def gor(self, seznam):
        self.premaknigor(seznam)
        self.zdruzigor(seznam)
        self.premaknigor(seznam)
#        self.nakljucno()
#         self.narisi()
        return seznam

    def dol(self, seznam):
        self.premaknidol(seznam)
        self.zdruzidol(seznam)
        self.premaknidol(seznam)
#        self.nakljucno()
#         self.narisi()
        return seznam

    def desno(self, seznam):
        self.premaknidesno(seznam)
        self.zdruzidesno(seznam)
        self.premaknidesno(seznam)
#        self.nakljucno()
#         self.narisi()
        return seznam

    def levo(self, seznam):
        self.premaknilevo(seznam)
        self.zdruzilevo(seznam)
        self.premaknilevo(seznam)
#        self.nakljucno()
#         self.narisi()
        return seznam


    def premaknigor(self, seznam):
        '''Premakne vse ploscice gor.'''
        for j in range(4):
            if seznam[1][j]!=0:
                if seznam[0][j]==0:
                    seznam[0][j]=seznam[1][j]
                    seznam[1][j]=0

            if seznam[2][j]!=0:
                if seznam[0][j]==0:
                    seznam[0][j]=seznam[2][j]
                    seznam[2][j]=0
                elif seznam[1][j]==0:
                    seznam[1][j]=seznam[2][j]
                    seznam[2][j]=0

            if seznam[3][j]!=0:
                if seznam[0][j]==0:
                    seznam[0][j]=seznam[3][j]
                    seznam[3][j]=0
                elif seznam[1][j]==0:
                    seznam[1][j]=seznam[3][j]
                    seznam[3][j]=0
                elif seznam[2][j]==0:
                    seznam[2][j]=seznam[3][j]
                    seznam[3][j]=0
        return seznam

    def zdruzigor(self, seznam):
        '''Zdruzi vse mozne ploscice.'''
        for i in range(3):
            for j in range(4):
                if seznam[i][j]==seznam[i+1][j]:
                    seznam[i][j]=seznam[i][j]*2
                    seznam[i+1][j]=0
                    self.score+=seznam[i][j]
        return seznam

    def premaknidol(self, seznam):
        for j in range(4):
            if seznam[2][j]!=0:
                if seznam[3][j]==0:
                    seznam[3][j]=seznam[2][j]
                    seznam[2][j]=0

            if seznam[1][j]!=0:
                if seznam[3][j]==0:
                    seznam[3][j]=seznam[1][j]
                    seznam[1][j]=0
                elif seznam[2][j]==0:
                    seznam[2][j]=seznam[1][j]
                    seznam[1][j]=0

            if seznam[0][j]!=0:
                if seznam[3][j]==0:
                    seznam[3][j]=seznam[0][j]
                    seznam[0][j]=0
                elif seznam[2][j]==0:
                    seznam[2][j]=seznam[0][j]
                    seznam[0][j]=0
                elif seznam[1][j]==0:
                    seznam[1][j]=seznam[0][j]
                    seznam[0][j]=0
        return seznam

    def zdruzidol(self, seznam):
        for i in range(1,4):
            for j in range(4):
                if seznam[4-i][j]==seznam[3-i][j]:
                    seznam[4-i][j]=2*seznam[4-i][j]
                    seznam[3-i][j]=0
                    self.score+=seznam[4-i][j]
        return seznam

    def premaknilevo(self, seznam):
        for i in range(4):
            if seznam[i][1]!=0:
                if seznam[i][0]==0:
                    seznam[i][0]=seznam[i][1]
                    seznam[i][1]=0

            if seznam[i][2]!=0:
                if seznam[i][0]==0:
                    seznam[i][0]=seznam[i][2]
                    seznam[i][2]=0
                elif seznam[i][1]==0:
                    seznam[i][1]=seznam[i][2]
                    seznam[i][2]=0

            if seznam[i][3]!=0:
                if seznam[i][0]==0:
                    seznam[i][0]=seznam[i][3]
                    seznam[i][3]=0
                elif seznam[i][1]==0:
                    seznam[i][1]=seznam[i][3]
                    seznam[i][3]=0
                elif seznam[i][2]==0:
                    seznam[i][2]=seznam[i][3]
                    seznam[i][3]=0
        return seznam

    def zdruzilevo(self, seznam):
        for j in range(3):
            for i in range(4):
                if seznam[i][j]==seznam[i][j+1]:
                    seznam[i][j]=seznam[i][j]*2
                    seznam[i][j+1]=0
                    self.score+=seznam[i][j]
        return seznam


    def premaknidesno(self, seznam):
        for i in range(4):
            if seznam[i][2]!=0:
                if seznam[i][3]==0:
                    seznam[i][3]=seznam[i][2]
                    seznam[i][2]=0

            if seznam[i][1]!=0:
                if seznam[i][3]==0:
                    seznam[i][3]=seznam[i][1]
                    seznam[i][1]=0
                elif seznam[i][2]==0:
                    seznam[i][2]=seznam[i][1]
                    seznam[i][1]=0

            if seznam[i][0]!=0:
                if seznam[i][3]==0:
                    seznam[i][3]=seznam[i][0]
                    seznam[i][0]=0
                elif seznam[i][2]==0:
                    seznam[i][2]=seznam[i][0]
                    seznam[i][0]=0
                elif seznam[i][1]==0:
                    seznam[i][1]=seznam[i][0]
                    seznam[i][0]=0
        return seznam

    def zdruzidesno(self, seznam):
        for j in range(1, 4):
            for i in range(4):
                if seznam[i][4-j]==seznam[i][3-j]:
                    seznam[i][4-j]=seznam[i][4-j]*2
                    seznam[i][3-j]=0
                    self.score+=seznam[i][4-j]
        return seznam


Igra()
