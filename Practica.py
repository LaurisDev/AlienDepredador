import random
import math


class Node:
    __slots__ = 'value', 'next'

    def __init__(self, value):
        self.value = value
        self.next = None


class Tablero:
    def __init__(self, n, dificultad):
        self.n = n
        self.head = None
        self.dificultad = dificultad

    def iterar(self):
        curr_node = self.head
        while curr_node is not None:
            yield curr_node
            curr_node = curr_node.next

    def crear_tablero(self):
        while self.dificultad not in ["fácil", "intermedio", "difícil"]:
            self.dificultad = input("Ingresa el nivel de dificultad (fácil, intermedio, difícil): ")

        curr_node = None
        for i in range(self.n):
            for j in range(self.n):
                if self.dificultad == "fácil":
                    value = random.choices(["'+'", "'-'", "' '"], weights=[10, 20, 70])[0]
                elif self.dificultad == "intermedio":
                    value = random.choices(["'+'", "'-'", "' '"], weights=[20, 10, 50])[0]
                elif self.dificultad == "difícil":
                    value = random.choices(["'+'", "'-'", "' '"], weights=[30, 40, 30])[0]
                else:
                    print("Nivel de dificultad no válido")

                if curr_node is None:
                    curr_node = Node(value)
                    self.head = curr_node
                else:
                    new_node = Node(value)
                    curr_node.next = new_node
                    curr_node = new_node

    def imprimir(self):
        curr_node = self.head
        for i in range(self.n):
            print("[", end="")
            for j in range(self.n):
                print(curr_node.value, end=", " if j < self.n - 1 else " ")
                curr_node = curr_node.next
            print("]")

class Juego:
    def __init__(self, tablero):
        self.tablero = tablero
        self.puntaje_alien = 50
        self.puntaje_depredador = 50
        self.alien = None
        self.depredador = None

    def colocar_depredador(self):
      if self.depredador is None:
          curr_node = self.tablero.head
          index = 0
          while curr_node:
              if curr_node.value == "' '":
                  curr_node.value = "'🤖'"
                  self.depredador = (index // self.tablero.n, index % self.tablero.n)
                  break
              curr_node = curr_node.next
              index += 1

          if self.depredador is None:
              print("No hay espacio disponible para colocar al depredador.")


    def colocar_alien(self):
        fila = int(input("Ingrese la fila en donde desea comenzar: "))
        columna = int(input("Ingrese la columna en donde desea comenzar: "))

        while fila < 0 or fila >= self.tablero.n or columna < 0 or columna >= self.tablero.n:
          print("Fuera de rango.Intentelo de nuevo")
          self.colocar_alien()

        curr_node = self.tablero.head
        for _ in range(fila * self.tablero.n + columna):
          curr_node = curr_node.next
        curr_node.value = "'👽'"
        self.alien = (fila, columna)

    def obtenerPosicion(self, personaje):
        if personaje == "alien":
            return self.alien
        elif personaje == "depredador":
            return self.depredador

    def eliminar_posicion_alien(self):
      for node in self.tablero.iterar():
          if node.value == "'👽'":
              node.value = "' '"
              break

    def alien_depredador_casilla(self):
      if self.distancia_alien_depredador() == 0:
        for node in self.tablero.iterar():
          if node.value == "'🤖'" or node.value =="'👽'":
              node.value = "'👽🤖'"
      elif self.alien_depredador_casilla !=0:
        for node in self.tablero.iterar():
          if node.value =="'👽🤖'":
            node.value = "' '"



    def eliminar_posicion_depredador(self):
       for node in self.tablero.iterar():
          if node.value == "'🤖'":
              node.value = "' '"
              break

    def distancia_alien_depredador(self):
      filaA, columnaA = self.obtenerPosicion("alien")
      filaD, columnaD = self.obtenerPosicion("depredador")
      distancia = math.sqrt((filaD-filaA)**2 + (columnaD-columnaA)**2)
      return distancia

    def turno_alien(self):
      if self.distancia_alien_depredador()==1:
        atacar = input("¿Deseas ATACAR al Depredador 🤖? (Si/No): ")
        if atacar.lower() == "si":
          print("¡El alien ataca al depredador!")
          self.puntaje_depredador -= 10
      else:
        movimiento_alien = input("Ingrese cómo desea moverse (arriba, abajo, derecha o izquierda): ")
        fila, columna = self.obtenerPosicion("alien")

        if movimiento_alien == "arriba":
          fila_nueva = fila - 1
          columna_nueva = columna
        elif movimiento_alien == "abajo":
            fila_nueva = fila + 1
            columna_nueva = columna
        elif movimiento_alien == "derecha":
          fila_nueva = fila
          columna_nueva = columna + 1
        elif movimiento_alien == "izquierda":
          fila_nueva = fila
          columna_nueva = columna - 1
        else:
          print("Movimiento invalido")
          self.turno_alien()
          return


        if fila_nueva < 0 or fila_nueva >= self.tablero.n or columna_nueva < 0 or columna_nueva >= self.tablero.n:
          print("Fuera de rango.Intentelo de nuevo")
          self.turno_alien()
          return

        curr_node = self.tablero.head
        for _ in range(fila_nueva * self.tablero.n + columna_nueva):
          curr_node = curr_node.next
        caracter_alien = curr_node.value

        if caracter_alien == "'+'":
          self.puntaje_alien += 10
        elif caracter_alien == "'-'":
          self.puntaje_alien -= 10
        elif caracter_alien == "'🤖'":
          self.puntaje_depredador -= 25
        elif caracter_alien == "' '":
          self.puntaje_alien = self.puntaje_alien

        else:
          print("Coodernada invalida")


        curr_node.value = "'👽'"
        self.alien = (fila_nueva, columna_nueva)
        self.alien_depredador_casilla()

    def mover_depredador(self):
      movimientos = ["arriba", "abajo", "izquierda", "derecha"]
      movimiento_depredador = random.choice(movimientos)
      fila, columna = self.obtenerPosicion("depredador")

      if movimiento_depredador == "arriba":
          fila_nueva = fila - 1
          columna_nueva = columna
      elif movimiento_depredador == "abajo":
          fila_nueva = fila + 1
          columna_nueva = columna
      elif movimiento_depredador == "derecha":
          fila_nueva = fila
          columna_nueva = columna + 1
      elif movimiento_depredador == "izquierda":
          fila_nueva = fila
          columna_nueva = columna - 1

      if 0 <= fila_nueva < self.tablero.n and 0 <= columna_nueva < self.tablero.n:
          curr_node = self.tablero.head
          for _ in range(fila_nueva * self.tablero.n + columna_nueva):
              curr_node = curr_node.next
          caracter_depredador = curr_node.value

          if caracter_depredador == "'+'":
              self.puntaje_depredador += 10
          elif caracter_depredador == "'-'":
              self.puntaje_depredador -= 10
          elif caracter_depredador == "'👽'":
              self.puntaje_alien -= 25
              self.eliminar_posicion_alien()
          elif caracter_depredador == "' '":
              self.puntaje_depredador = self.puntaje_depredador

          curr_node.value = "'🤖'"
          self.depredador = (fila_nueva, columna_nueva)
          self.alien_depredador_casilla()
      else:
        self.mover_depredador()
        return

    def verificar_fin_juego(self):
      if self.puntaje_alien <= 0:
          print("¡El depredador ha ganado!")
          return True
      elif self.puntaje_depredador <= 0:
          print("¡El alien ha ganado!")
          return True
      return False


n = int(input("Ingrese el tamaño de la matriz (nxn): "))
dificultad = input("Ingrese el nivel de dificultad (fácil, intermedio, difícil): ")

tablero = Tablero(n, dificultad)
tablero.crear_tablero()
tablero.imprimir()

juego = Juego(tablero)
juego.colocar_depredador()
juego.colocar_alien()
tablero.imprimir()


while not juego.verificar_fin_juego():
    print("Turno del depredador")
    juego.eliminar_posicion_depredador()
    juego.mover_depredador()
    print("Alien:", juego.puntaje_alien, "- Depredador:", juego.puntaje_depredador)
    tablero.imprimir()
    if juego.verificar_fin_juego():
        break

    print("Turno del jugador")
    juego.eliminar_posicion_alien()
    juego.turno_alien()
    print("Alien:", juego.puntaje_alien, "- Depredador:", juego.puntaje_depredador)
    tablero.imprimir()
    if juego.verificar_fin_juego():
        break



