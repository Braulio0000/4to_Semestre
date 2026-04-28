import itertools

# -------------------------
# Clase Entorno
# -------------------------
class Entorno:
    def __init__(self, estadoA="Sucio", estadoB="Sucio"):
        # Estado inicial de las dos posiciones
        self.estados = {"A": estadoA, "B": estadoB}
    
    def esta_sucio(self, loc):
        return self.estados[loc] == "Sucio"
    
    def limpiar(self, loc):
        self.estados[loc] = "Limpio"


# -------------------------
# Clase Agente Reactivo Simple
# -------------------------
class Aspiradora:
    def __init__(self, entorno, posicion="A"):
        self.entorno = entorno
        self.localizacion = posicion
        self.rendimiento = 0
    
    def sensor(self):
        """Detecta el estado actual (ubicación y suciedad)."""
        estado = self.entorno.estados[self.localizacion]
        return (self.localizacion, estado)
    
    def actuar(self, percepcion):
        """Agente reactivo simple: acción depende solo de la percepción actual."""
        loc, estado = percepcion

        if estado == "Sucio":
            self.entorno.limpiar(loc)
            self.rendimiento += 1
        elif loc == "A" and estado == "Limpio":
            self.localizacion = "B"
        elif loc == "B" and estado == "Limpio":
            self.localizacion = "A"
    
    def ejecutar(self, pasos=10):
        """Corre la simulación cierto número de pasos."""
        for _ in range(pasos):
            percepcion = self.sensor()
            self.actuar(percepcion)
        return self.rendimiento


# -------------------------
# Simulador de todas las configuraciones
# -------------------------
def simular_todas_configuraciones(pasos=10):
    posiciones = ["A", "B"]
    estados = ["Sucio", "Limpio"]

    configuraciones = list(itertools.product(posiciones, estados, estados))
    resultados = []

    for config in configuraciones:
        pos_ini, estadoA, estadoB = config
        entorno = Entorno(estadoA, estadoB)
        aspiradora = Aspiradora(entorno, pos_ini)

        puntaje = aspiradora.ejecutar(pasos=pasos)
        resultados.append(puntaje)

        print(f"Config: Aspiradora en {pos_ini}, A={estadoA}, B={estadoB} → "
              f"Rendimiento={puntaje}")

    media = sum(resultados) / len(resultados)
    print("\n--- RESULTADOS ---")
    print(f"Puntuaciones por configuración: {resultados}")
    print(f"Media global del rendimiento: {media:.2f}")


# -------------------------
# Ejecución
# -------------------------
if __name__ == "__main__":
    simular_todas_configuraciones(pasos=10)
