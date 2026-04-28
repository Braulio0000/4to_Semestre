import random

# -------------------------
# Clase Entorno
# -------------------------
class Entorno:
    def __init__(self):
        # Dos posiciones: A y B
        self.estados = {"A": random.choice(["Sucio", "Limpio"]),
                        "B": random.choice(["Sucio", "Limpio"])}
    
    def esta_sucio(self, loc):
        return self.estados[loc] == "Sucio"
    
    def limpiar(self, loc):
        self.estados[loc] = "Limpio"


# -------------------------
# Clase Agente Aspiradora
# -------------------------
class Aspiradora:
    def __init__(self, entorno):
        self.entorno = entorno
        self.localizacion = "A"  # inicia en A
        self.rendimiento = 0
    
    def sensor(self):
        """Detecta el estado actual (ubicación y suciedad)."""
        estado = self.entorno.estados[self.localizacion]
        return (self.localizacion, estado)
    
    def actuar(self, percepcion):
        """Decide qué acción tomar según la función agente (Fig.2)."""
        loc, estado = percepcion

        if estado == "Sucio":
            self.entorno.limpiar(loc)
            print(f"En {loc}: Aspirar")
            self.rendimiento += 1  # limpiar da puntos
        elif loc == "A" and estado == "Limpio":
            print("Mover a la derecha")
            self.localizacion = "B"
        elif loc == "B" and estado == "Limpio":
            print("Mover a la izquierda")
            self.localizacion = "A"
    
    def ejecutar(self, pasos=10):
        """Corre la simulación cierto número de pasos."""
        for i in range(pasos):
            percepcion = self.sensor()
            print(f"Paso {i+1} | Percepción: {percepcion}")
            self.actuar(percepcion)
            print(f"Estado del entorno: {self.entorno.estados}\n")
        print(f"Medida de rendimiento final: {self.rendimiento}")


# -------------------------
# Simulación
# -------------------------
if __name__ == "__main__":
    entorno = Entorno()
    aspiradora = Aspiradora(entorno)
    print(f"Estado inicial del entorno: {entorno.estados}\n")
    aspiradora.ejecutar(pasos=10)
