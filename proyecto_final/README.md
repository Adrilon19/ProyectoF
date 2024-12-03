# Save the documentation as a README.md file for GitHub
readme_path = "/mnt/data/README.md"

with open(readme_path, "w") as readme_file:
    readme_file.write("""
# Documentación: Simulación de Discos en una Caja

Este proyecto simula el movimiento de discos dentro de una caja bidimensional. Los discos pueden colisionar elásticamente entre ellos y con las paredes. Además, se genera una visualización animada del sistema y un análisis de las distribuciones de velocidad mediante histogramas.

---

## **Estructura del Proyecto**

### **Clases Principales**

#### **Clase `Disco`**
Representa un disco dentro de la simulación. Cada disco tiene propiedades y comportamientos individuales.

- **Atributos:**
  - `x`, `y`: Coordenadas de la posición del disco.
  - `vx`, `vy`: Velocidades en las direcciones `x` e `y`.
  - `r`: Radio del disco.
  - `color`: Color del disco (usado para la visualización).

- **Métodos:**
  - `mover(dt)`: Actualiza la posición del disco según su velocidad y el intervalo de tiempo `dt`.
  - `chocar_pared(L)`: Detecta colisiones con las paredes de la caja y actualiza la velocidad invirtiendo su dirección.
  - `detectar_colision(otro)`: Determina si el disco actual colisiona con otro disco.
  - `resolver_colision(otro)`: Calcula y actualiza las velocidades de dos discos después de una colisión.

#### **Clase `Simulacion`**
Controla el sistema global de discos.

- **Atributos:**
  - `L`: Tamaño de la caja (longitud de los lados).
  - `r`: Radio de los discos.
  - `discos`: Lista de objetos `Disco`.
  - `colores`: Lista de colores posibles para los discos.

- **Métodos:**
  - `__init__(L, N, r)`: Inicializa la simulación creando `N` discos con posiciones y velocidades aleatorias.
  - `avanzar(dt)`: Mueve todos los discos, verifica colisiones con las paredes y entre discos, y actualiza sus estados.
  - `generar_histogramas()`: Genera histogramas de las velocidades en las direcciones `x` e `y`.
  - `visualizar(pasos, dt)`: Crea una animación que muestra el movimiento de los discos dentro de la caja.

---

## **Cómo Funciona**

### **1. Inicialización**
El programa comienza definiendo los parámetros principales:
- `L`: Tamaño de la caja (e.g., 1.0).
- `N`: Número de discos en la simulación (e.g., 10).
- `r`: Radio de cada disco (e.g., 0.05).

Luego, se crea un objeto de la clase `Simulacion`:
```python
sim = Simulacion(L, N, r)

### **2. Visualizacion**
El metodo visualizar usa Matplotlib para animar el movimiento de los discos
-sim.visualizar(pasos=500, dt=0.01): pasos es el numero de cuadros de la animacion y dt el intervalo de tiempo entre cuadros
la animcion actualiza las posiciones de los discos y maneja colisiones en tiempo real

### **3.Analisis de velocidades**
el metodo generar_histogramas genera dos histogramas 
-Velocidades en y
-Velocidades en x
se ejecuta despues de la animacion 
sim.generar_histogramas()

### **4. Mover y Detectar Colisiones**

En cada paso de tiempo (dt):

    Se mueve cada disco con mover(dt).
    Se detectan colisiones con las paredes usando chocar_pared(L).
    Se verifican y resuelven colisiones entre pares de discos usando detectar_colision y resolver_colision.


