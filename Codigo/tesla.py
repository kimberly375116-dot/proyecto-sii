
import random

class Carretera:
    # Ubicacion de la simulacion
    UBICACION = "Cocula, Jalisco"
    ESCENARIO = "Zona urbana de Cocula"

    DISTANCIA_SEGURA = 20
    DISTANCIA_PELIGRO = 8

    def __init__(self, pasos=60, semilla=7):
        self.azar = random.Random(semilla)
        self.pasos = pasos
        self.reiniciar()

    def reiniciar(self):
        self.t = 0
        self.distancia = 30.0
        self.velocidad = 50.0
        self.obstaculo = False
        self.carril_visible = True
        self.frenados = 0
        self.colisiones = 0
        self.penalizacion = 0.0
        return self.percepcion()

    def percepcion(self):
        # Camaras del vehiculo en las calles de Cocula
        return {
            "t": self.t,
            "distancia": round(
                max(0, self.distancia + self.azar.uniform(-3, 3)), 1
            ),
            "obstaculo": self.obstaculo,
            "carril_visible": self.carril_visible
        }

    def paso(self, frenar):
        # Simular situaciones de transito en Cocula
        self.obstaculo = self.azar.random() < 0.10
        self.carril_visible = self.azar.random() > 0.10

        if frenar:
            self.velocidad = max(0, self.velocidad - 10)
            self.frenados += 1
        else:
            self.velocidad = min(80, self.velocidad + 2)

        # Cambios en la distancia del vehiculo
        if frenar:
            self.distancia += 5
        else:
            self.distancia -= self.velocidad * 0.08

        self.distancia = max(0, min(50, self.distancia))

        # Penalizar situaciones peligrosas
        if self.distancia < self.DISTANCIA_PELIGRO:
            self.penalizacion += 10

        if self.obstaculo and not frenar:
            self.colisiones += 1
            self.penalizacion += 50

        self.t += 1

        return self.percepcion(), self.t >= self.pasos

    def desempeno(self):
        return self.penalizacion + self.frenados


class AgenteReactivo:
    # Decide utilizando solamente la informacion actual

    def actuar(self, percepcion):
        if percepcion["distancia"] < 15:
            return True

        if percepcion["obstaculo"]:
            return True

        return False


class AgenteConModelo:
    # Recuerda informacion de pasos anteriores

    def __init__(self):
        self.distancia_anterior = None
        self.frenar_antes = False

    def actuar(self, percepcion):
        distancia = percepcion["distancia"]
        obstaculo = percepcion["obstaculo"]
        carril_visible = percepcion["carril_visible"]

        se_acerca = False

        if self.distancia_anterior is not None:
            se_acerca = distancia < self.distancia_anterior

        self.distancia_anterior = distancia

        if obstaculo:
            self.frenar_antes = True
            return True

        if distancia < 20 and se_acerca:
            self.frenar_antes = True
            return True

        if distancia < 10:
            self.frenar_antes = True
            return True

        if not carril_visible:
            self.frenar_antes = True
            return True

        self.frenar_antes = False
        return False


def correr(agente_clase, semilla, pasos=60):
    carretera = Carretera(pasos=pasos, semilla=semilla)
    percepcion = carretera.reiniciar()
    agente = agente_clase()
    fin = False

    while not fin:
        frenar = agente.actuar(percepcion)
        percepcion, fin = carretera.paso(frenar)

    return (
        carretera.desempeno(),
        carretera.colisiones,
        carretera.frenados
    )


def comparar(pasos=60, repeticiones=20):
    print("=" * 60)
    print(" SISTEMA INTELIGENTE DE CONDUCCION TESLA")
    print(" UBICACION: COCULA, JALISCO")
    print(" ESCENARIO: ZONA URBANA")
    print("=" * 60)
    print()

    print(f"{'Agente':18s} {'Puntuacion':>12s} "
          f"{'Colisiones':>12s} {'Frenados':>10s}")
    print("-" * 56)

    agentes = [
        ("Reactivo", AgenteReactivo),
        ("Con modelo", AgenteConModelo)
    ]

    for nombre, agente_clase in agentes:
        resultados = [
            correr(agente_clase, semilla, pasos)
            for semilla in range(repeticiones)
        ]

        puntuacion = sum(r[0] for r in resultados) / len(resultados)
        colisiones = sum(r[1] for r in resultados) / len(resultados)
        frenados = sum(r[2] for r in resultados) / len(resultados)

        print(f"{nombre:18s} {puntuacion:12.1f} "
              f"{colisiones:12.2f} {frenados:10.2f}")

    print()
    print("Simulacion finalizada en Cocula, Jalisco.")


if __name__ == "__main__":
    comparar(pasos=60, repeticiones=20)
