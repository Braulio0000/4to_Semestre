#include <iostream>

class ListaDinamica { // Define una clase llamada ListaDinamica
private:
    int* lista;      // Puntero a un arreglo dinámico de enteros
    int tamanio;     // Variable para almacenar el número actual de elementos en la lista
    int capacidad;   // Variable para almacenar la capacidad actual de la lista

public:
    ListaDinamica() { // Constructor que inicializa la lista vacía
        tamanio = 0;  // Inicializa el tamaño de la lista a 0
        capacidad = 5; // Inicializa la capacidad de la lista
        lista = new int[capacidad]; // Reserva memoria para la lista
    }

    ~ListaDinamica() { // Destructor para liberar la memoria
        delete[] lista; // Libera la memoria reservada
    }

    void agregar(int elemento) { // Método para agregar un elemento al final de la lista
        if (tamanio >= capacidad) { // Verifica si hay que aumentar la capacidad
            capacidad *= 2; // Duplicar la capacidad
            int* nuevaLista = new int[capacidad]; // Reserva nueva memoria
            for (int i = 0; i < tamanio; i++) {
                nuevaLista[i] = lista[i]; // Copia los elementos existentes
            }
            delete[] lista; // Libera la memoria antigua
            lista = nuevaLista; // Actualiza el puntero
        }
        lista[tamanio] = elemento; // Agrega el elemento al final de la lista
        tamanio++; // Incrementa el tamaño de la lista
    }

    void eliminar() { // Método para eliminar el último elemento de la lista
        if (tamanio > 0) { // Verifica si la lista no está vacía
            tamanio--; // Decrementa el tamaño de la lista
        } else {
            std::cout << "Error: La lista está vacía." << std::endl; // Mensaje de error si la lista está vacía
        }
    }

    int obtener(int posicion) const { // Método para obtener el elemento en una posición específica
        if (posicion >= 0 && posicion < tamanio) { // Verifica si la posición es válida
            return lista[posicion]; // Devuelve el elemento en la posición especificada
        } else {
            std::cout << "Error: Posición inválida." << std::endl; // Mensaje de error si la posición es inválida
            return -1; // Devuelve un valor de error
        }
    }

    void mostrar() const { // Método para mostrar todos los elementos de la lista
        std::cout << "Elementos en la lista: "; // Imprime el mensaje inicial
        for (int i = 0; i < tamanio; i++) { // Recorre todos los elementos en la lista
            std::cout << lista[i] << " "; // Imprime cada elemento
        }
        std::cout << std::endl; // Termina la línea de salida
    }

    int obtenerTamanio() const { // Método para obtener el tamaño actual de la lista
        return tamanio; // Devuelve el número de elementos en la lista
    }
};

int main() { // Punto de entrada del programa
    ListaDinamica miLista; // Crea un objeto de tipo ListaDinamica

    miLista.agregar(10); // Agrega 10 a la lista
    miLista.agregar(20); // Agrega 20 a la lista
    miLista.agregar(30); // Agrega 30 a la lista

    miLista.mostrar(); //
