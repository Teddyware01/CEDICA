from src import interfaz

numero1 = float(input("Ingrese un numero:  "))
print("Ingrese una de las siguientes operaciones: ")
operacion = input("|  +  |  -  |  /  |  *  |\nIngresa tu operación: ")
resultado = interfaz.opciones(operacion,numero1)
print(F"El resultado de la operacion es: {resultado}")

