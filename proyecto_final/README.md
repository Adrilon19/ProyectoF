# Simulación de Discos en una Caja

Este código implementa una simulación de discos que se mueven y colisionan dentro de una caja cuadrada. Proporciona funcionalidades para analizar el comportamiento de los discos y generar visualizaciones animadas y estadísticas.

## **Estructura del código**

### **1. Clase `Disco`**
La clase `Disco` representa un disco individual con las siguientes propiedades y métodos:

#### **Propiedades**:
- `x`, `y`: Posición del disco.
- `vx`, `vy`: Velocidades en los ejes \(x\) e \(y\).
- `r`: Radio del disco.
- `color`: Color del disco (usado para visualizaciones).

#### **Métodos**:
- **`mover(dt)`**:
  Actualiza la posición del disco en función de su velocidad y el intervalo de tiempo `dt`.
  ```python
  self.x += self.vx * dt
  self.y += self.vy * dt
  ```

- **`chocar_pared(L)`**:
  Detecta colisiones con las paredes de la caja (de lado `L`) y ajusta las velocidades para reflejar el rebote.
  ```python
  if self.x - self.r < margen or self.x + self.r > L - margen:
      self.vx = -self.vx
  ```

- **`detectar_colision(otro)`**:
  Comprueba si el disco está colisionando con otro disco.
  ```python
  distancia = np.sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)
  return distancia < (self.r + otro.r)
  ```

- **`resolver_colision(otro)`**:
  Ajusta las velocidades de dos discos tras una colisión, basándose en la conservación del momento lineal.

### **2. Clase `Simulacion`**
La clase `Simulacion` gestiona el movimiento de todos los discos y la visualización de la simulación.

#### **Constructor (`__init__`)**:
- Crea una lista de discos con posiciones iniciales, radios y velocidades aleatorias. Se asegura de que no haya colisiones iniciales.
  ```python
  if all(not nuevo_disco.detectar_colision(d) for d in self.discos):
      self.discos.append(nuevo_disco)
  ```

#### **Métodos**:

- **`avanzar(dt)`**:
  Avanza la simulación un intervalo de tiempo `dt`:
  1. Mueve cada disco y detecta colisiones con las paredes.
  2. Usa multithreading para dividir la detección de colisiones entre los discos en varios hilos.

  ```python
  num_hilos = 4
  hilo = Thread(target=self._resolver_colisiones, args=(inicio, fin))
  ```

- **`_resolver_colisiones(inicio, fin)`**:
  Detecta y resuelve colisiones entre los discos dentro de un rango de índices (`inicio`, `fin`).

- **`generar_histogramas(output_path)`**:
  Genera histogramas de las velocidades en \(x\) e \(y\) de los discos y los guarda como una imagen.
  ```python
  axs[0].hist(velocidades_x, bins=20, alpha=0.7, color='blue', edgecolor='black')
  ```

- **`visualizar(pasos, dt, output_path)`**:
  Genera una animación del movimiento de los discos usando Matplotlib.
  ```python
  anim = FuncAnimation(fig, actualizar, frames=pasos, blit=True, interval=50)
  ```

---

## **Funciones principales**

### **Generación de la simulación**
La simulación se inicializa creando una caja de lado `L` y un número `N` de discos:
```python
sim = Simulacion(L, N)
```

### **Visualización**
La función `visualizar` genera un archivo de video (`.mp4`) que muestra el movimiento de los discos:
```python
sim.visualizar(pasos=500, dt=0.01, output_path="animacion9.mp4")
```

### **Análisis estadístico**
La función `generar_histogramas` guarda un archivo con histogramas de las velocidades:
```python
sim.generar_histogramas(output_path="histogramas9.png")
```

---

## **Requisitos**

### Dependencias
- Python 3.x
- Bibliotecas:
  - `matplotlib`
  - `numpy`
  - `random`
  - `threading`

### Ejecución
Ejecuta el archivo principal para generar la animación y los histogramas:
```bash
python3 simulacion_DM.py
```

---

## **Archivos generados**
- **`animacion9.mp4`**: Video que muestra el movimiento de los discos.
- **`histogramas9.png`**: Histogramas de las velocidades en \(x\) e \(y\).

---

