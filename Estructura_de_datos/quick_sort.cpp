#include <iostream> // Incluye la biblioteca para operaciones de entrada y salida (cout, cin).
#define MAX 1000    // Define una constante MAX con valor 1000, utilizada para el tamaño de los arreglos.
using namespace std; // Permite evitar tener que escribir "std::" antes de funciones como cout, etc.

// Declaración de funciones para el ordenamiento y la impresión.
void quickSort(int[], int);
void print(int[], int);

int main() {
    int n; // Variable para almacenar el número de elementos a ordenar.
    cout << "Ingresa los elementos totales:" << endl; // Solicita al usuario que ingrese la cantidad de elementos.
    cin >> n; // Lee el número de elementos desde la entrada estándar.
    
    int a[n]; // Declara un arreglo de tamaño n para almacenar los elementos.
    
    // Bucle para leer los elementos desde la entrada estándar.
    for (int i = 0; i < n; i++) {
        cout << "Ingresa el elemento: " << i + 1 << " : " << endl; // Solicita el elemento i+1.
        cin >> a[i]; // Lee el elemento y lo almacena en el arreglo.
    }
    
    quickSort(a, n); // Llama a la función quickSort para ordenar el arreglo.
    print(a, n); // Llama a la función print para mostrar el arreglo ordenado.
}

// Función que implementa el algoritmo de ordenamiento Quick Sort.
void quickSort(int a[], int n) {
    int tope, ini, fin, pos; // Variables para controlar los límites y posición de los elementos.
    int may[MAX], menor[MAX]; // Arreglos para almacenar los límites de los subarreglos.
    tope = 0; // Inicializa el tope del arreglo.
    menor[tope] = 0; // Establece el límite inferior del primer subarreglo.
    may[tope] = n - 1; // Establece el límite superior del primer subarreglo.
    
    // Bucle principal que ejecuta el algoritmo mientras haya subarreglos por procesar.
    while (tope >= 0) {
        ini = menor[tope]; // Obtiene el límite inferior del subarreglo actual.
        fin = may[tope]; // Obtiene el límite superior del subarreglo actual.
        tope--; // Decrementa el tope para procesar el siguiente subarreglo.

        int izq, der, aux; // Variables para índices y un auxiliar para el intercambio.
        bool band; // Bandera para controlar el bucle interno.
        izq = ini; // Inicializa el índice izquierdo al inicio del subarreglo.
        der = fin; // Inicializa el índice derecho al final del subarreglo.
        pos = ini; // Inicializa la posición actual al inicio del subarreglo.

        band = true; // Establece la bandera en verdadero para comenzar el bucle.

        // Bucle que reorganiza los elementos del subarreglo.
        while (band == true) {
            // Mueve el índice derecho hacia la izquierda hasta encontrar un elemento menor o igual al pivote.
            while ((a[pos] < a[der]) && (pos != der))
                der--;

            if (pos == der) // Si el índice de posición alcanza el derecho, se termina el bucle.
                band = false;
            else {
                // Intercambia los elementos en la posición actual y en el índice derecho.
                aux = a[pos];
                a[pos] = a[der];
                a[der] = aux;
                pos = der; // Actualiza la posición actual al índice derecho.
            }

            // Mueve el índice izquierdo hacia la derecha hasta encontrar un elemento mayor o igual al pivote.
            while ((a[pos] > a[izq]) && (pos != izq))
                izq++;

            if (pos == izq) // Si el índice de posición alcanza el izquierdo, se termina el bucle.
                band = false;
            else {
                // Intercambia los elementos en la posición actual y en el índice izquierdo.
                aux = a[pos];
                a[pos] = a[izq];
                a[izq] = aux;
                pos = izq; // Actualiza la posición actual al índice izquierdo.
            }
        }

        // Si hay elementos a la izquierda del pivote, se agrega el subarreglo izquierdo a la pila.
        if (ini <= (pos - 1)) {
            tope++;
            menor[tope] = ini; // Límite inferior del subarreglo izquierdo.
            may[tope] = pos - 1; // Límite superior del subarreglo izquierdo.
        }

        // Si hay elementos a la derecha del pivote, se agrega el subarreglo derecho a la pila.
        if (fin >= (pos + 1)) {
            tope++;
            menor[tope] = pos + 1; // Límite inferior del subarreglo derecho.
            may[tope] = fin; // Límite superior del subarreglo derecho.
        }
    }
}

// Función para imprimir los elementos del arreglo.
void print(int a[], int n) {
    cout << "Elementos ordenados:" << endl; // Mensaje que indica que se van a imprimir los elementos ordenados.
    for (int i = 0; i < n; i++) {
        cout << "[" << a[i] << "]"; // Imprime cada elemento del arreglo entre corchetes.
    }
    cout << endl; // Imprime una nueva línea al final.
}

