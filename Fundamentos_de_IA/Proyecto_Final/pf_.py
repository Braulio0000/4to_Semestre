import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# =============================================================================
# 1. CONFIGURACIÓN DEL ESCENARIO (LABERINTO)
# =============================================================================
INICIO = np.array([5.0, 5.0])
META = np.array([95.0, 95.0])

# Muros: [x_min, x_max, y_min, y_max]
OBSTACULOS = [
    [20, 40, 0, 60],     # Muro 1 (Vertical abajo)
    [60, 80, 40, 100],   # Muro 2 (Vertical arriba)
    [0, 50, 70, 80]      # Muro 3 (Horizontal)
]

# =============================================================================
# 2. CONFIGURACIÓN DE LOS ALGORITMOS (REQUISITOS PASO 3 Y 4)
# =============================================================================
# Codificación: Vector de coordenadas (x,y) para 5 puntos intermedios.
DIMENSION = 10           # 5 waypoints * 2 coordenadas
POBLACION = 50           # Mismo tamaño para todos (Requisito)
ITERACIONES = 200        # Mismo número de iteraciones (Requisito)
CORRIDAS = 20            # 20 ejecuciones para estadística (Requisito)
LIMITES = (0.0, 100.0)

# =============================================================================
# 3. LÓGICA DEL PROBLEMA (FUNCIÓN OBJETIVO CON OBSTÁCULOS)
# =============================================================================

def check_colision(p1, p2, obst):
    """Detecta si el segmento p1-p2 toca un obstáculo con alta precisión."""
    x1, y1 = p1
    x2, y2 = p2
    xmin, xmax, ymin, ymax = obst
    
    # Filtro rápido (AABB - Axis Aligned Bounding Box)
    if max(x1, x2) < xmin or min(x1, x2) > xmax or max(y1, y2) < ymin or min(y1, y2) > ymax:
        return False
        
    dist = np.hypot(x2 - x1, y2 - y1)
    if dist < 1e-10: 
        return False
    
    # Revisar cada 0.5 unidades para no saltarse muros
    pasos = max(2, int(dist / 0.5) + 1)
    
    for i in range(pasos):
        t = i / max(1, (pasos - 1))  # Evitar división por cero
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        if (xmin - 0.5) <= px <= (xmax + 0.5) and (ymin - 0.5) <= py <= (ymax + 0.5):
            return True
    return False

def decodificar(ind):
    """Decodifica el vector en ruta completa: Inicio -> Puntos -> Meta"""
    waypoints = ind.reshape(-1, 2)
    return np.vstack([INICIO, waypoints, META])

def fitness_maze(ind):
    """
    Función Objetivo: Minimizar distancia.
    Si choca, retorna INFINITO (Muerte súbita para cumplir restricción).
    """
    ruta = decodificar(ind)
    distancia_total = 0.0
    
    for i in range(len(ruta) - 1):
        p1 = ruta[i]
        p2 = ruta[i + 1]
        
        # Verificar colisión con cada obstáculo
        colision = False
        for obst in OBSTACULOS:
            if check_colision(p1, p2, obst):
                return float('inf')  # Penalización máxima
        
        distancia_total += np.hypot(p2[0] - p1[0], p2[1] - p1[1])
        
    return distancia_total

# =============================================================================
# 4. IMPLEMENTACIÓN DE ALGORITMOS (PSO, GA, DE)
# =============================================================================

def pso(func, dim, bounds, iters, pop_size):
    """Optimización por Enjambre de Partículas (Particle Swarm Optimization)"""
    X = np.random.uniform(bounds[0], bounds[1], (pop_size, dim))
    V = np.random.uniform(-5, 5, (pop_size, dim))
    pbest = X.copy()
    
    # Evaluación inicial
    pbest_fit = np.array([func(ind) for ind in X])
    
    min_idx = np.argmin(pbest_fit)
    gbest = pbest[min_idx].copy()
    gbest_fit = pbest_fit[min_idx]
    
    historia = [gbest_fit]
    w = 0.7
    c1 = 1.5
    c2 = 1.5
    
    for _ in range(iters - 1):
        r1 = np.random.rand(pop_size, dim)
        r2 = np.random.rand(pop_size, dim)
        V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest - X)
        V = np.clip(V, -15, 15)  # Control de velocidad
        X = np.clip(X + V, bounds[0], bounds[1])
        
        fit = np.array([func(ind) for ind in X])
        
        mask = fit < pbest_fit
        pbest[mask] = X[mask].copy()
        pbest_fit[mask] = fit[mask]
        
        current_best = np.min(fit)
        if current_best < gbest_fit:
            gbest_fit = current_best
            gbest = X[np.argmin(fit)].copy()
            
        historia.append(gbest_fit)
        
    return gbest, gbest_fit, historia

def ga(func, dim, bounds, iters, pop_size):
    """Algoritmo Genético (Genetic Algorithm)"""
    pop = np.random.uniform(bounds[0], bounds[1], (pop_size, dim))
    fit = np.array([func(ind) for ind in pop])
    
    gbest_idx = np.argmin(fit)
    gbest = pop[gbest_idx].copy()
    gbest_fit = fit[gbest_idx]
    historia = [gbest_fit]
    
    for _ in range(iters - 1):
        # Elitismo (2 mejores)
        idx_sorted = np.argsort(fit)
        hijos = [pop[i].copy() for i in idx_sorted[:2]]
        
        while len(hijos) < pop_size:
            # Selección por torneo binario
            idxs1 = np.random.choice(pop_size, 2, replace=False)
            p1 = pop[idxs1[0]] if fit[idxs1[0]] < fit[idxs1[1]] else pop[idxs1[1]]
            
            idxs2 = np.random.choice(pop_size, 2, replace=False)
            p2 = pop[idxs2[0]] if fit[idxs2[0]] < fit[idxs2[1]] else pop[idxs2[1]]
            
            # Cruce aritmético
            alpha = np.random.rand()
            hijo = alpha * p1 + (1 - alpha) * p2
            
            # Mutación gaussiana
            if np.random.rand() < 0.3:
                hijo += np.random.normal(0, 3, dim)
            
            hijo = np.clip(hijo, bounds[0], bounds[1])
            hijos.append(hijo)
            
        # Nueva población
        pop = np.array(hijos)
        fit = np.array([func(ind) for ind in pop])
        
        # Actualizar mejor global
        current_best = np.min(fit)
        if current_best < gbest_fit:
            gbest_fit = current_best
            gbest = pop[np.argmin(fit)].copy()
        
        historia.append(gbest_fit)
        
    return gbest, gbest_fit, historia

def de(func, dim, bounds, iters, pop_size):
    """Evolución Diferencial (Differential Evolution)"""
    pop = np.random.uniform(bounds[0], bounds[1], (pop_size, dim))
    fit = np.array([func(ind) for ind in pop])
    
    gbest_idx = np.argmin(fit)
    gbest = pop[gbest_idx].copy()
    gbest_fit = fit[gbest_idx]
    historia = [gbest_fit]
    
    F = 0.8
    CR = 0.9
    
    for _ in range(iters - 1):
        nueva_pop = pop.copy()
        nuevas_fit = fit.copy()
        
        for i in range(pop_size):
            # Seleccionar 3 índices diferentes al actual
            candidatos = [j for j in range(pop_size) if j != i]
            a, b, c = pop[np.random.choice(candidatos, 3, replace=False)]
            
            # Mutación: estrategia rand/1
            mutant = a + F * (b - c)
            mutant = np.clip(mutant, bounds[0], bounds[1])
            
            # Cruce binomial
            j_rand = np.random.randint(dim)
            trial = np.where((np.random.rand(dim) < CR) | (np.arange(dim) == j_rand), 
                           mutant, pop[i])
            
            # Evaluación y selección
            f_trial = func(trial)
            if f_trial < fit[i]:
                nueva_pop[i] = trial
                nuevas_fit[i] = f_trial
                
                if f_trial < gbest_fit:
                    gbest_fit = f_trial
                    gbest = trial.copy()
        
        pop = nueva_pop
        fit = nuevas_fit
        historia.append(gbest_fit)
    
    return gbest, gbest_fit, historia

# =============================================================================
# 5. EJECUCIÓN PRINCIPAL, ESTADÍSTICA Y VISUALIZACIÓN
# =============================================================================
if __name__ == "__main__":
    print("="*70)
    print("COMPARATIVA DE ALGORITMOS EN LABERINTO")
    print(f"Conf: {CORRIDAS} corridas | {ITERACIONES} iteraciones | Población {POBLACION}")
    print("="*70)
    
    algoritmos = {"PSO": pso, "GA": ga, "DE": de}
    tabla_datos = []
    mejores_rutas = {}
    curvas_plot = {}
    
    tiempo_total_inicio = time.time()
    
    for nombre, algo in algoritmos.items():
        print(f"\nProcesando {nombre}...")
        tiempo_algo_inicio = time.time()
        
        costos = []
        todas_curvas = []
        mejor_global_sol = None
        mejor_global_costo = float('inf')
        mejor_curva_idx = 0
        
        for i in range(CORRIDAS):
            sol, costo, curva = algo(fitness_maze, DIMENSION, LIMITES, ITERACIONES, POBLACION)
            costos.append(costo)
            todas_curvas.append(curva)
            
            if costo < mejor_global_costo:
                mejor_global_costo = costo
                mejor_global_sol = sol.copy()
                mejor_curva_idx = i
            
            if (i + 1) % 5 == 0:
                print(f"  Completado: {i + 1}/{CORRIDAS} corridas", end="\n" if i + 1 == CORRIDAS else " ")
        
        tiempo_algo = time.time() - tiempo_algo_inicio
        
        # Estadísticas
        validos = [c for c in costos if c != float('inf')]
        if validos:
            promedio = np.mean(validos)
            std_dev = np.std(validos)
            exito = (len(validos) / CORRIDAS) * 100
        else:
            promedio = float('inf')
            std_dev = 0.0
            exito = 0.0
        
        tabla_datos.append((nombre, mejor_global_costo, promedio, std_dev, exito, tiempo_algo))
        mejores_rutas[nombre] = (mejor_global_sol, mejor_global_costo)
        curvas_plot[nombre] = todas_curvas[mejor_curva_idx]
        
        print(f"  Tiempo: {tiempo_algo:.2f}s | Éxito: {exito:.1f}% | Mejor: {mejor_global_costo:.2f}")

    tiempo_total = time.time() - tiempo_total_inicio

    # --- 1. TABLA COMPARATIVA MANUAL (SIN PANDAS) ---
    print("\n" + "="*105)
    print(f"| {'ALGORITMO':<10} | {'MEJOR':<12} | {'PROMEDIO':<12} | {'DESV. STD':<12} | {'ÉXITO %':<10} | {'TIEMPO (s)':<10} |")
    print("-" * 105)
    
    # Ordenar Ranking por Promedio
    tabla_datos.sort(key=lambda x: x[2] if x[2] != float('inf') else float('inf'))
    
    for fila in tabla_datos:
        nom, mej, prom, std, ex, tpo = fila
        mej_str = f"{mej:.2f}" if mej != float('inf') else "FALLÓ"
        prom_str = f"{prom:.2f}" if prom != float('inf') else "FALLÓ"
        print(f"| {nom:<10} | {mej_str:<12} | {prom_str:<12} | {std:<12.2f} | {ex:<10.1f} | {tpo:<10.2f} |")
    print("="*105)

    # --- 2. GRÁFICA DE CONVERGENCIA ---
    plt.figure(figsize=(14, 8))
    
    # Encontrar el máximo valor finito para escalar la gráfica
    max_val = 0
    for nombre, curva in curvas_plot.items():
        curva_finita = [x for x in curva if x != float('inf')]
        if curva_finita:
            max_val = max(max_val, max(curva_finita[:50]))  # Solo primeros 50 valores
    
    for nombre, curva in curvas_plot.items():
        # Limpiar infinitos para la gráfica
        curva_limpia = []
        for x in curva:
            if x == float('inf'):
                curva_limpia.append(max_val * 2)
            else:
                curva_limpia.append(min(x, max_val * 2))
        
        plt.plot(curva_limpia, label=nombre, linewidth=2.5, alpha=0.9)
    
    plt.title("Evolución de la Función Objetivo (Mejor Corrida por Algoritmo)", 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Iteraciones", fontsize=14)
    plt.ylabel("Costo (Distancia)", fontsize=14)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Añadir línea horizontal para el óptimo teórico
    distancia_directa = np.hypot(META[0] - INICIO[0], META[1] - INICIO[1])
    plt.axhline(y=distancia_directa, color='r', linestyle=':', alpha=0.5, 
                label=f'Óptimo teórico: {distancia_directa:.1f}')
    plt.legend(fontsize=12)
    
    plt.yscale('log')
    plt.tight_layout()
    plt.show()

    # --- 3. VISUALIZACIÓN DE RUTAS ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for idx, (nombre, (sol, costo)) in enumerate(mejores_rutas.items()):
        ax = axes[idx]
        
        # Dibujar Muros
        for obs in OBSTACULOS:
            rect = patches.Rectangle((obs[0], obs[2]), 
                                    obs[1] - obs[0], 
                                    obs[3] - obs[2], 
                                    facecolor='#34495e', 
                                    edgecolor='#2c3e50',
                                    alpha=0.8,
                                    linewidth=2,
                                    zorder=1)
            ax.add_patch(rect)
        
        # Dibujar Ruta si es válida
        if sol is not None and costo != float('inf'):
            ruta = decodificar(sol)
            ax.plot(ruta[:, 0], ruta[:, 1], '-o', color='#27ae60', 
                   linewidth=3, markersize=8, label='Ruta', 
                   markerfacecolor='white', markeredgewidth=2, zorder=3)
            
            # Numerar waypoints
            for i, p in enumerate(ruta[1:-1]):
                ax.text(p[0], p[1] + 3, str(i + 1), 
                       fontsize=11, fontweight='bold',
                       ha='center', va='bottom', zorder=4,
                       bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor="#f39c12", 
                                alpha=0.9, edgecolor='black'))
            
            titulo = f"{nombre}\nCosto: {costo:.2f}"
            color_titulo = '#27ae60'
        else:
            titulo = f"{nombre}\nFALLÓ (CHOQUE)"
            color_titulo = '#e74c3c'
            
        # Marcar inicio y meta
        ax.plot(INICIO[0], INICIO[1], 's', markersize=15, label='Inicio', 
               markerfacecolor='#3498db', markeredgecolor='#2980b9', 
               markeredgewidth=2, zorder=4)
        ax.plot(META[0], META[1], '*', markersize=25, label='Meta',
               markerfacecolor='#e74c3c', markeredgecolor='#c0392b', 
               markeredgewidth=2, zorder=4)
        
        # Configurar ejes
        ax.set_xlim(-2, 102)
        ax.set_ylim(-2, 102)
        ax.set_title(titulo, fontsize=14, fontweight='bold', color=color_titulo, pad=15)
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.set_aspect('equal', adjustable='box')
        
        # Solo mostrar leyenda en el primer gráfico
        if idx == 0:
            ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
        
        ax.set_xlabel("Coordenada X", fontsize=11)
        ax.set_ylabel("Coordenada Y", fontsize=11)
        
        # Añadir texto informativo
        info_text = f"Waypoints: {DIMENSION//2}\nPoblación: {POBLACION}"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    plt.suptitle("Mejores Rutas Encontradas por Cada Algoritmo", 
                 fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
    
    # --- 4. GRÁFICA DE ESTADÍSTICAS ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    # 4.1 Tasa de Éxito
    nombres = [d[0] for d in tabla_datos]
    exitos = [d[4] for d in tabla_datos]
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    bars1 = axes[0].bar(nombres, exitos, color=colors, alpha=0.8, edgecolor='black')
    axes[0].set_title('Tasa de Éxito por Algoritmo', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Porcentaje de Éxito (%)', fontsize=12)
    axes[0].set_ylim(0, 110)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    for bar in bars1:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 4.2 Tiempo de Ejecución
    tiempos = [d[5] for d in tabla_datos]
    bars2 = axes[1].bar(nombres, tiempos, color=colors, alpha=0.8, edgecolor='black')
    axes[1].set_title('Tiempo Promedio de Ejecución', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Tiempo (segundos)', fontsize=12)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    for bar in bars2:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.2f}s', ha='center', va='bottom', fontweight='bold')
    
    # 4.3 Mejor Costo Encontrado
    mejores_costos = [d[1] if d[1] != float('inf') else 300 for d in tabla_datos]
    bars3 = axes[2].bar(nombres, mejores_costos, color=colors, alpha=0.8, edgecolor='black')
    axes[2].set_title('Mejor Costo Encontrado', fontsize=14, fontweight='bold')
    axes[2].set_ylabel('Distancia', fontsize=12)
    axes[2].axhline(y=distancia_directa, color='r', linestyle='--', alpha=0.7, 
                   label=f'Óptimo: {distancia_directa:.1f}')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3, axis='y')
    
    for bar, costo in zip(bars3, [d[1] for d in tabla_datos]):
        height = bar.get_height()
        if costo != float('inf'):
            axes[2].text(bar.get_x() + bar.get_width()/2., height + 5,
                        f'{costo:.2f}', ha='center', va='bottom', fontweight='bold')
        else:
            axes[2].text(bar.get_x() + bar.get_width()/2., height + 5,
                        'FALLÓ', ha='center', va='bottom', fontweight='bold', color='red')
    
    # 4.4 Distribución de Costos (boxplot simulado)
    axes[3].axis('off')
    info_text = f"""
    RESUMEN EJECUCIÓN
    
    • Total algoritmos: {len(algoritmos)}
    • Corridas por algoritmo: {CORRIDAS}
    • Iteraciones por corrida: {ITERACIONES}
    • Población: {POBLACION}
    • Dimensión del problema: {DIMENSION}
    • Waypoints intermedios: {DIMENSION//2}
    
    TIEMPO TOTAL: {tiempo_total:.2f} segundos
    
    DISTANCIA ÓPTIMA TEÓRICA: {distancia_directa:.2f}
    (sin obstáculos, línea recta)
    """
    axes[3].text(0.1, 0.5, info_text, fontsize=11, family='monospace',
                bbox=dict(boxstyle="round,pad=1", facecolor="lightyellow", alpha=0.9))
    
    plt.suptitle('Análisis Comparativo de Algoritmos de Optimización', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
    
    # --- 5. RESULTADOS FINALES ---
    print("\n" + "="*80)
    print("RESUMEN EJECUCIÓN COMPLETA")
    print("="*80)
    print(f"Tiempo total: {tiempo_total:.2f} segundos")
    print(f"Total corridas: {CORRIDAS * len(algoritmos)}")
    print(f"Configuración: {POBLACION} individuos × {ITERACIONES} iteraciones")
    print(f"Waypoints intermedios: {DIMENSION//2}")
    print(f"Distancia óptima teórica (sin obstáculos): {distancia_directa:.2f}")
    
    # Identificar el mejor algoritmo global
    mejor_algo = min(tabla_datos, key=lambda x: x[2] if x[2] != float('inf') else float('inf'))
    print(f"\n✓ MEJOR ALGORITMO GLOBAL: {mejor_algo[0]}")
    print(f"  • Mejor costo: {mejor_algo[1]:.2f}")
    print(f"  • Promedio: {mejor_algo[2]:.2f}")
    print(f"  • Tasa de éxito: {mejor_algo[4]:.1f}%")
    print(f"  • Tiempo promedio: {mejor_algo[5]:.2f}s")
    
    print("\n" + "="*80)
    print("FIN DE LA EJECUCIÓN")
    print("="*80)