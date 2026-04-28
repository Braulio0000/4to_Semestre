import random
from collections import deque

# Estado objetivo
objetivo = [1,2,3,4,5,6,7,8,0]

# Generar un estado inicial aleatorio
def generar_estado_inicial():
    estado = objetivo[:]
    random.shuffle(estado)
    return estado

# Obtener los movimientos posibles
def sucesores(estado):
    sucesores = []
    i = estado.index(0)  # posición del hueco
    filas, cols = divmod(i, 3)

    movimientos = {
        "arriba": (filas > 0, -3),
        "abajo": (filas < 2, 3),
        "izquierda": (cols > 0, -1),
        "derecha": (cols < 2, 1),
    }

    for valido, delta in movimientos.values():
        if valido:
            nuevo = estado[:]
            j = i + delta
            nuevo[i], nuevo[j] = nuevo[j], nuevo[i]
            sucesores.append(nuevo)
    return sucesores

# Búsqueda en amplitud (BFS)
def bfs(inicial):
    frontera = deque([[inicial]])
    visitados = set()
    while frontera:
        camino = frontera.popleft()
        estado = camino[-1]
        if estado == objetivo:
            return camino
        visitados.add(tuple(estado))
        for s in sucesores(estado):
            if tuple(s) not in visitados:
                frontera.append(camino + [s])
    return None

# Búsqueda en profundidad (DFS)
def dfs(inicial, limite=50):
    frontera = [[inicial]]
    visitados = set()
    while frontera:
        camino = frontera.pop()
        estado = camino[-1]
        if estado == objetivo:
            return camino
        if len(camino) > limite:
            continue
        visitados.add(tuple(estado))
        for s in sucesores(estado):
            if tuple(s) not in visitados:
                frontera.append(camino + [s])
    return None

# Ejemplo
inicial = generar_estado_inicial()
print("Estado inicial:", inicial)

solucion_bfs = bfs(inicial)
print("\nSolución BFS (pasos):", len(solucion_bfs)-1 if solucion_bfs else "No encontrada")

solucion_dfs = dfs(inicial)
print("\nSolución DFS (pasos):", len(solucion_dfs)-1 if solucion_dfs else "No encontrada")
