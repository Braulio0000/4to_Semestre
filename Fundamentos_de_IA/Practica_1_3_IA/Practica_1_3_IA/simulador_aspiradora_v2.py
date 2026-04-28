import random

LOC_A = "A"
LOC_B = "B"
ESTADO_SUCIO = "Sucio"
ESTADO_LIMPIO = "Limpio"
ACCION_ASPIRAR = "Aspirar"
ACCION_MOVER_DERECHA = "Mover a la derecha (A -> B)"
ACCION_MOVER_IZQUIERDA = "Mover a la izquierda (B -> A)"
ACCION_NO_OP = "No hacer nada (todo limpio)"

class Entorno:
    def __init__(self):
        self.estados = {
            LOC_A: random.choice([ESTADO_SUCIO, ESTADO_LIMPIO]),
            LOC_B: random.choice([ESTADO_SUCIO, ESTADO_LIMPIO])
        }
    def limpiar(self, loc):
        self.estados[loc] = ESTADO_LIMPIO

class Aspiradora:
    def __init__(self, entorno):
        self.entorno = entorno
        self.localizacion = LOC_A  
        self.rendimiento = 0
        self.modelo = {LOC_A: None, LOC_B: None}
    
    def sensor(self):
        loc_actual = self.localizacion
        estado_loc_actual = self.entorno.estados[loc_actual]
        
        self.modelo[loc_actual] = estado_loc_actual
        
        return (loc_actual, estado_loc_actual)
    
    def actuar(self, percepcion):
        loc, estado = percepcion
        if estado == ESTADO_SUCIO:
            accion = ACCION_ASPIRAR
            self.entorno.limpiar(loc)
            self.rendimiento += 10
            print(f"Decisión: {loc} está sucio. Acción: {accion}. (+10 puntos)")
            return

        otra_loc = LOC_B if loc == LOC_A else LOC_A
        
        if self.modelo[otra_loc] != ESTADO_LIMPIO:
            accion = ACCION_MOVER_DERECHA if loc == LOC_A else ACCION_MOVER_IZQUIERDA
            self.localizacion = otra_loc
            self.rendimiento -= 1
            print(f"Decisión: {loc} está limpio, pero el modelo indica que {otra_loc} no está limpio. Acción: {accion}. (-1 punto)")
      
        else:
            accion = ACCION_NO_OP
            print(f"Decisión: El modelo confirma que todo está limpio. Acción: {accion}. (0 puntos)")

    def ejecutar(self, pasos=10):
        print(f"Estado inicial del entorno: {self.entorno.estados}")
        print(f"Modelo inicial del agente: {self.modelo}\n")
        print("--- INICIANDO SIMULACIÓN ---")
        
        for i in range(pasos):
            print(f"--- Paso {i+1} ---")
            percepcion = self.sensor()
            print(f"Percepción: El agente está en '{percepcion[0]}' y está '{percepcion[1]}'.")
            print(f"Modelo interno actualizado: {self.modelo}")
            print(f"Rendimiento actual: {self.rendimiento}")
            self.actuar(percepcion)
            print(f"Nuevo estado del entorno: {self.entorno.estados}\n")

        print("--- SIMULACIÓN FINALIZADA ---")
        print(f"Rendimiento final: {self.rendimiento}")

if __name__ == "__main__":
    entorno_simulacion = Entorno()
    agente_inteligente = Aspiradora(entorno_simulacion)
    agente_inteligente.ejecutar(pasos=8)