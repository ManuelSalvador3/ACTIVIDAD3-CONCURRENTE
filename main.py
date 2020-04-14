import sys
import math
import random
import multiprocessing
import time

#Funcion merge sort que hace uso de la funcion merge anterior para ordenar el array de forma natural
def mergeSort(array):
    length = len(array)
    if length <= 1:
        return array
    middle = length // 2
    left = mergeSort(array[:middle])
    right = mergeSort(array[middle:])
    return merge(left, right)

def merge(*args): #Funcion la cual usa el mergeSort tanto para el lado derecho como el lado izquierdo
    izq, der = args[0] if len(args) == 1 else args
    longi_izq, longi_der = len(izq), len(der)
    index_izq, index_der = 0, 0
    merged = []

    while index_izq < longi_izq and index_der < longi_der:
        if izq[index_izq] <= der[index_der]:
            merged.append(izq[index_izq])
            index_izq += 1
        else:
            merged.append(der[index_der])
            index_der += 1
    if index_izq == longi_izq:
        merged.extend(der[index_der:])
    else:
        merged.extend(izq[index_izq:])

    return merged

def mergeSortParalelo(array): #Funcion mergeSort la cual paraleliza el proceso del algoritmo con todos los nucleos de nuestro procesador
    procesos = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=procesos)
    tam = int(math.ceil(float(len(array)) / procesos))
    array = [array[i * tam:(i + 1) * tam] for i in range(procesos)]
    array = pool.map(mergeSort, array)

    while len(array) > 1: #Hacemos merge de la parejas que estan usando el pool de procesos
        extra = array.pop() if len(array) % 2 == 1 else None
        array = [(array[i], array[i + 1]) for i in range(0, len(array), 2)]
        array = pool.map(merge, array) + ([extra] if extra else [])
    return array[0]

#Main donde ejecutamos el merge Sort en paralelo para
if __name__ == "__main__":
    tam = 10
    array = [random.randint(0, tam) for _ in range(tam)] #tam siendo el tamaño del array que se va a ordenar
    for sort in mergeSort, mergeSortParalelo:
        array_ordenado = sort(array)
    print("El array ordenado es", array_ordenado)

