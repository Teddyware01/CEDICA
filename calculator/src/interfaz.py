from src import sumar

def opciones(op):
    match op:
        case '+':
            return sumar.sumar
        case '-':
            print("algo")
        case '/':
            print("algo")
        case '*':
            print("algo") 
        case _:
            print("Operacion invalida ")

           
