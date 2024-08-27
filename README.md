# TC2008B: Modelación de Sistemas Multiagentes con Gráficas Computacionales

## Actividad Integradora

### Parte 1: Sistemas Multiagentes

#### Descripción del Problema
¡Felicidades! Eres el orgulloso propietario de 5 robots nuevos y un almacén lleno de objetos. El dueño anterior del almacén lo dejó en completo desorden, por lo que depende de tus robots organizar los objetos en algo parecido al orden y convertirlo en un negocio exitoso.

Cada robot está equipado con un sistema de tracción potente y puede avanzar sobre cualquier terreno y girar en cualquier dirección. Pueden recoger objetos en celdas de cuadrícula frente a ellos con sus manipuladores, llevarlos a otra ubicación e incluso construir pilas de hasta cinco objetos. Todos los robots están equipados con la tecnología de sensores más nueva, lo que les permite recibir datos de sensores de las cuatro celdas adyacentes. Pueden distinguir si un campo está libre, es una pared, contiene una pila de objetos (y cuántos objetos hay en la pila) o está ocupado por otro robot. Los robots también tienen sensores de presión que les indican si llevan un objeto en ese momento. Además, tienen la capacidad de llevar un mapa consigo.

Tu tarea es enseñar a los robots cómo ordenar su almacén. La organización de los agentes depende de ti, siempre que todos los objetos terminen en pilas ordenadas de cinco.

#### Simulación
- **Inicialización**: Las posiciones iniciales de los K objetos deben ser aleatorias, y todos los objetos estarán a nivel de piso.
- **Posición de los Agentes**: Todos los robots empiezan en posiciones aleatorias vacías.
- **Ejecución**: Se ejecuta durante el tiempo máximo establecido o hasta alcanzar el número máximo de pasos.

#### Recolección de Información
Durante la ejecución, deberás recopilar la siguiente información:
- Tiempo necesario hasta que todos los objetos estén en pilas de máximo 5 objetos.
- Número de movimientos realizados por cada robot.
- Estrategias para disminuir el tiempo y la cantidad de movimientos.

#### Consideraciones
- Los robots pueden operar con razonamiento deductivo, práctico, o una combinación de ambos.
- Implementa un sistema básico de detección de colisiones (por ejemplo, detenerse antes de una colisión y asignar el paso a uno de los robots).
- Los robots solo pueden avanzar hacia adelante, pero pueden girar en todas las direcciones sobre su propio eje.
- Diseña, implementa y usa una ontología en cada agente.

### Parte 2: Gráficas Computacionales

#### Descripción del Problema
Aplica la misma descripción de la Parte 1.

#### Requerimientos
- **Modelado 3D**:
  - Estante, objetos varios, robots (al menos 5), almacén (piso, paredes y puerta) usando modelos con materiales (colores) y texturas (usando mapeo UV).
- **Animación**:
  - Los robots deben desplazarse por el piso del almacén, en los pasillos formados por los estantes.
- **Iluminación**:
  - Al menos una fuente de luz direccional.
  - Al menos una fuente de luz puntual sobre cada robot (tipo sirena), la cual se moverá con cada robot.
- **Detección de Colisiones**:
  - Los robots se moverán en rutas predeterminadas con velocidad aleatoria y detectarán colisiones entre ellos.

### Parte 3: Visión Computacional

#### Descripción del Problema
Aplica la misma descripción de la Parte 1.

#### Requerimientos
- **Identificación de Objetos**:
  - Asume que el robot tiene una cámara que puede estar orientada hacia el frente o según convenga.
  - La cámara debe hacer un stream hacia el modelo de visión (SAM, YOLO, OpenAI, etc.).
  - Cuando el robot percibe un objeto, debe dar una señal de lo que está observando (e.g., un globo de diálogo que diga: "¡Es una manzana!").

### Especificaciones de Entrega

El enlace a un repositorio personal de GitHub debe contener:
- **Parte 1**:
  - Un documento PDF con especificaciones de propiedades de agentes y ambiente, una métrica de utilidad o éxito de cada agente, diagramas de clase de los agentes y ontologías utilizadas, y una conclusión con alternativas de mejora.
  - Código implementado para la simulación.
- **Parte 2**:
  - Un archivo `.unitypackage` con todo lo necesario para ejecutar la solución.

### Notas

Considera que:
- El almacén tiene MxN espacios.
- Hay K objetos iniciales en posiciones aleatorias.
- Al menos 5 robots.
- Tiempo máximo de ejecución (en segundos o pasos).
