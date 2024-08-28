from src import sumar, multiplicar

def opciones(op, num1):
    match op:
        case '+':
            numero2 = float(input("Ingrese otro numero:  "))
            return sumar.sumar(num1,numero2)
        case '-':
            numero2 = float(input("Ingrese otro numero:  "))
            print("algo")
        case '/':
            numero2 = float(input("Ingrese otro numero:  "))
            print("algo")
        case '*':
            numero2 = float(input("Ingrese otro numero:  "))
            return multiplicar.multiplicar(num1,numero2)
        case _:
            print("Operacion invalida ")

           
