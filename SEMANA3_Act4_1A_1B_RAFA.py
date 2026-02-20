

# Enunciado actividad

# A11 A12
# A21 A22

# B11 B12
# B21 B22

# C11=(A11*B11 + A12*B21)    C12=(A11*B12 + A12*B22)
# C21=(A21*B11 + A22*B21)    C22=(A21*B12 + A22*B22)
from multiprocessing import Queue
import time
import multiprocessing
import numpy as np
from numpy.random import seed
from numpy.random import rand
def intro():
    print("""
┏┓      ┓  ┓•             ┏┓•            ┳┓•    •┓   • ┓   
┃┃┏┓┏┓┏┓┃┏┓┃┓┏┏┳┓┏┓┏  ┓┏  ┗┓┓┏╋┏┓┏┳┓┏┓┏  ┃┃┓┏╋┏┓┓┣┓┓┏┓┏┫┏┓┏
┣┛┗┻┛ ┗┻┗┗ ┗┗┛┛┗┗┗┛┛  ┗┫  ┗┛┗┛┗┗ ┛┗┗┗┻┛  ┻┛┗┛┗┛ ┗┗┛┗┻┗┗┻┗┛┛
                       ┛                                   

          Actividad 4 Rafael Cañada Abolafia \n\n\n
          
    1. Modificar el programa de multiplicación de matrices para que todas las funciones paralelas sean ejecutadas en un proceso.
        a. Implementar una versión donde no haga falta coordinación porque cada bloque
        de salida se calcule en una función.
        b. Implementar una versión donde las multiplicaciones de bloques que tienen que
        ser sumadas para obtener el resultado se pongan en sendas colas que será
        consumidas para realizar las sumar y calcular el resultado final
          
    
          """)
def Crea_bloque(N,M):
        N = N # Numero de bloques
        M = M # Tamaño de los bloques

        seed(10)

        A_bloques = []
        B_bloques = []

        for i in range(N):
            fila_A = []
            fila_B = []
            for j in range(N):
                fila_A.append(rand(M, M))
                fila_B.append(rand(M, M))
            A_bloques.append(fila_A)
            B_bloques.append(fila_B)

        

        

        A = np.block(A_bloques)
        B = np.block(B_bloques)
        print("Matrices Generadas.\n")
        print(f"A = {A}")
        print("\n")
        print(f"B = {B}\n\n")
        return A,B,A_bloques,B_bloques


def Antes_De_Sumar_Bloques_Verifica_que_TODOS_los_bloques_Finalizaron(C_hilos):
    n = 0
    for fila_hilos in C_hilos:
            for filaa in fila_hilos:
                filaa.join()
                n+=1
    return n



     

def multiply(A, B,C_sol_fila):
    res = np.zeros((A.shape[0], A.shape[1]))  

    for k in range(A.shape[0]):
        for i in range(B.shape[1]):            
            for j in range(A.shape[1]):
                #print("---")
                #print(f"{A[k][j]} x {B[j][i]} = {A[k][j] * B[j][i]}")
                res[k, i] += A[k][j] * B[j][i]                              # Multiplica filas x columnas entre bloques
                                                                            # Por ejemplo A11 = [[1 2],  *   B12 = [[5 6],   = (1*5) + (2*7)
                                                                            #                    [3,4]]             [7 8]]
    C_sol_fila.put(res)                                                     # añado a la cola


def multiply_bloques(A_bl, B_bl):
    
    C_hilos = []
    N = len(A_bl)
    fila_x_columna = []
    n_procesos = 0                                                                             # para contar los hilos totales
    for k in range(N):
                              
        for i in range(N):
            C_sol_fila = []
            cola_fila = []
            for j in range(N):
                C_sol_fila.append(Queue())                                                  # Pasamos como parámetros Queue()
                cola_fila.append(
                    multiprocessing.Process(
                        target=multiply,args=(A_bl[k][j], B_bl[j][i],C_sol_fila[-1])        # Por ejemplo multiply(A11,B11) , multiply(A11,B12) ......
                    )
                )    
                cola_fila[-1].start()
                
            C_hilos.append(cola_fila)                                            
            
            fila_x_columna.append(C_sol_fila)
            
            
    n_procesos += Antes_De_Sumar_Bloques_Verifica_que_TODOS_los_bloques_Finalizaron(C_hilos)   # nos aseguramos de que todos los procesos se ejecutan
    
    print(f"\n\nSe han generado y ejecutado un total de {n_procesos} procesos de multiplicaciones\n\n")
    return fila_x_columna

def suma_filas_generadas(solucion_bloques, N):
    Csol = []

    for fila in range(N):
        fila_completa = []

        for col in range(N):
            indice = fila * N + col
            bloques_a_sumar = solucion_bloques[indice]
            bloque_suma = bloques_a_sumar[0].copy()
            for b in bloques_a_sumar[1:]:
                bloque_suma += b

            fila_completa.append(bloque_suma)

        Csol.append(fila_completa)

    return Csol


def desencolar(procesos_bloques):
    sumaCij = []
    
    
    for i in range(len(procesos_bloques)):
        process_row  = []
        for j in range(len(procesos_bloques[0])):
            process_row.append(procesos_bloques[i][j].get())
        sumaCij.append(process_row)
    return sumaCij


if __name__ == '__main__':
    intro()                                                     # Presentación Actividad
    
    N = int(input(" nº bloques :"))                                                       # Numero de bloques
    M = int(input(" tamaño de los bloque :"))                                                       # Tamaño de los bloques
                                  
    A,B, A_bloques, B_bloques = Crea_bloque(N,M)                # Inicializacion matrices, bloques
    
    ########################################################
    inicio = time.perf_counter()

    Cola_De_Procesos_Mul = multiply_bloques(A_bloques, B_bloques)   # Solución Multiplicación Matrices python puro
    sumaCij = desencolar(Cola_De_Procesos_Mul)                      # Funciona para desencolar procesos 
    Cij = suma_filas_generadas(sumaCij,N)                           # Suma las multiplicaciones de cada fila y genera Cij FINAL
    
    fin = time.perf_counter()
    ########################################################
    
    
    
    print("\nSolucion Multiplicación Matrices python puro\n")
    print(np.block(Cij))
    print("Solucion libreria numpy\n")
    print(np.matmul(A, B))
    

    if np.allclose(np.matmul(A, B), np.block(Cij)) == True:
        print("\n\n\nTest Verificación correcta")
        print(f"Tiempo de ejecución: {fin-inicio}sg")
    else:
        print("\n\n\nTest Verificación incorrecta")
