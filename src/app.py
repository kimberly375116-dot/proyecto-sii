def percibe_funcion(imagenes):
resultado = "Imagen recibida: " + imagenes
return resultado

def decide_funcion(reducir_velocidad):
if reducir_velocidad:
resultado = "Se debe reducir la velocidad"
else:
resultado = "No se debe reducir la velocidad"

return resultado

def acciona_funcion(modificar_velocidad):
resultado = "Velocidad modificada a: " + str(modificar_velocidad)
return resultado

def main():
resultado1 = percibe_funcion("Obstáculo detectado")
print(resultado1)

resultado2 = decide_funcion(True)
print(resultado2)

resultado3 = acciona_funcion(30)
print(resultado3)

if **name** == "**main**":
main()
