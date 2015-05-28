__author__ = 'sarak'
from Igra2048 import Igra
import kombiniraj
import analyse

# prazni, par, razlika, povprecje, rob, k, globina
# p1=[0,1,3,-2,2,5]
# p2=[-1,4,2,0,4,3]
# p3=[0,2,3,-1,2,2]

p1 = [1, 0, -8, -1, 1, 7, 4]
p2 = [1, 0, 0, -8, 1, 7, 4]
p3 = [3, 0, 6, -3, 1, 4, 5]

parametri=[p1, p2, p3]

for j in range(13, 30):
    novi = kombiniraj.kombiniraj(parametri)
    parametri = parametri + novi

    for parameter in parametri:
        for i in range(20):
            print(parameter)
            print(i)
            Igra(parameter, j).novaigra()

    parametri = analyse.analiza(j)
