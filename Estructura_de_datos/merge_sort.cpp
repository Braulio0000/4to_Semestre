#include <iostream> // Incluye la biblioteca para operaciones de entrada y salida (cout, cin).
#include <vector>   // Incluye la biblioteca para usar el contenedor vector.

using namespace std; // Permite evitar tener que escribir "std::" antes de funciones como cout, etc.

// Función que combina dos subarreglos en un arreglo ordenado.
void merge(vector<int>& arreglo, int inicio, int mitad, int final) {
    int i, j, k; // Variables para los índices de los arreglos.
    int elementosIzq = mitad - inicio + 1; // Número de elementos en el subarreglo izquierdo.
    int elementosDer = final - mitad; // Número de elementos en el subarreglo derecho.

    // Crea vectores temporales para los subarreglos izquierdo y derecho.
    vector<int> izquierda(elementosIzq);
    vector<int> derecha(elementosDer);

    // Copia los elementos del subarreglo izquierdo.
    for (int i = 0; i < elementosIzq; i++) {
        izquierda[i] = arreglo[inicio + i];
    }
    // Copia los elementos del subarreglo derecho.
    for (int j = 0; j < elementosDer; j++) {
        derecha[j] = arreglo[mitad + 1 + j];
    }

    i = 0; // Índice para el subarreglo izquierdo.
    j = 0; // Índice para el subarreglo derecho.
    k = inicio; // Índice para el arreglo original.

    // Combina los elementos de los subarreglos en el arreglo original.
    while (i < elementosIzq && j < elementosDer) {
        if (izquierda[i] <= derecha[j]) { // Compara los elementos de los subarreglos.
            arreglo[k] = izquierda[i]; // Coloca el elemento izquierdo en el arreglo.
            i++; // Avanza en el subarreglo izquierdo.
        } else {
            arreglo[k] = derecha[j]; // Coloca el elemento derecho en el arreglo.
            j++; // Avanza en el subarreglo derecho.
        }
        k++; // Avanza en el arreglo original.
    }

    // Copia los elementos restantes del subarreglo derecho, si los hay.
    while (j < elementosDer) {
        arreglo[k] = derecha[j];
        j++;
        k++;
    }

    // Copia los elementos restantes del subarreglo izquierdo, si los hay.
    while (i < elementosIzq) {
        arreglo[k] = izquierda[i];
        i++;
        k++;
    }
}

// Función que implementa el algoritmo de ordenamiento por mezcla (Merge Sort).
void mergeSort(vector<int>& arreglo, int inicio, int final) {
    if (inicio < final) { // Verifica si hay más de un elemento.
        int mitad = inicio + (final - inicio) / 2; // Encuentra el punto medio.
        mergeSort(arreglo, inicio, mitad); // Ordena la primera mitad.
        mergeSort(arreglo, mitad + 1, final); // Ordena la segunda mitad.
        merge(arreglo, inicio, mitad, final); // Combina las dos mitades ordenadas.
    }
}

// Función para imprimir los elementos del arreglo.
void imprimirArreglo(vector<int> arreglo) {
    for (int i = 0; i < arreglo.size(); i++) {
        cout << arreglo[i] << " "; // Imprime cada elemento del arreglo.
    }
    cout << endl; // Imprime una nueva línea al final.
}

int main() {
    vector<int> prueba1 = {12, 0, 6, 2, 9, 34, 1}; // Inicializa un vector con valores desordenados.
    imprimirArreglo(prueba1); // Imprime el arreglo original.
    mergeSort(prueba1, 0, prueba1.size() - 1); // Aplica el algoritmo Merge Sort al arreglo.
    imprimirArreglo(prueba1); // Imprime el arreglo ordenado.
    return 0; // Termina el programa correctamente.
}
