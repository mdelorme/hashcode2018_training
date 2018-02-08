import sys
from types import SimpleNamespace as sns

# R : Rows
# C : Cols
# L : Minimum of each ingredient in a slice
# H : Maximum cells of a slice
R, C, L, H = (int(x) for x in input().split())

print('Rows       : {}'.format(R))
print('Cols       : {}'.format(C))
print('Minimum (L): {}'.format(L))
print('Maximum (H): {}'.format(H))

M_int = 0
T_int = 1
# Grid represente la pizza, c'est une liste de liste (row-major)
grid = []
for r in range(R):
    # grid += [list(input())]
    l = list(input())
    l = list(map(lambda c : M_int if (c == "M") else T_int, l))
    # print("l", l)
    grid += [l]

# Types de rectangles possibles
def generate_rectangles():
    rect = []
    # Le rectangle le plus petit compte au moins L mushroom ET L tomato
    # for j in range(2*L, H+1):
    for j in range(H, 2*L - 1, -1):
        for i in range(1, j+1):
            if j%i == 0:
                rect += [(i, j//i)]
    return rect

rect = generate_rectangles()
print('Total possible rectangles : {}'.format(len(rect)), file=sys.stderr)
print (rect)

# Dans la suite du code, une partition est un 4-tuple (x0, x1, y0, y1)
def ncells(p):
    ''' Nombre de cellules dans une partition '''
    # En exemple, entre le rows (0, 2) et les columns (0, 1), il y a 6 elements
    return (p.x1 - p.x0 + 1) * (p.y1 - p.y0 + 1)

def contents(p):
    ''' 
    Renvoie le contenu d'une partition sous la forme d'un couple
    (Mushroom, Tomato)
    '''
    M = 0 # Champignons
    T = 0 # Tomates
    for y in range(p.y0, p.y1 + 1):
        for x in range(p.x0, p.x1 + 1):
            if grid[y][x] == M_int:
                M += 1
            else:
                T += 1
    return M, T
            

def score(p_list):
    ''' Score total sur une liste de partitions '''
    return sum(ncells(p) for p in p_list)

def is_rectangle_valid(rect):
    # Dans les limites du terrain
    x0, x1, y0, y1 = rect.x0, rect.x1, rect.y0, rect.y1
    if ((x0 < 0) or ((C - 1) < x0) or
        (x1 < 0) or ((C - 1) < x1) or
        (y0 < 0) or ((R - 1) < y0) or
        (y1 < 0) or ((R - 1) < y1)):
        return False
    return True

def does_overlap(p_list, rect):
    g = [[False]*C for _ in range(R)]
    for p in p_list:
        # On verifie que les cellules ne sont pas en double
        for y in range(p.y0, p.y1 + 1):
            for x in range(p.x0, p.x1 + 1):
                if g[y][x]:
                    return False
                g[y][x] = True


    x0, x1, y0, y1 = rect.x0, rect.x1, rect.y0, rect.y1
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if g[y][x]:
                return True

    return False
    

def is_valid(p_list):
    ''' 
    Est-ce que la liste de partition est valide ?
    Rappel des critères de validité :
     - Chaque cellule doit appartenir, au plus a une partition.
     - Le nombre de cellules d'une partition ne peut depasser H
     - Chaque partition doit contenir au moins L ingredients de chaque type
    '''
    for p in p_list:
        # Pas assez d'ingredients
        M, T = contents(p)
        if M < L or T < L:
            return False

        # Surface trop grande
        if (M + T) > H:
            return False

    return True


best_score     = -1
best_partition = None

def backtrack(l_partition):
    global best_score

    for cur_x in range(C - 1):
        for cur_y in range(R - 1):
            for shape in rect:
                cur_rect = sns(x0 = cur_x,
                               x1 = cur_x + shape[0] - 1,
                               y0 = cur_y,
                               y1 = cur_y + shape[1] - 1)
                if (not is_rectangle_valid(cur_rect)):
                    continue

                if (does_overlap(l_partition, cur_rect)):
                    continue

                l_partition.append(cur_rect)
                if (is_valid(l_partition)):
                    if (best_score < score(l_partition)):
                        print("best_partition:", l_partition, score(l_partition))
                        best_score     = score(l_partition)
                        best_partition = l_partition[:]
                    backtrack(l_partition)
                l_partition.pop()


l_partition = []
backtrack(l_partition)
