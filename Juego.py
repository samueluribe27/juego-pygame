import pygame, sys
import random
from pygame.locals import *

pygame.init()

# Configuración de la pantalla del juego
PANTALLA = pygame.display.set_mode((800, 600))  # Crea una ventana de 800x600 píxeles.
pygame.display.set_caption('Juego esquivar enemigos')  # Establece el título de la ventana.

# Definición de colores en formato RGB
BLANCO = (255, 255, 255)  # Color blanco.
NEGRO = (0, 0, 0)  # Color negro.
ROJO = (255, 0, 0)  # Color rojo.
AZUL = (0, 0, 255)  # Color azul.

# Configuración de la velocidad de actualización de la pantalla
FPS = 60  # Frames por segundo.
fpsClock = pygame.time.Clock()  # Controlador para limitar la velocidad del juego.

# Dimensiones del jugador y los enemigos
jugador_ancho, jugador_alto = 50, 50  # Tamaño del jugador.
enemigo_ancho, enemigo_alto = 50, 50  # Tamaño de los enemigos.
enemigos_max = 5  # Cantidad máxima de enemigos en pantalla.

# Velocidades y otras configuraciones
jugador_vel = 5  # Velocidad de movimiento del jugador.
enemigo_vel = 2  # Velocidad de movimiento de los enemigos.

# Fuente para mostrar los puntajes
fuente = pygame.font.Font(None, 74)  # Crea una fuente con un tamaño de 74 puntos.


def dibujar_boton(superficie, color, rect, texto=''):
    """Dibuja un botón en la superficie especificada."""
    pygame.draw.rect(superficie, color, rect)  # Dibuja un rectángulo con el color y las dimensiones especificadas.
    if texto:
        texto_superficie = fuente.render(texto, True, BLANCO)  # Renderiza el texto del botón.
        texto_rect = texto_superficie.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))  # Posiciona el texto en el centro del botón.
        superficie.blit(texto_superficie, texto_rect)  # Dibuja el texto en la superficie.

def mostrar_menu():
    """Muestra el menú principal y devuelve el nivel seleccionado."""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  # Cierra Pygame.
                sys.exit()  # Termina el programa.
            if event.type == MOUSEBUTTONDOWN:
                mouse_position = event.pos  # Obtiene la posición del clic del ratón.
                # Define las áreas de los botones
                button_level1 = pygame.Rect(300, 150, 200, 50)  # Área del botón Nivel 1.
                button_level2 = pygame.Rect(300, 250, 200, 50)  # Área del botón Nivel 2.
                button_level3 = pygame.Rect(300, 350, 200, 50)  # Área del botón Nivel 3.

                # Verifica si se hizo clic en uno de los botones
                if button_level1.collidepoint(mouse_position):
                    return 1  # Regresa el nivel de dificultad 1
                elif button_level2.collidepoint(mouse_position):
                    return 2  # Regresa el nivel de dificultad 2
                elif button_level3.collidepoint(mouse_position):
                    return 3  # Regresa el nivel de dificultad 3

        # Dibujar el menú
        PANTALLA.fill(NEGRO)  # Llena la pantalla de color negro.
        dibujar_boton(PANTALLA, AZUL, (300, 150, 200, 50), 'Nivel 1')  # Dibuja el botón del Nivel 1.
        dibujar_boton(PANTALLA, AZUL, (300, 250, 200, 50), 'Nivel 2')  # Dibuja el botón del Nivel 2.
        dibujar_boton(PANTALLA, AZUL, (300, 350, 200, 50), 'Nivel 3')  # Dibuja el botón del Nivel 3.
        pygame.display.update()  # Actualiza la pantalla para mostrar los cambios.
        fpsClock.tick(FPS)  # Controla la velocidad de actualización de la pantalla.

def generar_enemigos(nivel):
    """Genera enemigos en la pantalla según el nivel."""
    enemigos = []
    for _ in range(enemigos_max + nivel):  # Incrementa la cantidad de enemigos según el nivel.
        x = random.randint(0, PANTALLA.get_width() - enemigo_ancho)  # Posición X aleatoria.
        y = random.randint(0, PANTALLA.get_height() - enemigo_alto)  # Posición Y aleatoria.
        enemigos.append(pygame.Rect(x, y, enemigo_ancho, enemigo_alto))  # Crea un enemigo y lo añade a la lista.
    return enemigos

def juego(nivel):
    """Gestiona la lógica del juego, incluyendo movimiento del jugador y enemigos, y colisiones."""
    global enemigo_vel
    enemigos = generar_enemigos(nivel)  # Genera enemigos según el nivel.
    jugador = pygame.Rect(375, 525, jugador_ancho, jugador_alto)  # Crea el rectángulo del jugador.
    puntuacion = 0  # Inicializa la puntuación.

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  # Cierra Pygame.
                sys.exit()  # Termina el programa.

        # Movimiento del jugador
        keys = pygame.key.get_pressed()  # Obtiene el estado actual de todas las teclas.
        if keys[K_LEFT] and jugador.left > 0:
            jugador.left -= jugador_vel  # Mueve el jugador a la izquierda.
        if keys[K_RIGHT] and jugador.right < PANTALLA.get_width():
            jugador.right += jugador_vel  # Mueve el jugador a la derecha.
        if keys[K_UP] and jugador.top > 0:
            jugador.top -= jugador_vel  # Mueve el jugador hacia arriba.
        if keys[K_DOWN] and jugador.bottom < PANTALLA.get_height():
            jugador.bottom += jugador_vel  # Mueve el jugador hacia abajo.

        # Movimiento de los enemigos
        for enemigo in enemigos:
            enemigo.y += enemigo_vel  # Mueve el enemigo hacia abajo.
            if enemigo.y > PANTALLA.get_height():  # Si el enemigo sale de la pantalla por abajo...
                enemigo.x = random.randint(0, PANTALLA.get_width() - enemigo_ancho)  # Coloca el enemigo en una nueva posición X.
                enemigo.y = random.randint(-100, -50)  # Coloca el enemigo en una nueva posición Y arriba de la pantalla.
                puntuacion += 1  # Incrementa la puntuación por evitar enemigos.

        # Comprobar colisiones
        for enemigo in enemigos:
            if jugador.colliderect(enemigo):  # Si el jugador colide con un enemigo...
                return puntuacion  # Termina el juego y devuelve la puntuación.

        # Dibujar los elementos en la pantalla
        PANTALLA.fill(NEGRO)  # Llena la pantalla de color negro.
        pygame.draw.rect(PANTALLA, AZUL, jugador)  # Dibuja el jugador en la pantalla.
        for enemigo in enemigos:
            pygame.draw.rect(PANTALLA, ROJO, enemigo)  # Dibuja cada enemigo en la pantalla.

        # Mostrar la puntuación en la pantalla
        texto_puntuacion = fuente.render(f'Puntos: {puntuacion}', True, BLANCO)  # Renderiza la puntuación.
        PANTALLA.blit(texto_puntuacion, (10, 10))  # Dibuja la puntuación en la pantalla.

        pygame.display.update()  # Actualiza la pantalla para mostrar los cambios.
        fpsClock.tick(FPS)  # Controla la velocidad de actualización de la pantalla.

def main():
    """Función principal para ejecutar el menú y el juego."""
    while True:
        nivel = mostrar_menu()  # Muestra el menú y obtiene el nivel seleccionado.
        if nivel is None:
            continue  # Vuelve a mostrar el menú si no se selecciona ningún nivel.

        global enemigo_vel
        enemigo_vel = 2 + nivel  # Configura la velocidad de los enemigos basada en el nivel.
        puntuacion = juego(nivel)  # Inicia el juego con el nivel seleccionado y obtiene la puntuación final.

        # Mostrar la puntuación final y esperar a que el usuario cierre el juego o vuelva al menú.
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_position = event.pos
                    button_menu = pygame.Rect(300, 250, 200, 50)  # Área del botón Volver al Menú.
                    if button_menu.collidepoint(mouse_position):
                        print(main()) # Salir del bucle para volver al menú.

            # Dibujar la pantalla de puntuación final
            PANTALLA.fill(NEGRO)
            texto_puntuacion = fuente.render(f'Puntos: {puntuacion}', True, BLANCO)
            PANTALLA.blit(texto_puntuacion, (300, 150))

            # Dibujar el botón para volver al menú
            dibujar_boton(PANTALLA, AZUL, (300, 250, 200, 50), 'Volver')
            pygame.display.update()
            fpsClock.tick(FPS)

juego = main()
print(juego)