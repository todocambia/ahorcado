from constants import menu_options, vidas_inicio, ahorcado
from random_word import RandomWords
import json
import os

class Palabra:

    def __init__(self, palabra = "moreta en bicicleta"):
        self.palabra = palabra

class GuardarJuego:

    def __init__(self, file_path="Historial_de_juegos.json"):
        self.file_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump({"juegos": []}, file)
      
    def guardar_resultados(self, game_mode, resultado, palabra):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        data["juegos"].append({
            "game_mode": game_mode,
            "result": resultado,
            "word": palabra
        })
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
    
    def mostrar_historial(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        indice = 0
        historial = "\nHistorial de Juegos:\n\n"
        for juego in data["juegos"]:    
            indice += 1
            historial += f"{indice} Modo de Juego: {juego['game_mode']}, Resultado: {juego['result']}, Palabra: {juego['word']}\n\n"
        with open(self.file_path, "r") as file:
            json.dump(data, file, indent=4)
        print (historial)
        return input("Presione cualquier letra para continuar volver al menu...")

class Jugando:

    def __init__(self):
        self.palabra = Palabra().palabra
        self.vidas = vidas_inicio
        self.guardado = GuardarJuego()
        self.game_mode = None

    def options(self):  
        text = """
            El ahorcado
            --------------------------------
            """
        for i, o in enumerate(menu_options):
            i += 1
            text += """
            {0} - {1}
            """.format(i, o)
        text +="\n---------------------\n"
        return text 
    
    def menu(self):
        try:
            eleccion = int(input(self.options()))
            if eleccion < 1 or eleccion > len(menu_options):
                print("\nOpción inválida. Por favor elija nuevamente.\n")
                return self.menu()
            return eleccion
        except ValueError:
            print("\nPor favor solo ingrese números.\n")
            return self.menu()

    def palabra_cifrada(self):
        n = len(self.palabra)
        p_c = ["_" if letra != " " else " " for letra in self.palabra]
        while self.vidas > 0:
            print(ahorcado[7 - self.vidas])
            print(" ".join (p_c))           
            jugada = input("\n").lower()
            if len(jugada) != 1 or not jugada.isalpha():
                    print ("\nSolo ingrese letras y solo una a la vez.\n")
                    continue
            if jugada in self.palabra:
                    for i in range(n):
                         if self.palabra[i] == jugada:
                              p_c[i] = jugada
            else:   
                self.vidas -= 1
                print("\nLetra no encontrada. Intente de nuevo.\n")
            if "_" not in p_c:
                self.guardado.guardar_resultados(self.game_mode, "Victoria", self.palabra)
                print(f"\nGanaste! La palabra cifarada era: {self.palabra}")
                break
        if self.vidas == 0:
            self.guardado.guardar_resultados(self.game_mode, "Derrota", self.palabra)
            print(ahorcado[-1])
            print(f"Haz perdido! La palabra era: {self.palabra}")

def init_game():
    juego = Jugando()   
    while True:
        eleccion = juego.menu()
        if eleccion == 4:
            print("\nGracias por jugar! Saliendo del juego...\n")
            break
        elif eleccion == 1:
            r = RandomWords()
            palabra_random = r.get_random_word()
            juego.palabra = palabra_random
            juego.game_mode = "1 Jugador"
            juego.palabra_cifrada()
        elif eleccion == 2:
            dos_jugadores = input("Ingrese la palabra deseada: ")
            juego.palabra = dos_jugadores
            juego.game_mode = "2 Jugadores"
            juego.palabra_cifrada()
        elif eleccion == 3:
            print(juego.guardado.mostrar_historial())
