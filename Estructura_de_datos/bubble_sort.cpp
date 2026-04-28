// Método Burbuja

#include <iostream> // Incluye la biblioteca para operaciones de entrada y salida (cout, cin).
#include <conio.h>  // Incluye la biblioteca para funciones de consola, como getch().

using namespace std; // Permite evitar tener que escribir "std::" antes de funciones como cout, cin, etc.

int main() {
    // Inicializa un arreglo de 5 elementos con valores desordenados.
    int array[5] = {2, 3, 1, 5, 4}; 
    int i, j, aux; // Declara variables para los índices y una variable auxiliar para el intercambio.

    // Bucle externo que itera sobre el arreglo.
    for (i = 0; i < 5; i++) {
        // Bucle interno que compara elementos adyacentes.
        for (j = 0; j < 4; j++) {
            // Si el elemento actual es mayor que el siguiente, se realiza el intercambio.
            if (array[j] > array[j + 1]) {
                aux = array[j]; // Guarda el valor actual en la variable auxiliar.
                array[j] = array[j + 1]; // Asigna el siguiente valor al actual.
                array[j + 1] = aux; // Asigna el valor guardado en la auxiliar al siguiente.
            }
        }
    }

    // Imprime los números ordenados de forma ascendente.
    cout << "Números de forma Ascendente: ";
    for (i = 0; i < 5; i++) {
        cout << array[i] << " "; // Imprime cada elemento del arreglo.
    }

    // Imprime los números ordenados de forma descendente.
    cout << "\nNúmeros de forma Descendente: ";
    for (i = 4; i >= 0; i--) {
        cout << array[i] << " "; // Imprime cada elemento del arreglo en orden inverso.
    }

    getch(); // Espera a que el usuario presione una tecla antes de cerrar la consola.
    return 0; // Termina el programa correctamente.
}
