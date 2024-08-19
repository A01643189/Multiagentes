# Multiagentes

Evidencia 1. Actividad Integradora

    Fecha de entrega Domingo a las 23:59 Puntos 100 Entregando una herramienta externa

Subcompetencias a evaluar

La evidencia es la demostración de lo que has logrado. Con ésta, tu profesor podrá observar y evaluar la subcompetencia en la profundidad y complejidad (nivel del dominio A, B o C) que la unidad de formación te llevó a desarrollar. Con esta evidencia demostrarás las siguientes subcompetencias:


SICT0102 Demostración del funcionamiento de los sistemas computacionales

STC0103 Generación de modelos computacionales
Descripción de la evidencia
Instrucciones:

    Ser puntual y presentarte en el sitio señalado con todo el material que te sea solicitado.
    Escucha con atención las instrucciones del profesor. 
    Ten muy claras las instrucciones de la actividad.
    Lee cuidadosamente la redacción de la actividad. Es muy importante comprender todo lo que se te pide realizar.
    Realiza la entrega en tiempo y forma de acuerdo a los requerimientos establecidos en el documento de la actividad.
    ¡Mucho éxito!

Especificaciones  

    A llevarse a cabo durante la Semana 3.
    Como se establece en el documento de definición de la actividad integradora. Actividad integradora - Sistemas multiagentes con GC.pdf 

Download Actividad integradora - Sistemas multiagentes con GC.pdf
Entrega: un enlace a un repositorio personal de Github. Deja el enlace en la página que se abre desde este espacio de Canvas.

# TC2008B - Modelación de Sistemas Multiagentes con Gráficas Computacionales

## Actividad Integradora

### Parte 1: Sistemas Multiagentes

#### Descripción del Problema
¡Felicidades! Eres el orgulloso propietario de 5 robots nuevos y un almacén lleno de objetos. El dueño anterior del almacén lo dejó en completo desorden, por lo que depende de tus robots organizar los objetos en algo parecido al orden y convertirlo en un negocio exitoso.

Cada robot está equipado con un sistema de tracción potente y puede avanzar sobre cualquier terreno, y también girar en cualquier dirección. Pueden recoger objetos en celdas de cuadrícula frente a ellos con sus manipuladores, luego llevarlas a otra ubicación e incluso construir pilas de hasta cinco objetos.

Los robots están equipados con tecnología de sensores que les permite recibir datos de las cuatro celdas adyacentes, distinguiendo si un campo está libre, es una pared, contiene una pila de objetos (y cuántos objetos hay en la pila), o está ocupado por otro robot. También tienen sensores de presión que les indican si llevan un objeto en ese momento.

Tu tarea es enseñar a los robots cómo ordenar su almacén. La organización de los agentes depende de ti, siempre que todos los objetos terminen en pilas ordenadas de cinco.

#### Simulación
- **Inicialización:**
  - Los objetos inician en posiciones aleatorias a nivel de piso.
  - Los robots comienzan en posiciones aleatorias vacías.
  - Se establece un tiempo máximo de ejecución (o un número máximo de steps).

- **Datos a recopilar:**
  - Tiempo necesario hasta que todos los objetos estén en pilas de máximo 5 objetos.
  - Número de movimientos realizados por cada robot.
  - Análisis de estrategias que podrían disminuir el tiempo y la cantidad de movimientos.

#### Puntos Importantes
- Los robots solo pueden operar con razonamiento deductivo, razonamiento práctico, o una combinación de ambos.
- Los robots detectarán colisiones entre ellos en el mundo 3D y se deberá implementar un sistema básico para evitar colisiones.
- Los robots solo pueden avanzar hacia el frente, pero pueden girar en todas las direcciones sobre su propio eje.
- Se deberá diseñar, implementar y usar una ontología en cada agente.

### Parte 2: Gráficas Computacionales

#### Descripción del Problema
La actividad consiste en modelar y desplegar la representación en 3D del sistema de robots descrito en la Parte 1.

#### Requisitos
- **Modelos:**
  - Estante (con repetición de instancias o prefabs por código).
  - Objetos varios (con repetición de instancias o prefabs por código).
  - Robots (con repetición de instancias o prefabs por código, al menos 5 robots).
  - Almacén (piso, paredes y puerta).
  
- **Animación:**
  - Los robots deberán desplazarse sobre el piso del almacén, en los pasillos que forman los estantes.

- **Iluminación:**
  - Al menos una fuente de luz direccional.
  - Al menos una fuente de luz puntual sobre cada robot (tipo sirena) que se mueva con cada robot.

- **Detección de Colisiones:**
  - Los robots se moverán en rutas predeterminadas con velocidades predeterminadas (aleatorias).
  - Los robots comenzarán a operar en posiciones predeterminadas (aleatorias).
  - Los robots detectarán colisiones entre ellos.

### Especificaciones de Entrega

Deberás entregar un enlace a un repositorio personal de GitHub que contenga:

- **Parte 1:**
  - Documento PDF con especificaciones de Propiedades de agentes y ambiente, así como una métrica de utilidad o éxito de cada agente.
  - Diagramas de clases de los agentes utilizados, y diagramas de clase de las ontologías utilizadas.
  - Código implementado para la simulación del reto.
  - Conclusión con una breve descripción de soluciones alternativas para mejorar la eficiencia de los agentes.

- **Parte 2:**
  - Archivo `.unitypackage` con todo lo necesario para ejecutar la solución.

### Notas
Para ambas partes del problema, considera que:

- El almacén tiene MxN espacios.
- Hay K cajas iniciales en posiciones aleatorias.
- Se utilizan al menos 5 robots.
- Hay un tiempo máximo de ejecución (segundos o steps).
