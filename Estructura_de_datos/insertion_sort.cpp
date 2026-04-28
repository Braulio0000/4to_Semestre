#include <iostream> // Incluye la biblioteca para operaciones de entrada y salida (cout, cin).
#include <conio.h>  // Incluye la biblioteca para funciones de consola, como getch().

using namespace std; // Permite evitar tener que escribir "std::" antes de funciones como cout, cin, etc.

int main() {
    // Inicializa un arreglo de enteros con valores desordenados.
    int numeros[] = {3, 4, 2, 1, 5}; 
    int i, pos, aux; // Declara variables para el índice, la posición y una variable auxiliar.

    // Bucle que itera sobre cada elemento del arreglo.
    for (i = 0; i < 5; i++) {
        pos = i; // Establece la posición actual.
        aux = numeros[i]; // Guarda el valor actual en la variable auxiliar.

        // Mueve los elementos mayores que 'aux' a la derecha.
        while ((pos > 0) && (numeros[pos - 1] > aux)) {
            numeros[pos] = numeros[pos - 1]; // Desplaza el elemento hacia la derecha.
            pos--; // Decrementa la posición.
        }
        // Coloca el valor de 'aux' en su posición correcta.
        numeros[pos] = aux;
    }

    // Imprime los números ordenados de forma ascendente.
    cout << "Orden Ascendente: ";
    for (i = 0; i < 5; i++) {
        cout << numeros[i] << " "; // Imprime cada elemento del arreglo.
    }

    // Imprime los números ordenados de forma descendente.
    cout << "\nOrden Descendente: ";
    for (i = 4; i >= 0; i--) {
        cout << numeros[i] << " "; // Imprime cada elemento del arreglo en orden inverso.
    }

    getch(); // Espera a que el usuario presione una tecla antes de cerrar la consola.
    return 0; // Termina el programa correctamente.
}

