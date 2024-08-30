def dividir (num1, num2):
    try:
        return num1 / num2
    except ZeroDivisionError:
        return "Error: No se puede dividir por cero"