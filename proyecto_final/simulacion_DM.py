#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
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
        if self.x - self.r < 0 or self.x + self.r > L:
            self.vx = -self.vx
        if self.y - self.r < 0 or self.y + self.r > L:
            self.vy = -self.vy

    def detectar_colision(self, otro):
        dx = self.x - otro.x
        dy = self.y - otro.y
        distancia = np.sqrt(dx**2 + dy**2)
        return distancia < 2 * self.r

    def resolver_colision(self, otro):
        dx = self.x - otro.x
        dy = self.y - otro.y
        distancia = np.sqrt(dx**2 + dy**2)

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

class Simulacion:
    def __init__(self, L, N, r):
        self.L = L
        self.r = r
        self.discos = []
        self.colores = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow", "brown", "pink"]

        for _ in range(N):
            while True:
                x = np.random.uniform(r, L - r)
                y = np.random.uniform(r, L - r)
                vx = np.random.uniform(-1, 1)
                vy = np.random.uniform(-1, 1)
                color = random.choice(self.colores)

                nuevo_disco = Disco(x, y, vx, vy, r, color)
                if all(not nuevo_disco.detectar_colision(d) for d in self.discos):
                    self.discos.append(nuevo_disco)
                    break

    def avanzar(self, dt):
        # Mover los discos y manejar colisiones con las paredes
        for disco in self.discos:
            disco.mover(dt)
            disco.chocar_pared(self.L)

        # Paralelizar la detección y resolución de colisiones entre discos
        num_hilos = 4
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

    def generar_histogramas(self):
        velocidades_x = [disco.vx for disco in self.discos]
        velocidades_y = [disco.vy for disco in self.discos]

        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        axs[0].hist(velocidades_x, bins=20, alpha=0.7, color='blue', edgecolor='black')
        axs[0].set_xlabel("Velocidad en x")
        axs[0].set_ylabel("Frecuencia")
        axs[0].set_title("Histograma de velocidades en x")

        axs[1].hist(velocidades_y, bins=20, alpha=0.7, color='green', edgecolor='black')
        axs[1].set_xlabel("Velocidad en y")
        axs[1].set_ylabel("Frecuencia")
        axs[1].set_title("Histograma de velocidades en y")

        plt.tight_layout()
        plt.show()

    def visualizar(self, pasos, dt):
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
        plt.show()

if __name__ == "__main__":
    L = 4.0  # Tamaño de la caja
    N = 50   # Número de discos
    r = 0.05 # Radio de los discos

    sim = Simulacion(L, N, r)
    sim.visualizar(pasos=500, dt=0.01)
    sim.generar_histogramas()

