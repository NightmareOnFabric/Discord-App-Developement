import string

def detectar_mensaje():
    keyboard_characters = input("Introduce una oración: ")  # Pedimos la oración al usuario
    caracteres_globales = string.ascii_letters + string.digits + string.punctuation + ' '  # Todo el alfabeto, dígitos, puntuación y espacio

    # Verificar si la oración contiene alguno de los caracteres del teclado
    if any(letra in keyboard_characters for letra in caracteres_globales):
        print("Se ha detectado un mensaje:")
        print(keyboard_characters)
    else:
        print("No se ha detectado ningún mensaje con los caracteres del teclado.")

    input("\nPresiona Enter para salir...")  # Pausa para evitar que se cierre la ventana

detectar_mensaje()
