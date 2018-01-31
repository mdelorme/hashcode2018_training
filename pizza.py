import sys

# R : Rows
# C : Cols
# L : Minimum of each ingredient in a slice
# H : Maximum cells of a slice
R, C, L, H = (int(x) for x in input().split())

# Grid represente la pizza, c'est une liste de liste (row-major)
grid = []
for r in range(R):
    grid += [list(input())]

# Types de rectangles possibles
rect = []
def generate_rectangles():
    global rect
    for j in range(L, H+1):
        for i in range(1, j+1):
            if j%i == 0:
                rect += [(i, j//i)]
generate_rectangles()
print('Total possible rectangles : {}'.format(len(rect)), file=sys.stderr)
            

# Dans la suite du code, une partition est un 4-tuple (x0, y0, x1, y1)
def ncells(partition):
    ''' Nombre de cellules dans une partition '''
    return (partition[2]-partition[0]) * (partition[3]-partition[1])

def contents(partition):
    ''' 
    Renvoie le contenu d'une partition sous la forme d'un couple
    (Mushroom, Tomato)
    '''
    M = 0 # Champignons
    T = 0 # Tomates
    for x in range(partition[0], partition[2]+1):
        for y in range(partition[1], partition[3]+1):
            if grid[y][x] == 'M':
                M += 1
            else:
                T += 1
    return M, T
            

def score(p_list):
    ''' Score total sur une liste de partitions '''
    return sum(ncells(x) for x in p_list)

def is_valid(p_list):
    ''' 
    Est-ce que la liste de partition est valide ?
    Rappel des critères de validité :
     - Chaque cellule doit appartenir, au plus a une partition.
     - Le nombre de cellules d'une partition ne peut depasser H
     - Chaque partition doit contenir au moins L ingredients de chaque type
    '''
    g = [[False]*C for _ in range(R)]
    for p in p_list:
        # Pas assez d'ingredients
        M, T = contents(p)
        if M < L or T < L:
            return False

        # Surface trop grande
        if ncells(p) > H:
            return False

        # On verifie que les cellules ne sont pas en double
        for x in range(p[0], p[2]+1):
            for y in range(p[1], p[3]+1):
                if g[y][x]:
                    return False
                g[y][x] = True
    return True


    
