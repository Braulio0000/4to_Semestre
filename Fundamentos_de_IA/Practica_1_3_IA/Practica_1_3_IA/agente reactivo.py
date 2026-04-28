import random

LOC_A = "A"
LOC_B = "B"
ESTADO_SUCIO = "Sucio"
ESTADO_LIMPIO = "Limpio"
ACCION_ASPIRAR = "Aspirar"
ACCION_NO_OP = "No hacer nada"

class Entorno:
    def __init__(self):
        self.estados = {
            LOC_A: random.choice([ESTADO_SUCIO, ESTADO_LIMPIO]),
            LOC_B: random.choice([ESTADO_SUCIO, ESTADO_LIMPIO])
        }
    
    def limpiar(self, loc):
        self.estados[loc] = ESTADO_LIMPIO

class AspiradoraReactivaCobarde:
    def __init__(self, entorno):
        self.entorno = entorno
        self.localizacion = LOC_A
        self.rendimiento = 0

    def sensor(self):
        return (self.localizacion, self.entorno.estados[self.localizacion])

    def actuar(self, percepcion):
        loc, estado = percepcion
        
        if estado == ESTADO_SUCIO:
            print(f"Decisión: ¡Hay puntos fáciles! Acción: {ACCION_ASPIRAR}.")
            self.entorno.limpiar(loc)
            self.rendimiento += 10
        
        elif estado == ESTADO_LIMPIO:
            print(f"Decisión: {loc} está limpio. Me quedo quieto para no gastar energía (-1 punto).")

    def ejecutar(self, pasos=8):
        print(f"Agente COBARDE | Estado inicial: {self.entorno.estados}\n--- INICIANDO ---\n")
        for i in range(pasos):
            percepcion = self.sensor()
            print(f"Paso {i+1} | En: '{self.localizacion}' | Ve: '{percepcion[1]}' | Puntos: {self.rendimiento}")
            self.actuar(percepcion)
        print(f"\n--- FINALIZADO ---\nRendimiento Final: {self.rendimiento}")

if __name__ == "__main__":
    entorno_sim = Entorno()
    agente_cobarde = AspiradoraReactivaCobarde(entorno_sim)
    agente_cobarde.ejecutar()