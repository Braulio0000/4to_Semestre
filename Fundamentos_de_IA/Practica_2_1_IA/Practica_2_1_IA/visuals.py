import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from collections import deque
import random
import time

N = 20

def generar_plano(prob_obstaculo=0.25):
    plano = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            if random.random() < prob_obstaculo:
                plano[i, j] = 1
    return plano

movs = [(-1,0), (1,0), (0,-1), (0,1)]

def es_valido(plano, x, y, visitado):
    return 0 <= x < N and 0 <= y < N and plano[x][y] == 0 and not visitado[x][y]

# BFS con estadísticas
def bfs_pasos(plano, inicio, destino):
    q = deque([[inicio]])
    visitado = np.zeros((N,N), dtype=bool)
    visitado[inicio[0], inicio[1]] = True
    pasos = []
    nodos_visitados = 0
    inicio_tiempo = time.time()

    while q:
        camino = q.popleft()
        x, y = camino[-1]
        nodos_visitados += 1
        pasos.append((list(camino), nodos_visitados))

        if (x, y) == destino:
            tiempo_total = time.time() - inicio_tiempo
            return pasos, nodos_visitados, len(camino), tiempo_total
        for dx, dy in movs:
            nx, ny = x + dx, y + dy
            if es_valido(plano, nx, ny, visitado):
                visitado[nx, ny] = True
                q.append(camino + [(nx, ny)])
    tiempo_total = time.time() - inicio_tiempo
    return pasos, nodos_visitados, 0, tiempo_total

# DFS con estadísticas
def dfs_pasos(plano, inicio, destino, limite=1000):
    stack = [[inicio]]
    visitado = np.zeros((N,N), dtype=bool)
    visitado[inicio[0], inicio[1]] = True
    pasos = []
    nodos_visitados = 0
    inicio_tiempo = time.time()

    while stack:
        camino = stack.pop()
        x, y = camino[-1]
        nodos_visitados += 1
        pasos.append((list(camino), nodos_visitados))

        if (x, y) == destino:
            tiempo_total = time.time() - inicio_tiempo
            return pasos, nodos_visitados, len(camino), tiempo_total
        if len(camino) > limite:
            continue
        for dx, dy in movs:
            nx, ny = x + dx, y + dy
            if es_valido(plano, nx, ny, visitado):
                visitado[nx, ny] = True
                stack.append(camino + [(nx, ny)])
    tiempo_total = time.time() - inicio_tiempo
    return pasos, nodos_visitados, 0, tiempo_total

class VisualizadorAnimado:
    def __init__(self, plano, inicio, destino, bfs_data, dfs_data):
        self.plano = plano
        self.inicio = inicio
        self.destino = destino
        self.pasos_bfs, self.nodos_bfs, self.long_bfs, self.tiempo_bfs = bfs_data
        self.pasos_dfs, self.nodos_dfs, self.long_dfs, self.tiempo_dfs = dfs_data
        self.modo = 0

        plt.rcParams['toolbar'] = 'none'
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        plt.subplots_adjust(bottom=0.25)
        self.ax.axis("off")

        # Botón
        ax_boton = plt.axes([0.35, 0.02, 0.3, 0.08])
        self.boton = Button(ax_boton, "Siguiente versión →")
        self.boton.on_clicked(self.cambiar_version)

        self.animar_camino()

    def dibujar(self, camino, nodos_visitados, titulo):
        self.ax.clear()
        self.ax.imshow(self.plano, cmap="gray_r", origin="upper")
        self.ax.scatter(self.inicio[1], self.inicio[0], c='red', s=120, marker='o', label="Inicio")
        self.ax.scatter(self.destino[1], self.destino[0], c='red', s=150, marker='*', label="Destino")
        if camino:
            x, y = zip(*camino)
            self.ax.plot(y, x, c='lime', linewidth=2)
            self.ax.scatter(y[-1], x[-1], c='blue', s=80)
        self.ax.set_title(titulo)
        self.ax.legend(loc='upper right')

        # Mostrar estadísticas en tiempo real
        path_len = len(camino)
        stats = f"Nodos visitados: {nodos_visitados}\nLongitud del camino actual: {path_len}"
        self.ax.text(0, -2, stats, fontsize=10, va='top', ha='left', transform=self.ax.transAxes)
        self.ax.axis("off")
        self.fig.canvas.draw_idle()

    def mostrar_estadisticas_finales(self):
        if self.modo == 0:
            stats = f"--- Estadísticas finales BFS ---\nTotal nodos visitados: {self.nodos_bfs}\nLongitud del camino final: {self.long_bfs}\nTiempo de ejecución: {self.tiempo_bfs:.4f} s"
        else:
            stats = f"--- Estadísticas finales DFS ---\nTotal nodos visitados: {self.nodos_dfs}\nLongitud del camino final: {self.long_dfs}\nTiempo de ejecución: {self.tiempo_dfs:.4f} s"
        print(stats)
        # Mostrar en la figura
        self.ax.text(0, -0.1, stats, fontsize=10, va='top', ha='left', transform=self.ax.transAxes)

    def animar_camino(self):
        pasos = self.pasos_bfs if self.modo == 0 else self.pasos_dfs
        titulo = "Camino BFS" if self.modo == 0 else "Camino DFS"

        for camino, nodos_visitados in pasos:
            self.dibujar(camino, nodos_visitados, titulo)
            plt.pause(0.05)
        # Al final de la animación, mostrar estadísticas finales
        self.mostrar_estadisticas_finales()

    def cambiar_version(self, event):
        self.modo = 1 - self.modo
        self.animar_camino()

if __name__ == "__main__":
    plano = generar_plano()
    inicio = (0,0)
    destino = (N-1,N-1)
    plano[inicio] = 0
    plano[destino] = 0

    bfs_data = bfs_pasos(plano, inicio, destino)
    dfs_data = dfs_pasos(plano, inicio, destino)

    VisualizadorAnimado(plano, inicio, destino, bfs_data, dfs_data)
plt.show(block=True)