============================================================
               PROYECTOS DE MULTIPROCESAMIENTO
============================================================

1) Multiplicación de matrices por bloques en paralelo
-----------------------------------------------------
Este proyecto implementa la multiplicación de matrices
dividiendo matrices grandes en bloques más pequeños y
calculando cada bloque en un proceso independiente.
Cada proceso devuelve su resultado mediante una Queue,
y al finalizar se suman los bloques parciales para
reconstruir la matriz final completa.

La multiplicación se valida comparando el resultado
con numpy.matmul para asegurar que la implementación
es correcta.

Conceptos demostrados:
- Paralelismo real con multiprocessing
- Comunicación entre procesos con Queue
- Sincronización de procesos con join()
- Descomposición de matrices por bloques
- Validación numérica de resultados
- Optimización de problemas CPU-bound

Ejemplo de uso: calcula matrices grandes de forma
eficiente aprovechando todos los núcleos del CPU.

------------------------------------------------------------
2) Descarga de datos financieros y procesamiento paralelo
------------------------------------------------------------
Este proyecto descarga datos históricos de símbolos
financieros (Yahoo Finance) y procesa la información
en paralelo usando procesos.

Cada símbolo se descarga en un proceso independiente,
y los resultados se devuelven mediante Queue para
posteriormente agregarlos en un DataFrame único.
Se añaden características temporales (año, semana, mes)
y se realizan agregaciones.

Conceptos demostrados:
- Paralelismo para tareas I/O-bound y CPU-bound
- Multiprocesamiento con Queue
- Procesamiento de datos financieros
- Agrupación y agregación de DataFrames
- Medición de tiempos de ejecución

============================================================
Ambos proyectos muestran cómo aprovechar Python para
resolver problemas reales usando paralelismo y
procesamiento eficiente, combinando teoría y práctica.
============================================================
