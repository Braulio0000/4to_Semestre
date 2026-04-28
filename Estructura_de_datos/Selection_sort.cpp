// Ordenamiento por Selección

#include <iostream> // Incluye la biblioteca para operaciones de entrada y salida (cout, cin).
#include <conio.h>  // Incluye la biblioteca para funciones de consola (getch).

using namespace std; // Permite evitar tener que escribir "std::" antes de funciones como cout, etc.

int main() {
    // Inicializa un arreglo de números desordenados.
    int numeros[] = {3, 4, 5, 2, 1};
    int i, j, aux, min; // Declaración de variables: índices, auxiliar y mínimo.

    // Algoritmo del Ordenamiento por Selección
    for (i = 0; i < 5; i++) { // Bucle que recorre todo el arreglo.
        min = i; // Asigna el índice actual como el mínimo.
        
        // Bucle interno para encontrar el índice del valor mínimo en el subarreglo no ordenado.
        for (j = i + 1; j < 5; j++) {
            if (numeros[j] < numeros[min]) { // Compara el elemento actual con el mínimo encontrado.
                min = j; // Actualiza el índice del mínimo si se encuentra un nuevo mínimo.
            }
        }
        
        // Intercambia el elemento en la posición actual con el mínimo encontrado.
        aux = numeros[i]; // Almacena el valor actual en una variable auxiliar.
        numeros[i] = numeros[min]; // Coloca el valor mínimo en la posición actual.
        numeros[min] = aux; // Coloca el valor original de la posición actual en la posición del mínimo.
    }

    // Imprime el arreglo ordenado en orden ascendente.
    cout << "Orden Ascendente: ";
    for (i = 0; i < 5; i++) {
        cout << numeros[i] << " "; // Imprime cada número en el arreglo.
    }

    // Imprime el arreglo en orden descendente.
    cout << "\nOrden Descendente: ";
    for (i = 4; i >= 0; i--) {
        cout << numeros[i] << " "; // Imprime cada número en el arreglo en orden inverso.
    }

    getch(); // Espera a que el usuario presione una tecla antes de cerrar la consola.
    return 0; // Termina el programa correctamente.
}
