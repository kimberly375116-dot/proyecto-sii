import json

def corte_trapezoidal(a, b, c, d, alfa):
    izquierda = a + alfa * (b - a)
    derecha = d - alfa * (d - c)
    return izquierda, derecha

def corte_triangular(a, b, c, alfa):
    izquierda = a + alfa * (b - a)
    derecha = c - alfa * (c - b)
    return izquierda, derecha

def calcular_cortes(datos):
    conjuntos = datos["conjuntos_difusos"]
    niveles = datos["alfa_cortes"]

    print("\nCALCULO DE CORTES ALFA")
    print("=" * 65)

    print(f"{'Alfa':<10}{'Bajo':<20}{'Medio':<20}{'Alto':<20}")
    print("-" * 65)

    for alfa in niveles:
        resultados = []

        for nombre in ["bajo", "medio", "alto"]:
            conjunto = conjuntos[nombre]
            parametros = conjunto["parametros"]

            if conjunto["tipo"] == "trapezoidal":
                izquierda, derecha = corte_trapezoidal(
                    *parametros, alfa
                )

            elif conjunto["tipo"] == "triangular":
                izquierda, derecha = corte_triangular(
                    *parametros, alfa
                )

            resultados.append(
                f"[{izquierda:.2f}, {derecha:.2f}]"
            )

        print(
            f"{alfa:<10.1f}"
            f"{resultados[0]:<20}"
            f"{resultados[1]:<20}"
            f"{resultados[2]:<20}"
        )


def main():
    with open("datos_tesla.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print("=" * 65)
    print("SISTEMA INTELIGENTE DE CONDUCCION TESLA")
    print("UBICACION:", datos["ubicacion"])
    print("=" * 65)

    print("\nVARIABLE:", datos["variable"])
    print("UNIDAD:", datos["unidad"])
    print("UNIVERSO:", datos["universo"])

    print("\nCONJUNTOS DIFUSOS")

    for nombre, conjunto in datos["conjuntos_difusos"].items():
        print("\nConjunto:", nombre.upper())
        print("Funcion:", conjunto["tipo"])
        print("Parametros:", conjunto["parametros"])

    calcular_cortes(datos)

    print("\nSIMULACION DE CORTES ALFA FINALIZADA")


if __name__ == "__main__":
    main()
