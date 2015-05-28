import random

def kombiniraj(parametri):
    # parametri = [p1, p2, p3]
    novi = []
    en = []
    seznam = []
    for i in range(3):
        for j in range(3):
            if i != j:
                for m in range(len(parametri[0])):
                    if random.randint(1, 10)<6:
                        en.append(parametri[i][m])
                    else: en.append(parametri[j][m])
                novi.append(en)
                seznam = []
                en = []
    for i in range(len(novi)):
        for j in range(len(parametri[0])):
            a = random.randint(1, 10)
            if a <= 2: en.append(novi[i][j]+1)
            elif a <= 4: en.append(novi[i][j]-1)
            elif a <= 6: en.append(novi[i][j]+2)
            elif a <= 8: en.append(novi[i][j]-2)
            else: en.append(novi[i][j])
        if en[5] < 1: en[5]=1
        if en[6] < 1 or en[6] > 4: en[6]=random.randint(1, 4)
        novi.append(en)
        en = []

    return novi
