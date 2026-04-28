# --- Configuración de recompensas y costos ---
COSTO_POR_ACCION = -1        # penalización por cada acción (mover o aspirar)
RECOMPENSA_LIMPIAR = 10      # recompensa por limpiar con éxito una casilla sucia
RECOMPENSA_POR_TODO_LIMPIO = 0  # opcional, por cada paso con todo limpio

from dataclasses import dataclass
from typing import Tuple, Dict
import csv
import pathlib

# --- Entorno de la aspiradora ---
@dataclass
class EntornoAspiradora:
    suciedad: Dict[str, bool]     # True si está sucio
    ubicacion_agente: str         # 'A' o 'B'
    pasos: int = 0
    pasos_maximos: int = 100

    def sensor(self) -> Tuple[str, bool]:
        """Devuelve la ubicación y si está sucia (lo que 've' el agente)."""
        return self.ubicacion_agente, self.suciedad[self.ubicacion_agente]

    def actuar(self, accion: str) -> int:
        """Ejecuta la acción y devuelve el cambio de puntaje inmediato."""
        self.pasos += 1
        recompensa = 0
        if accion == 'ASPIRAR':
            recompensa += COSTO_POR_ACCION
            if self.suciedad[self.ubicacion_agente]:
                self.suciedad[self.ubicacion_agente] = False
                recompensa += RECOMPENSA_LIMPIAR
        elif accion == 'IZQUIERDA':
            recompensa += COSTO_POR_ACCION
            self.ubicacion_agente = 'A'
        elif accion == 'DERECHA':
            recompensa += COSTO_POR_ACCION
            self.ubicacion_agente = 'B'
        elif accion == 'NO_HACER_NADA':
            pass
        else:
            raise ValueError("Acción desconocida: "+str(accion))
        if all(not d for d in self.suciedad.values()):
            recompensa += RECOMPENSA_POR_TODO_LIMPIO
        return recompensa

# --- Agente reactivo simple ---
class AgenteReactivoSimple:
    def __init__(self):
        self.puntaje = 0

    def programa(self, percepcion: Tuple[str, bool]) -> str:
        """Decide qué hacer según la percepción actual."""
        ubic, esta_sucia = percepcion
        if esta_sucia:
            return 'ASPIRAR'
        if ubic == 'A':
            return 'DERECHA'
        else:
            return 'IZQUIERDA'

# --- Función para mostrar el estado visualmente ---
def mostrar_estado(entorno: EntornoAspiradora):
    estado_A = "*" if entorno.suciedad['A'] else " "
    estado_B = "*" if entorno.suciedad['B'] else " "
    if entorno.ubicacion_agente == 'A':
        print(f"[AX{estado_A}] [B {estado_B}]")
    else:
        print(f"[A {estado_A}] [BX{estado_B}]")

# --- Función para correr un episodio ---
def correr_episodio(entorno: EntornoAspiradora, agente: AgenteReactivoSimple,
                    pasos_maximos: int=100, permitir_chequeo_global: bool=False) -> int:
    total = 0
    for paso in range(1, pasos_maximos+1):
        percepcion = entorno.sensor()
        if permitir_chequeo_global and all(not d for d in entorno.suciedad.values()):
            accion = 'NO_HACER_NADA'
        else:
            accion = agente.programa(percepcion)
            if permitir_chequeo_global and accion in ('IZQUIERDA','DERECHA'):
                if all(not d for d in entorno.suciedad.values()):
                    accion = 'NO_HACER_NADA'

        # --- Mostrar estado paso a paso ---
        print(f"Paso {paso}: Acción={accion}")
        mostrar_estado(entorno)

        recompensa = entorno.actuar(accion)
        total += recompensa
        if all(not d for d in entorno.suciedad.values()) and accion == 'NO_HACER_NADA':
            break
    agente.puntaje += total
    return total

# --- Función para correr muchas configuraciones ---
def correr_todas(runs_por_config:int=5, pasos_maximos:int=10,
                 permitir_chequeo_global: bool=True, archivo_csv: str = "resultados_aspiradora.csv"):
    configuraciones = []
    for ubicacion_inicial in ['A','B']:
        for sucA in [True, False]:
            for sucB in [True, False]:
                configuraciones.append({
                    'ubicacion_inicial': ubicacion_inicial,
                    'suciedad': {'A': sucA, 'B': sucB}
                })

    resultados = []
    for cfg in configuraciones:
        puntajes_cfg = []
        for _ in range(runs_por_config):
            entorno = EntornoAspiradora(suciedad=cfg['suciedad'].copy(),
                                        ubicacion_agente=cfg['ubicacion_inicial'],
                                        pasos_maximos=pasos_maximos)
            agente = AgenteReactivoSimple()
            puntaje = correr_episodio(entorno, agente, pasos_maximos=pasos_maximos,
                                      permitir_chequeo_global=permitir_chequeo_global)
            puntajes_cfg.append(puntaje)
        promedio = sum(puntajes_cfg)/len(puntajes_cfg)
        resultados.append({
            'ubicacion_inicial': cfg['ubicacion_inicial'],
            'sucA': cfg['suciedad']['A'],
            'sucB': cfg['suciedad']['B'],
            'runs': runs_por_config,
            'puntajes': puntajes_cfg,
            'promedio': promedio
        })

    promedio_global = sum(r['promedio'] for r in resultados)/len(resultados)
    campos = ['ubicacion_inicial','sucA','sucB','iteracion','puntaje']
    pathlib.Path(archivo_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(archivo_csv, 'w', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for r in resultados:
            for i,s in enumerate(r['puntajes']):
                escritor.writerow({
                    'ubicacion_inicial': r['ubicacion_inicial'],
                    'sucA': r['sucA'],
                    'sucB': r['sucB'],
                    'iteracion': i+1,
                    'puntaje': s
                })
    return resultados, promedio_global, archivo_csv

# --- Ejecución principal ---
if __name__ == "__main__":
    resultados, promedio_global, archivo = correr_todas()
    print("\nResultados por configuración:")
    for r in resultados:
        print(f"Inicia en {r['ubicacion_inicial']}, sucA={r['sucA']}, sucB={r['sucB']} -> promedio={r['promedio']:.2f} en {r['runs']} ejecuciones")
    print(f"\nPromedio global: {promedio_global:.2f}")
    print(f"Resultados guardados en: {archivo}")