import sys
from types import SimpleNamespace as sns


#### Parse INPUT
input_file = sys.argv[1]
out_file = input_file.split(".")[0] + ".out"
print(out_file)

# R : Rows
# C : Cols
# L : Minimum of each ingredient in a slice
# H : Maximum cells of a slice
lines = open(input_file).readlines()
line = lines.pop(0)
R, C, L, H = (int(x) for x in line.split())

print('Rows       : {}'.format(R))
print('Cols       : {}'.format(C))
print('Minimum (L): {}'.format(L))
print('Maximum (H): {}'.format(H))

M_id = 0
T_id = 1

grid = []
for line in lines:
    # Grid represente la pizza, c'est une liste de liste (row-major)
    for r in range(R):
        l = list(line)
        l = list(map(lambda c : M_id if (c == "M") else T_id, l))
    grid += [l]
#### END Parse INPUT

# Types de shapes (formes) possibles
def generate_shapes():
    '''
    On fonction des paramètres L et H, on génére tous les formes de rectangles
    possibles. Ces formes contiennent au moins 2L éléments et au plus H éléments.
    '''
    shapes = []
    # La forme la plus petite compte au moins L mushroom ET L tomato
    for j in range(H, 2*L - 1, -1):
        for i in range(1, j+1):
            if j%i == 0:
                shapes += [sns(x=i, y=j//i)]
    return shapes

# Dans la suite du code, une partition est un 4-tuple (x0, x1, y0, y1)
def ncells(p):
    ''' Nombre de cellules dans une partition '''
    if (p is None):
        return 0
    else:
        # Par exemple, entre le rows (0, 2) et les columns (0, 1), il y a 6 elements
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
            if grid[y][x] == M_id:
                M += 1
            else:
                T += 1
    return M, T
            

def score(p_list):
    ''' Score total sur une liste de partitions '''
    return sum(ncells(p) for p in p_list)

def is_rectangle_valid(rect):
    ''' 
    Est-ce que qu'un rectangle est valide ?
    Rappel des critères de validité :
     - Un rectangle doit contenir au moins L mushroom et L tomate
     - Le nombre d'incrédient d'un rectangle ne peut depasser H
    '''
    # Dans les limites du terrain
    x0, x1, y0, y1 = rect.x0, rect.x1, rect.y0, rect.y1
    if ((x0 < 0) or ((C - 1) < x0) or
        (x1 < 0) or ((C - 1) < x1) or
        (y0 < 0) or ((R - 1) < y0) or
        (y1 < 0) or ((R - 1) < y1)):
        return False

    # Pas assez d'ingredients
    M, T = contents(rect)
    if M < L or T < L:
        return False

    # Surface trop grande
    if (M + T) > H:
        return False

    return True

class Pt(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle(object):
    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.y0, self.x0, self.y1, self.x1)

    def __str__(self):
        return "{} {} {} {}".format(self.y0, self.x0, self.y1, self.x1)

    def size(self):
        return (self.x1 - self.x0 + 1) * (self.y1 - self.y0 + 1)

    def __lt__(self, other):
        '''Permet de trier par taille les rectangles, et ensuite positions'''
        if (self.size() == other.size()):
            if ((self.x0 == other.x0) and
                (self.y0 == other.y0)):
                if (self.x1 == other.x1):
                    return self.y1 < other.y1
                else:
                    return self.x1 < other.x1
            else:
                if (self.x0 == other.x0):
                    return self.y0 < other.y0
                else:
                    return self.x0 < other.x0
        else:
            return self.size() < other.size()

    def __gt__(self, other):
        return other.__lt__(self)

    def contain(self, pt):
        return ((self.x0 <= pt.x) and (pt.x <= self.x1) and
                (self.y0 <= pt.y) and (pt.y <= self.y1))


def compute_l_seed_pt():
    '''
    Calcul l'ensemble des points seed possible
    '''
    whole_pizza = Rectangle(x0 = 0, x1 = C - 1, y0 = 0, y1 = R - 1)
    nb_M, nb_T = contents(whole_pizza)
    print("nb M", nb_M, "nb T", nb_T)

    ressource_min_id = None
    if (nb_M < nb_T):
        ressource_min_id = M_id
    else:
        ressource_min_id = T_id

    l_seed_pt = []
    for y in range(R):
        for x in range(C):
            if (grid[y][x] == ressource_min_id):
                l_seed_pt.append( Pt(x=x, y=y) )

    return l_seed_pt

def get_possible_rect(pt_seed, shapes):
    l_possible_rect = list()

    for shape in shapes:
        for x_offset in range(shape.x):
            for y_offset in range(shape.y):
                start_x = pt_seed.x - x_offset
                start_y = pt_seed.y - y_offset
                rect = Rectangle(start_x, start_x + shape.x -1,
                                 start_y, start_y + shape.y -1)
                if (is_rectangle_valid(rect)):
                    l_possible_rect.append(rect)

    return l_possible_rect

def compute_l_possible_rect():
    '''
    Calcul l'ensemble des rectangles possible. Les rectangles sont classés par taille,
    de la plus grande à la plus petite.
    '''
    s_possible_rect = set()

    shapes = generate_shapes()
    l_seed_pt = compute_l_seed_pt()
    for pt_seed in l_seed_pt:
        s_possible_rect = s_possible_rect.union (set (get_possible_rect (pt_seed, shapes)))

    l_possible_rect = sorted(list(s_possible_rect), reverse = True)
    return l_possible_rect

def does_overlap(p_list, len_p_list, rect):
    '''
    Calcul si un rectangle overlap les autres présents dans la liste p_list.
    '''
    for i in range(len_p_list):
        tmp_rect = p_list[i]
        for x in range(rect.x0, rect.x1 + 1):
            for y in range(rect.y0, rect.y1 + 1):
                if ((tmp_rect.x0 <= x) and (x <= tmp_rect.x1) and
                    (tmp_rect.y0 <= y) and (y <= tmp_rect.y1)):
                    return True

    return False

def print_n_write_best():
    '''
    Print la meilleure solution courante. Ecrit le fichier de sorti.
    '''
    global best_score, best_partition
    print("BEST Score:", best_score)
    to_print  = str(len(best_partition)) + "\n"
    to_print += "\n".join(map(lambda p : str(p), best_partition))
    print(to_print)

    h_out_file = open(out_file, "w")
    h_out_file.write(to_print)
    h_out_file.close()

best_score     = -1
best_partition = None

def backtrack():
    '''
    Calcul toutes les partitions possible sans appel recrusif : gain de temps.
    La recursion est geree grace a la variable context.
    '''
    global best_score, best_partition

    l_possible_rect = compute_l_possible_rect()
    l_partition     = [None] * len(l_possible_rect)
    idx_possible    = 0
    idx_partition   = 0

    # print(l_possible_rect)
    context = []
    while (not((idx_partition == 0) and (idx_possible >= len(l_possible_rect)))):
        while(idx_possible < len(l_possible_rect)):
            cur_rect = l_possible_rect[idx_possible]
            if (does_overlap(l_partition, idx_partition, cur_rect)):
                idx_possible += 1
                continue

            l_partition[idx_partition] = cur_rect
            context.append( (idx_partition, idx_possible) )
            idx_partition += 1
            idx_possible += 1
            if (best_score < score(l_partition[:idx_partition])):
                best_score     = score(l_partition)
                best_partition = l_partition[:idx_partition]
                print_n_write_best()

        # print(context)
        idx_partition, idx_possible = context.pop()
        idx_possible += 1


# backtrack()

def backtrack_big ():
    '''
    Probabiliste.
    '''
    global best_score, best_partition
    from random import Random

    l_partition = [None] * int((C * R)/(2*L))
    l_seed_pt = compute_l_seed_pt()
    shapes = generate_shapes()
    rand = Random()

    while (True):
        # RAZ de la liste des reectangles
        idx_partition = 0
        # Tous les points seed sont a nouveau disponibles
        pt_seed_avail = set(l_seed_pt)

        for pt_seed in l_seed_pt:
            if (pt_seed in pt_seed_avail):
                pt_seed_avail.remove (pt_seed)
            else:
                continue

            # Pour un point seed, on calcule au hazard un rectangle possible qui le contient
            l_possible_rect = get_possible_rect(pt_seed, shapes)
            idx_rect = 0
            if (0 < (len(l_possible_rect) -1)):
                idx_rect = rand.randint(0, len(l_possible_rect) -1)
            else :
                idx_rect = 0
            cur_rect = l_possible_rect[idx_rect]

            max_tentative = int(len(l_possible_rect) * 0.5)
            i_tentative = 0
            while (does_overlap(l_partition, idx_partition, cur_rect) and
                   (i_tentative < max_tentative)):
                if (0 < (len(l_possible_rect) -1)):
                    idx_rect = rand.randint(0, len(l_possible_rect) -1)
                else :
                    idx_rect = 0
                cur_rect = l_possible_rect[idx_rect]
                i_tentative += 1

            # Pas de bon rectangle pour un seed pt, on passe au pt suivant
            if (not (i_tentative < max_tentative)):
                continue

            # Ajout du rectangle à l'ensemble de partitionnemnt
            l_partition[idx_partition] = cur_rect
            idx_partition += 1

            other_pt_seed_avail = set(pt_seed_avail)
            for other_pt_seed in other_pt_seed_avail:
                if cur_rect.contain (other_pt_seed):
                    pt_seed_avail.remove (other_pt_seed)

            if (best_score < score(l_partition[:idx_partition])):
                best_partition = l_partition[:idx_partition]
                best_score     = score (best_partition)
                print_n_write_best()


backtrack_big ()
