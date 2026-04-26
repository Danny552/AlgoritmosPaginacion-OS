Este programa es una herramienta educativa interactiva diseñada para visualizar y comparar el comportamiento de diferentes algoritmos de gestión de memoria (reemplazo de páginas) utilizados en sistemas operativos.

Desarrollado por: **Daniel Alejandro Henao** y **Laura Sofía Cardona**.

## Características

El simulador permite ejecutar y visualizar paso a paso cómo se gestionan los marcos de memoria (frames) ante una secuencia de referencias de páginas. Incluye una **Matriz de Ejecución** visual inspirada en representaciones académicas clásicas (estilo Excel) para facilitar la comprensión de los fallos y aciertos.

### Algoritmos Implementados:
1.  **Óptimo:** Reemplaza la página que no se utilizará durante el periodo de tiempo más largo en el futuro. (Utilizado como benchmark teórico).
2.  **FIFO Mejorado (Segunda Oportunidad):** Una variante de FIFO que utiliza un bit de referencia para dar una "segunda oportunidad" a las páginas que han sido accedidas recientemente antes de ser reemplazadas.
3.  **LRU (Least Recently Used):** Reemplaza la página que no ha sido utilizada por el tiempo más largo en el pasado.

## Interfaz Visual

* **Marcos de Memoria (3 Frames):** Visualización animada del estado actual de la RAM.
* **Estadísticas en Tiempo Real:** Cálculo automático de Fallos, Aciertos (Hits) y porcentaje de Eficiencia.
* **Matriz de Ejecución:**
    * **Encabezado Verde Oscuro:** Página entrante.
    * **Celda Amarilla:** Indica un **Fallo de Página** y el marco específico que fue modificado.
    * **Celda Verde Claro:** Indica un **Acierto (Hit)** o una página que permanece en memoria sin cambios.

## Requisitos Técnicos

* **Lenguaje:** Python 3.12+
* **Framework de UI:** [Flet](https://flet.dev/) (basado en Flutter) (incorporado en el momento de la descarga).