# Hill-Climbing para la función Sphere

Implementación en Python de los **Algoritmos 1 y 4** del *Material de Apoyo de la clase de Inteligencia Artificial: Metaheurísticas*:

- **Algoritmo 1. Hill-Climbing**: ciclo principal de búsqueda.
- **Algoritmo 4. Bounded Uniform Convolution**: operación *Tweak* que genera un vecino respetando los límites.

El objetivo es minimizar la función Sphere de *n* dimensiones:

$$f(\mathbf{x}) = \sum_{i=1}^{n} x_i^2, \qquad -10 \le x_i \le 10$$

cuyo mínimo global es $f(0, \dots, 0) = 0$.

## Requisitos

- Python 3.7 o superior (probado con Python 3.11).
- No usa bibliotecas externas, solo `random` y `dataclasses` de la biblioteca estándar.

## Ejecución

```bash
git clone https://github.com/Arclyne/algoritmo-hill-climbing.git
cd algoritmo-hill-climbing
python3 hill_climbing.py
```

### Salida de ejemplo (parámetros por defecto)

```
Hill-Climbing parameters
  Dimensions (n):             2
  Bounds:                     [-10.0, 10.0]
  Alteration probability (p): 0.5
  Step size (r):              1.0
  Max evaluations:            10000
  Seed:                       42

Results
  Initial solution: [2.788536, -9.499785]
  Initial f(x):     9.802185e+01
  Best solution:    [-0.000749, -0.000406]
  Best f(x):        7.255184e-07
  Iterations:       9999
  Evaluations:      10000
  Accepted moves:   44 (0.4%)
```

El algoritmo parte de un punto aleatorio con f(x) ≈ 98 y termina a menos de una milésima del origen (f(x) ≈ 7 × 10⁻⁷). El signo de las coordenadas finales no importa: la función eleva cada coordenada al cuadrado.

## Parámetros

Los parámetros se configuran editando las constantes al inicio de [`hill_climbing.py`](hill_climbing.py). Antes de ejecutar, `validate_parameters` revisa que cada valor esté en su rango válido.

| Constante | Símbolo | Valor | Rango válido | Descripción |
|---|---|---|---|---|
| `DIMENSIONS` | n | `2` | n ≥ 1 | Número de coordenadas del vector x |
| `LOWER_BOUND` | L | `-10.0` | fijo | Límite inferior de cada coordenada |
| `UPPER_BOUND` | U | `10.0` | fijo | Límite superior de cada coordenada |
| `ALTERATION_PROBABILITY` | p | `0.5` | 0 < p ≤ 1 | Probabilidad de alterar cada coordenada en el Tweak |
| `STEP_SIZE` | r | `1.0` | r > 0 | El ruido de cada coordenada se sortea en [−r, r] |
| `MAX_EVALUATIONS` | — | `10000` | ≥ 1 | Condición de paro: evaluaciones de la función Sphere |
| `SEED` | — | `42` | entero o `None` | Semilla del generador aleatorio |

### Cómo se configuraron

**Dimensiones (n = 2).** Es el caso que se puede visualizar como el “tazón” de la función. El código no asume un valor fijo: el punto inicial, el ciclo del Tweak y la suma de la función usan `DIMENSIONS`, así que basta con cambiar la constante para trabajar con 10, 30 o más dimensiones.

**Límites (−10, 10).** Los fija la actividad. Se usan en dos momentos: al generar el punto inicial y en cada Tweak, donde el ruido se vuelve a sortear si saca a una coordenada del rango (nunca se recorta).

**Probabilidad de alteración (p = 0.5).** Con n = 2 se altera en promedio una coordenada por iteración. Un valor bajo desperdicia iteraciones en las que ninguna coordenada cambia; un valor alto mueve todas a la vez y aumenta la probabilidad de que el candidato se rechace. En los experimentos de abajo, p = 0.5 dio el mejor resultado para n = 2. Para dimensiones mayores conviene reducirlo (ver tabla).

**Tamaño de paso (r = 1.0).** Equivale al 5 % del ancho del espacio de búsqueda (20 unidades). Permite cruzar el espacio en pocas decenas de iteraciones desde cualquier punto inicial. Cerca del mínimo, pasos más finos dan mayor precisión: con r = 0.1 el resultado mejora, a costa de avanzar más lento al inicio.

**Condición de paro (10 000 evaluaciones).** Se eligió contar evaluaciones de la función objetivo porque es la medida estándar para comparar metaheurísticas. Cada iteración hace exactamente una evaluación (la del candidato U), y f(X) se guarda para no recalcularlo, por lo que:

```
evaluaciones = 1 (punto inicial) + iteraciones
```

**Semilla (42).** Con una semilla fija cada ejecución produce los mismos resultados, lo que permite reproducir los experimentos. Con `SEED = None` cada ejecución parte de un punto inicial distinto.

### Experimentos

Mejor f(x) al terminar, como mediana y peor caso sobre varias semillas.

**Efecto de r** (n = 2, p = 0.5, 10 000 evaluaciones, semillas 1–30):

| r | Mediana | Peor caso |
|---|---|---|
| 0.1 | 2.90e-09 | 1.83e-08 |
| 0.5 | 1.16e-07 | 6.91e-07 |
| **1.0** | **2.06e-07** | **2.07e-06** |
| 2.0 | 1.57e-06 | 1.92e-05 |
| 5.0 | 1.31e-05 | 5.49e-05 |

**Efecto de p** (n = 2, r = 1.0, 10 000 evaluaciones, semillas 1–30):

| p | Mediana | Peor caso |
|---|---|---|
| 0.1 | 2.32e-06 | 1.51e-05 |
| **0.5** | **2.06e-07** | **2.07e-06** |
| 1.0 | 8.59e-05 | 3.53e-04 |

**Efecto de p con más dimensiones** (n = 30, r = 1.0, 50 000 evaluaciones, semillas 1–10):

| p | Mediana | Peor caso |
|---|---|---|
| 0.05 | 2.06e-04 | 4.18e-04 |
| 0.1 | 9.77e-04 | 1.94e-03 |
| 0.2 | 4.74e-02 | 5.88e-02 |
| 0.5 | 1.56e+00 | 2.09e+00 |
| 1.0 | 4.81e+00 | 5.56e+00 |

Con más dimensiones conviene un p pequeño: alterar pocas coordenadas por iteración hace más probable que el candidato mejore.

## Funcionamiento

### Algoritmo 1: Hill-Climbing (`hill_climbing`)

1. Genera un punto inicial X con n valores aleatorios en [−10, 10] y lo evalúa.
2. Mientras no se alcance el máximo de evaluaciones:
   1. Genera un candidato U = Tweak(X).
   2. Evalúa f(U).
   3. Si f(U) < f(X), acepta el candidato: X ← U. Si no, lo descarta.
3. Regresa X, que es la mejor solución encontrada: solo se aceptan mejoras, así que X nunca empeora.

### Algoritmo 4: Bounded Uniform Convolution (`bounded_uniform_convolution`)

1. Copia X en W, para no modificar la solución actual.
2. Para cada coordenada i:
   1. Si p ≥ un número aleatorio en [0, 1), la coordenada se altera.
   2. Sortea un ruido uniforme en [−r, r] hasta que L ≤ Wᵢ + ruido ≤ U.
   3. Wᵢ ← Wᵢ + ruido.
3. Regresa W como candidato.

> **Nota:** en el material, la línea 10 del Algoritmo 4 aparece como `until Uᵢ ≤ Wᵢ + n ≤ Lᵢ`, con los límites invertidos. La implementación usa la condición correcta: `Lᵢ ≤ Wᵢ + n ≤ Uᵢ`.

## Estructura del código

| Elemento | Descripción |
|---|---|
| Constantes | Parámetros del algoritmo |
| `HillClimbingResult` | Resultado: solución inicial y final, sus valores, iteraciones, evaluaciones y movimientos aceptados |
| `validate_parameters` | Valida los parámetros antes de ejecutar |
| `sphere` | Función objetivo f(x) = Σ xᵢ² |
| `random_solution` | Genera el punto inicial aleatorio |
| `bounded_uniform_convolution` | Algoritmo 4 (Tweak) |
| `hill_climbing` | Algoritmo 1 |
| `main` | Valida, ejecuta e imprime parámetros y resultados |
