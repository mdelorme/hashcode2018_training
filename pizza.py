import sys

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
def ncells(partition):
    ''' Nombre de cellules dans une partition '''
    # En exemple, entre le rows (0, 2) et les columns (0, 1), il y a 6 elements
    return (partition[1]-partition[0]+1) * (partition[3]-partition[2]+1)

def contents(partition):
    ''' 
    Renvoie le contenu d'une partition sous la forme d'un couple
    (Mushroom, Tomato)
    '''
    M = 0 # Champignons
    T = 0 # Tomates
    for y in range(partition[2], partition[3]+1):
        for x in range(partition[0], partition[1]+1):
            if grid[y][x] == M_int:
                M += 1
            else:
                T += 1
    return M, T
            

def score(p_list):
    ''' Score total sur une liste de partitions '''
    return sum(ncells(x) for x in p_list)

def is_rectangle_valid(rect):
    # Dans les limites du terrain
    x0, x1, y0, y1 = rect
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
        for y in range(p[2], p[3]+1):
            for x in range(p[0], p[1]+1):
                if g[y][x]:
                    return False
                g[y][x] = True


    x0, x1, y0, y1 = rect
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
    # g = [[False]*C for _ in range(R)]
    for p in p_list:
        # Pas assez d'ingredients
        M, T = contents(p)
        if M < L or T < L:
            return False

        # Surface trop grande
        if (M + T) > H:
            return False

        # # On verifie que les cellules ne sont pas en double
        # for x in range(p[0], p[1]+1):
        #     for y in range(p[2], p[3]+1):
        #         if g[y][x]:
        #             return False
        #         g[y][x] = True
    return True


best_score     = -1
best_partition = None

def recur_aux(l_partition):
    global best_score

    for cur_x in range(C - 1):
        for cur_y in range(R - 1):

            for shape in rect:
                cur_rect = (cur_x, cur_x + shape[0] - 1, cur_y, cur_y + shape[1] - 1)
                if (not is_rectangle_valid(cur_rect)):
                    continue

                if (does_overlap(l_partition, cur_rect)):
                    continue

                l_partition.append(cur_rect)
                # print("l_partition ", l_partition, is_valid(l_partition))
                # print("is_valid(cur_rect) ")
                if (is_valid(l_partition)):
                # if (is_valid(l_partition) and (best_score < score(l_partition))):
                    # print("score", score(l_partition))
                    if (best_score < score(l_partition)):
                        print("best_partition:", l_partition, score(l_partition))
                        best_score     = score(l_partition)
                        best_partition = l_partition[:]
                    recur_aux(l_partition)
                l_partition.pop()


l_partition = []
recur_aux(l_partition)
