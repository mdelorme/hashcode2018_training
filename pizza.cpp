#include <bits/stdc++.h>

int R, C, L, H;
int **pizza;

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
}


void greedy() {
  std::vector<Rect> partition;
  bool used[R][C];
  memset(used, 0, R*C*sizeof(bool));

  int score = 0;

  // On check chaque case
  for (int y=0; y < R; ++y) {
    for (int x=0; x < C; ++x) {
      // Si deja utilisee on saute
      if (used[y][x])
	continue;

      // On essaie de prendre une forme qui tienne
      for (auto s : shapes) {
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

	// On marque toutes les cases utilisees par la procedure
	for (int nx=x; nx < x+s.x1; ++nx)
	  for (int ny=y; ny < y+s.y1; ++ny)
	    used[ny][nx] = true;

	// Et on ajoute la partition au groupe final
	partition.push_back(Rect{x, y, x+s.x1-1, y+s.y1-1});
	score += Mc+Tc;
      }
    }
  }
  
  std::cerr << "Final score : " << score << std::endl;
  std::cout << partition.size() << std::endl;
  for (auto r : partition) {
    std::cout << r.y0 << " " << r.x0 << " " << r.y1 << " " << r.x1
	      << std::endl;
  }
}

int main() {
  // Init
  std::cin >> R >> C >> L >> H;
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
  
  return 0;
}


