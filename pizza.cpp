#include <bits/stdc++.h>

int R, C, L, H;
int **pizza;

std::istream *input;

struct Point {
  int x, y;
};

struct Rect {
  int x0, y0, x1, y1;

  int area() {
    return (x1 - x0 + 1) * (y1 - y0 + 1);
  };

  void contents(int &M, int &T) {
    M = 0;
    T = 0;

    for (int i=x0; i <= x1; ++i) {
      for (int j=y0; j <= y1; ++j) {
	if (pizza[j][i] == 0)
	  M++;
	else
	  T++;
      }
    }
  };
};

// La liste de toutes les formes de rectangles possibles dans ce jeu
// de test
std::vector<Rect> shapes;

void compute_shapes(std::vector<Rect> &out) {
  out.clear();
  for (int j=H; j >= 2*L-1; --j)
    for (int i=1; i <= j+1; ++i)
      if (j%i == 0)
	out.push_back(Rect{0, 0, i, j/i});

  /*
    Tri -> Ne marche pas super.
    Trier par ordre croissant de taille tend a sous exploiter la grille

  auto lambda = [&] (const Rect &a, const Rect &b) {
		  return (a.x1-a.x0)*(a.y1-a.y0) > (b.x1-b.x0)*(b.y1-b.y0);
		};

  std::sort(out.begin(), out.end(), lambda);
  */
}


void greedy() {
  std::vector<Rect> partition;
  int **partition_index;
  bool used[R][C];
  memset(used, 0, R*C*sizeof(bool));

  partition_index = new int*[R];
  for (int r=0; r < R; ++r)
    partition_index[r] = new int[C];

  int score    = 0;
  int cur_part = 0;
  
  // On check chaque case
  for (int y=0; y < R; ++y) {
    for (int x=0; x < C; ++x) {
      // Si deja utilisee on saute
      if (used[y][x])
	continue;

      // On essaie de prendre une forme qui tienne
      int best_shape = -1;
      float best_score = -1;
      float cur_score = -1;
      for (int i=0; i < shapes.size(); ++i) {
	auto &s = shapes[i];
	bool is_valid = true;
	int Mc = 0;
	int Tc = 0;

	// On regarde si la forme est valide
	for (int nx=x; nx < x+s.x1; ++nx) {
	  // Si on sort de la pizza : invalide
	  if (nx >= C) {
	    is_valid = false;
	    break;
	  }
	  
	  for (int ny=y; ny < y+s.y1; ++ny) {
	    // Si on sort de la pizza : invalide
	    if (ny >= R) {
	      is_valid = false;
	      break;
	    }

	    // Si la case est deja utilisee : invalide
	    if (used[ny][nx]) {
	      is_valid = false;
	      break;
	    }

	    // Comptage des elements
	    if (pizza[ny][nx])
	      Mc++;
	    else
	      Tc++;
	  }

	  // On sort si c'est invalide
	  if (!is_valid)
	    break;
	}

	// On passe a la forme suivante si jamais le decoupage est invalide 
	if (!is_valid || Mc < L || Tc < L || Mc+Tc > H)
	  continue;

	// On calcule le score courant : taille totale - difference entre Mc et Tcc
	cur_score = Mc+Tc - abs(Mc-Tc);
	if (cur_score > best_score) {
	  best_shape = i;
	  best_score = cur_score;
	}
      }

      // On marque toutes les cases utilisees par la procedure
      if (best_shape < 0)
	continue;
      
      auto s = shapes[best_shape];
      for (int nx=x; nx < x+s.x1; ++nx) {
	for (int ny=y; ny < y+s.y1; ++ny) {
	  used[ny][nx] = true;
	  partition_index[ny][nx] = cur_part;
	}
      }
      
      // Et on ajoute la partition au groupe final
      Rect r {x, y, x+s.x1-1, y+s.y1-1};
      partition.push_back(r);
      score += r.area();
      cur_part++;
    }
  }

  // Greedy score + partition
  std::cerr << "Final score : " << score << std::endl;
  std::cout << partition.size() << std::endl;
  for (auto r : partition) {
    std::cout << r.y0 << " " << r.x0 << " " << r.y1 << " " << r.x1
	      << std::endl;
  }

  // Diagnostics :
  constexpr bool print_distrib = false;
  constexpr bool print_seeds = false;

  // Partition distribution
  if (print_distrib) {
    std::cerr << "Partition distribution : " << std::endl;
    for (int y=0; y < R; ++y) {
      for (int x=0; x < C; ++x) {
	std::cerr << (used[y][x] ? partition_index[y][x] : -1) << "\t";
      }
      std::cerr << std::endl;
    }
  }

  // Building seed list
  std::vector<Point> seeds;
  for (int y=0; y < R; ++y) {
    for (int x=0; x < C; ++x) {
      if (!used[y][x])
	seeds.push_back(Point{x, y});
    }
  }

  // Seeds
  if (print_seeds) {
    std::cerr << "Unassigned positions : " << std::endl;
    for (auto p : seeds)
      std::cerr << p.x << " " << p.y << std::endl;
  }
  
  // Liberation de la memoire
  for (int r=0; r < R; ++r)
    delete partition_index[r];
  delete [] partition_index;
    
}

int main(int argc, char **argv) {
  std::ifstream input_file;
  // Si on a un argument passe sur la ligne de commande, on
  // assigne le buffer de cin sur ce fichier
  if (argc > 1) {
    input_file.open(argv[1]);
    std::cin.rdbuf(input_file.rdbuf());
  }
  
  // Init
  std::cin >> R >> C >> L >> H;
  std::cerr << R << " "<< C << " " << L << " " << H << std::endl;
  pizza = new int*[R];
  for (int r=0; r < R; ++r) {
    pizza[r] = new int[C];
    std::string s;
    std::cin >> s;
    for (int c=0; c < C; ++c)
      pizza[r][c] = (s[c] == 'M' ? 0 : 1);
  }

  // On calcule une fois pour toutes, toutes les shapes
  compute_shapes(shapes);
  greedy();

  for (int r=0; r < R; ++r)
    delete pizza[r];
  delete [] pizza;

  if (argc > 1)
    input_file.close();
  
  return 0;
}


