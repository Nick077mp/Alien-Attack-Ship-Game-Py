import pygame  # Librería para videojuegos y aplicaciones multimedia con Python.
import random  # Librería para generar números aleatorios.
import math    # Librería para operaciones matemáticas.
from pygame import mixer  # Librería para música.
 
class Juego:
    """Inicializamos el constructor de la clase. El constructor contiene las características de la clase."""
    def __init__(self):
        pygame.init()
        self.pantalla, self.fondo_imagen = self.configurar_pantalla()  # Creamos la instancia de pantalla con dos valores.
        self.img_jugador, self.posicion_eje_x_jugador, self.posicion_eje_y_jugador = self.configurar_jugador()
        self.img_enemigo, self.posicion_eje_x_enemigo, self.posicion_eje_y_enemigo = self.configurar_enemigo()
        self.musica_archivo = self.configuracion_musica()
        self.fuente_letra, self.posicion_letra_eje_x, self.posicion_letra_eje_y = self.configuracion_fuente_letra_puntaje()
        self.fuente_letra_final, self.posicion_letra_x_enemigo, self.posicion_letra_y_enemigo = self.configuracion_texto_final()
        self.balas = []  # Lista de balas
        self.ciclo = True
        self.puntaje = 0  # Iniciar el puntaje en 0
        self.cambio_x_jugador = 0
 
    def configurar_pantalla(self):
        """Configura y devuelve la pantalla y el fondo del juego."""
        pantalla = pygame.display.set_mode((800, 600))  # Con set_mode asignamos el ancho y alto de la pantalla.
        pygame.display.set_icon(pygame.image.load('C:\\game_aline_invasion\\assets\\images\\ovni.png')) # Utilizamos load para cargar la imagen.
        pygame.display.set_caption('Invasión Nexunity')  # Asignamos el nombre de la ventana en el lado izquierdo.
        fondo_imagen = pygame.image.load('C:\\game_aline_invasion\\assets\\images\\fondo.png')
        return pantalla, fondo_imagen
 
    def configurar_jugador(self):
        """Carga y devuelve la imagen y la posición inicial del jugador."""
        img_jugador = pygame.image.load('C:\\game_aline_invasion\\assets\\images\\astronave.png')
        posicion_x = 368  # Centrar en pantalla | Fórmula: 800 / 2 - (64 / 2) | Ancho Pantalla(800), Tamaño Imagen(64)
        posicion_y = 536  # Posición en el borde inferior | Fórmula: 600 - 64 | Alto Pantalla(600), Tamaño Imagen(64)
        return img_jugador, posicion_x, posicion_y
 
    def configurar_enemigo(self):
        """Carga y devuelve la imagen y la posición inicial de los enemigos.
           Utilizamos listas para así generar múltiples objetos."""
        cantidad_enemigos = 8
        img_enemigo = []  # Dentro de cada lista se guardarán los respectivos elementos.
        posicion_eje_x_enemigo = []
        posicion_eje_y_enemigo = []
        self.cambio_x_enemigo = []
        self.cambio_y_enemigo = []
 
        for enemigo in range(cantidad_enemigos):  # Este bucle agrega a las listas vacías la información requerida en una iteración de 8. (0-7)
            img_enemigo.append(pygame.image.load('C:\\game_aline_invasion\\assets\\images\\nave-espacial-enemigo.png'))
            posicion_eje_x_enemigo.append(random.randint(0, 736))
            posicion_eje_y_enemigo.append(random.randint(50, 200))
            self.cambio_x_enemigo.append(4)
            self.cambio_y_enemigo.append(80)
 
        return img_enemigo, posicion_eje_x_enemigo, posicion_eje_y_enemigo
 
    def configurar_bala(self, x, y):
        """Configura la bala y la añade a la lista de balas."""
        img_bala = pygame.image.load('C:\\game_aline_invasion\\assets\\images\\bala.png')
        nueva_bala = {  # Creamos una bala por cada evento ejecutado.
            "img": img_bala,
            "x": x,
            "y": y,
            "velocidad": 8
        }
        return nueva_bala
 
    def calcular_colisiones(self, x_1, y_1, x_2, y_2):
        """Calcula la distancia entre dos puntos y verifica si hay colisión."""
        distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))  # Utilizamos esta operación matemática para calcular la distancia.
        if distancia < 27:
            return True
        else:
            return False
 
    def configuracion_musica(self):
        musica_fondo_archivo = 'C:\\game_aline_invasion\\assets\\audio\\musica_fondo.mp3'
        mixer.music.load(musica_fondo_archivo)  # Cargamos el archivo de la música con load.
        mixer.music.play(-1)  # Reproduce en bucle (-1).
        mixer.music.set_volume(1)  # Configura el volumen.
 
    def configuracion_fuente_letra_puntaje(self):
        fuente_letra = pygame.font.Font('freesansbold.ttf', 32)  # Utilizamos font.Font para determinar la fuente y asignamos su tamaño.
        posicion_letra_x = 10  # Posicionamos la palabra en el eje x.
        posicion_letra_y = 10  # Posicionamos la palabra en el eje y.
        return fuente_letra, posicion_letra_x, posicion_letra_y
 
    def configuracion_texto_final(self):
        fuente_letra_final = pygame.font.Font('freesansbold.ttf', 50)
        # Centrado del texto
        posicion_letra_x_enemigo = (800 - fuente_letra_final.size("Juego Terminado")[0]) // 2  # size devuelve una tupla con dos valores: Ancho y Alto del texto ya renderizado con la fuente.
        posicion_letra_y_enemigo = 200
        return fuente_letra_final, posicion_letra_x_enemigo, posicion_letra_y_enemigo
 
    def gestionar_eventos(self):
        """Gestiona los eventos de teclado para mover el jugador y disparar."""
        for evento in pygame.event.get():  # Recuerda que en pygame todo son eventos que se van ejecutando en el hardware y los identificamos para interactuar.
            if evento.type == pygame.QUIT:  # X de salida.
                self.ciclo = False
 
            # Cada vez que presionamos una tecla, asignamos el valor a restar o sumar en los píxeles y en las funciones actualizar hacemos una operación para actualizar la posición.
            elif evento.type == pygame.KEYDOWN:  # Tecla Presionada
                if evento.key == pygame.K_LEFT:  # Tecla izquierda
                    self.cambio_x_jugador = -6
                elif evento.key == pygame.K_RIGHT:  # Tecla Derecha
                    self.cambio_x_jugador = 6
                elif evento.key == pygame.K_SPACE:  # Espacio
                    # Cuando se presiona espacio, dispara una nueva bala
                    nueva_bala = self.configurar_bala(self.posicion_eje_x_jugador, self.posicion_eje_y_jugador)
                    self.balas.append(nueva_bala)
                    sonido_bala = mixer.Sound('C:\\game_aline_invasion\\assets\\audio\\balazo-real.mp3')
                    sonido_bala.play()
 
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.cambio_x_jugador = 0
 
    def actualizar_jugador(self):
        """Actualiza la posición del jugador y mantiene límites de pantalla."""
        self.posicion_eje_x_jugador += self.cambio_x_jugador
        self.posicion_eje_x_jugador = max(0, min(736, self.posicion_eje_x_jugador))  # Límite: 800 - 64 (ancho jugador).
 
    def actualizar_enemigos(self):
        """Actualiza la posición de cada enemigo y los hace rebotar en los bordes."""
        for i in range(len(self.img_enemigo)):
            # Movimiento horizontal de enemigos
            self.posicion_eje_x_enemigo[i] += self.cambio_x_enemigo[i]
            # Cambiar dirección al llegar a los bordes
            if self.posicion_eje_x_enemigo[i] <= 0 or self.posicion_eje_x_enemigo[i] >= 736:
                self.cambio_x_enemigo[i] *= -1  # Cambia la dirección.
                self.posicion_eje_y_enemigo[i] += self.cambio_y_enemigo[i]  # Baja al siguiente nivel.
 
    def actualizar_balas(self):
        """Actualiza la posición de las balas y elimina las que salen de la pantalla."""
        for bala in self.balas[:]:  # [:] bucle itera sobre una versión estática de la lista mientras puedes modificar la lista original de manera segura durante la iteración.
            bala['y'] -= bala['velocidad']  # Mueve la bala hacia arriba.
            if bala['y'] < 0:  # Si la bala sale de la pantalla, la eliminamos.
                self.balas.remove(bala)

               
    def actualizar_colisiones(self):
        """Verifica las colisiones entre las balas y los enemigos."""
        for i, bala in enumerate(self.balas[:]):  # Iteramos sobre las balas
            for e in range(len(self.img_enemigo)):  # Iteramos sobre los enemigos
                # Calculamos la colisión entre la bala y el enemigo
                colision = self.calcular_colisiones(self.posicion_eje_x_enemigo[e], self.posicion_eje_y_enemigo[e], bala['x'], bala['y'])
                if colision:
                    # Sonido de eliminación
                    sonido_enemigo_eliminado = mixer.Sound('C:\\game_aline_invasion\\assets\\audio\\enemigo_desaparecido.mp3')
                    sonido_enemigo_eliminado.play()
                   
                    # Eliminar la bala
                    self.balas.remove(bala)
                   
                    # Reiniciar la posición del enemigo
                    self.posicion_eje_x_enemigo[e] = random.randint(0, 736)
                    self.posicion_eje_y_enemigo[e] = random.randint(50, 200)
                   
                    # Aumentar el puntaje
                    self.puntaje += 1
                    print(f"Puntaje: {self.puntaje}")
                   
    def mostrar_puntaje(self):
        texto_puntaje = self.fuente_letra.render(f'Puntaje: {self.puntaje}', True, (255,255,255)) # renderizamos la fuente. elemento, bool, color.
        self.pantalla.blit(texto_puntaje, (self.posicion_letra_eje_x, self.posicion_letra_eje_y))
     
    def mostrar_texto_final(self):
        texto_final = self.fuente_letra_final.render(f'Juego Terminado', True, (255,255,255))
        self.pantalla.blit(texto_final, (self.posicion_letra_x_enemigo, self.posicion_letra_y_enemigo))
     
    def fin_del_juego(self):
        for e in range(8):
            # Fin del Juego
            if self.posicion_eje_y_enemigo[e] > 480:
                sonido_perdio = mixer.Sound('C:\\game_aline_invasion\\assets\\audio\\perdio.mp3')
                sonido_perdio.play()
                for k in range(8):
                    self.posicion_eje_y_enemigo[k] = 10000 # Si la condición se cumple, la posición de los enemigos en el eje y cambia a 10000 para ubicarlos fuera de la pantalla.
                return True
        return False
                           
 
    def dibujar_elementos(self):
        """Dibuja los elementos en la pantalla."""
        self.pantalla.blit(self.fondo_imagen, (0, 0))
        self.pantalla.blit(self.img_jugador, (self.posicion_eje_x_jugador, self.posicion_eje_y_jugador))
        # Dibujar Enemigos
        for i in range(len(self.img_enemigo)):
            self.pantalla.blit(self.img_enemigo[i], (self.posicion_eje_x_enemigo[i], self.posicion_eje_y_enemigo[i]))
       
        # Dibujar todas las balas
        for bala in self.balas:
            self.pantalla.blit(bala['img'], (bala['x'] + 16, bala['y'] + 10)) # Medida para ubicar la bala lo más excata posible a la ubicación del jugador.
       
        # Dibujar Puntos
        self.mostrar_puntaje()
       
        # Dibujar Fin del
        if self.fin_del_juego():
            self.mostrar_texto_final()
             
        pygame.display.update() # Es necesario actualizar cada iteración, para evitar errores en la ejecución.      
       
    def ejecutar(self):
        """Ejecuta el ciclo principal del juego."""
        self.configuracion_musica()
        while self.ciclo:
            self.gestionar_eventos()
            self.actualizar_jugador()
            self.actualizar_enemigos()
            self.actualizar_balas()  # Actualiza las balas
            self.actualizar_colisiones()  # Verifica colisiones
            self.dibujar_elementos()
            self.fin_del_juego()
        pygame.quit() # Confirmar finalización del juego.
 
# Iniciar el juego
if __name__ == "__main__": # Recuerda se tiene que ejecutar el archivi princpal, para ejecutar el codigo.
    juego = Juego()
    juego.ejecutar()
 
   