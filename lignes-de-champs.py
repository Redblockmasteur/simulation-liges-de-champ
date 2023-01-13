# Based on the work of  https://scipython.com/blog/visualizing-a-vector-field-with-matplotlib
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Configuration de la simulation :
auto = 0 # Auto : Si == 1 Le code génère un cercle et inverse la charge | nbCharges est utilisé pour définir le nombre de charges a placer sur le cercle
               #           Si == 0 Le code prends en argument la position de chaque | Ex avec 2 charges charges = [(-1, (1.0, 0.0)), (2, (-1.0, 1))]
nbCharges = 5


# Cette fonction revoie le vecteur de la ligne de champ engentré par la particule q en r0
def E(q, r0, x, y):
    den = np.hypot(x-r0[0], y-r0[1])**3
    return q * (x - r0[0]) / den, q * (y - r0[1]) / den



# Grille des points en x et en y. plus nx et ny sont éllevé  plus les postions de départs et l'arivés des lignes de champ est précis 
nx, ny = 64, 64
x = np.linspace(-2, 2, nx)
y = np.linspace(-2, 2, ny)
X, Y = np.meshgrid(x, y)



# Mode Auto crée un cercle avec des particules  
if auto == 1:
    nq = nbCharges  # nombre de charges à utiliser
    charges = []
    for i in range(nq):
        q = i%2 * 2 - 1
        charges.append((q, (np.cos(2*np.pi*i/nq), np.sin(2*np.pi*i/nq))))
elif auto == 0:
    # Défini un tableau avec les positions et le charges des particules au format :
    #  [-1,(1.0, 3.0),(3, -1.0, 2,0)]
    #    ↑    ↑     ↑
    #   Q1  X1  Y1
    # Q1 la charge de la particule 1
    # X1 la position en X de la particule 1
    # Y1 la position en Y de la particule 1

    # Note : Il n'est pas nécessaire de définir nbCharges en mode manuel
    #            Les valeurs en x et en y des particules de doivent pas ètres en dehors du plan défini par set_xlim et set_ylim

    charges = [(-1, (1.0, 0.0)), (2, (-1.0, 1))] 

else :
    print("Erreur la variable Auto prend en arguemnt 1 ou 0 ")




# Calcul du vecteur de la ligne de champ, E=(Ex, Ey), en composantes séparées
Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
for charge in charges:
    ex, ey = E(*charge, x=X, y=Y)
    Ex += ex
    Ey += ey
fig = plt.figure(num='Simulation les lignes de champ')
ax = fig.add_subplot(111)



# Affiche et extrapoles les lignes ainsi qu'applique un gradient aproximatif.
color = 2 * np.log(np.hypot(Ex, Ey))
ax.streamplot(x, y, Ex, Ey, color=color, linewidth=1, cmap=plt.cm.inferno,
              density=2, arrowstyle='->', arrowsize=1.5)



# Définie la couleur de la particule chargée (Rouge + et Bleu -)
charge_colors = {True: '#aa0000', False: '#0000aa'}
for q, pos in charges:
    ax.add_artist(Circle(pos, 0.05, color=charge_colors[q>0]))


ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(-2,2) # Limite du plan en X
ax.set_ylim(-2,2) # Limite du plan en y
ax.set_aspect('equal')

# Affiche le résultat de la simulation
plt.show()


print(charges)