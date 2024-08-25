from src import sumar

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
            print("algo") 
        case _:
            print("Operacion invalida ")

           
