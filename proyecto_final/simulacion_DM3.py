#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import numpy as np
from threading import Thread

class Disco:
    def __init__(self, x, y, vx, vy, r, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color

    def mover(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def chocar_pared(self, L):
        margen = 0.001  # Un pequeño margen para evitar colisiones instantáneas
        if self.x - self.r < margen or self.x + self.r > L - margen:
            self.vx = -self.vx
            self.x = np.clip(self.x, self.r, L - self.r)  # Evitar que el disco se salga de la caja
        if self.y - self.r < margen or self.y + self.r > L - margen:
            self.vy = -self.vy
            self.y = np.clip(self.y, self.r, L - self.r)  # Evitar que el disco se salga de la caja

    def detectar_colision(self, otro):
        dx = self.x - otro.x
        dy = self.y - otro.y
        distancia = np.sqrt(dx**2 + dy**2)
        return distancia < (self.r + otro.r) 

    def resolver_colision(self, otro):
        dx = self.x - otro.x
        dy = self.y - otro.y
        distancia = np.sqrt(dx**2 + dy**2)

        if distancia < (self.r + otro.r):
           # Vector unitario de colisión
            nx = dx / distancia
            ny = dy / distancia

            # Velocidades relativas
            dvx = self.vx - otro.vx
            dvy = self.vy - otro.vy

            # Momento transferido en la dirección normal
            p = 2 * (dvx * nx + dvy * ny) / 2  # Ambas masas son iguales a 1

            # Actualizar velocidades
            self.vx -= p * nx
            self.vy -= p * ny
            otro.vx += p * nx
            otro.vy += p * ny

           # Separar discos ligeramente para evitar colisiones múltiples
            overlap = (self.r + otro.r) - distancia
            separation = overlap / 2
            self.x += nx * separation
            self.y += ny * separation
            otro.x -= nx * separation
            otro.y -= ny * separation
class Simulacion:
    def __init__(self, L, N, r_min=0.05, r_max=0.1):
        self.L = L
        self.discos = []
        self.colores = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow", "brown", "pink"]

        for _ in range(N):
            while True:
                x = np.random.uniform(r_min, L - r_min)
                y = np.random.uniform(r_min, L - r_min)
                vx = np.random.uniform(-2.5, 2.5)
                vy = np.random.uniform(-2.5, 2.5)
                r = np.random.uniform(r_min, r_max)
                color = random.choice(self.colores)

                nuevo_disco = Disco(x, y, vx, vy, r, color)
                if all(not nuevo_disco.detectar_colision(d) for d in self.discos):
                    self.discos.append(nuevo_disco)
                    break

    def avanzar(self, dt):
        for disco in self.discos:
            disco.mover(dt)
            disco.chocar_pared(self.L)

        num_hilos = 8
        tamano_bloque = len(self.discos) // num_hilos
        hilos = []

        for i in range(num_hilos):
            inicio = i * tamano_bloque
            fin = len(self.discos) if i == num_hilos - 1 else (i + 1) * tamano_bloque
            hilo = Thread(target=self._resolver_colisiones, args=(inicio, fin))
            hilos.append(hilo)
            hilo.start()

        for hilo in hilos:
            hilo.join()

    def _resolver_colisiones(self, inicio, fin):
        for i in range(inicio, fin):
            for j in range(i + 1, len(self.discos)):
                if self.discos[i].detectar_colision(self.discos[j]):
                    self.discos[i].resolver_colision(self.discos[j])

    def generar_histogramas(self, output_path="histogramas13.png"):
        posiciones_x = [disco.x for disco in self.discos]
        posiciones_y = [disco.y for disco in self.discos]

        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        axs[0].hist(posiciones_x, bins=20, alpha=0.7, color='blue', edgecolor='black')
        axs[0].set_xlabel("Posicion en x")
        axs[0].set_ylabel("Frecuencia")
        axs[0].set_title("Histograma de posiciones en x")

        axs[1].hist(posiciones_y, bins=20, alpha=0.7, color='green', edgecolor='black')
        axs[1].set_xlabel("Posicion en y")
        axs[1].set_ylabel("Frecuencia")
        axs[1].set_title("Histograma de posiciones en y")

        plt.tight_layout()
        plt.savefig(output_path)  # Guardar la imagen de los histogramas
        plt.show()

    def visualizar(self, pasos, dt, output_path="animacion13.mp4"):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.L)
        ax.set_ylim(0, self.L)
        circulos = [plt.Circle((d.x, d.y), d.r, color=d.color, alpha=0.7) for d in self.discos]
        for c in circulos:
            ax.add_artist(c)

        def actualizar(frame):
            self.avanzar(dt)
            for disco, circulo in zip(self.discos, circulos):
                circulo.center = (disco.x, disco.y)
            return circulos

        anim = FuncAnimation(fig, actualizar, frames=pasos, blit=True, interval=50)
        anim.save(output_path, fps=30, extra_args=['-vcodec', 'libx264'])  # Guardar la animación como archivo de video
        print(f"Animación guardada en {output_path}")
        plt.show()

if __name__ == "__main__":
    L = 3  # Tamaño de la caja ajustado
    N = 50  # Número moderado de discos
    sim = Simulacion(L, N)

    # Generar animación
    print("Generando animación...")
    sim.visualizar(pasos=500, dt=0.01, output_path="animacion13.mp4")
    print("Animación generada y guardada como 'animacion13.mp4'")

    # Generar histogramas
    print("Generando histogramas...")
    sim.generar_histogramas(output_path="histogramas13.png")
    print("Histogramas generados y guardados como 'histogramas13.png'")

