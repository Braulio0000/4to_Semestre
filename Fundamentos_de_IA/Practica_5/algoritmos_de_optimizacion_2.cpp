#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <limits>
#include <iomanip>
#include <fstream>

using namespace std;

// Clase para representar una partícula
class Particle {
public:
    vector<double> position;
    vector<double> velocity;
    vector<double> best_position;
    double fitness;
    double best_fitness;
    
    Particle(int dim) {
        position.resize(dim);
        velocity.resize(dim);
        best_position.resize(dim);
        fitness = numeric_limits<double>::max();
        best_fitness = numeric_limits<double>::max();
    }
};

// Clase PSO
class PSO {
private:
    int num_particles;
    int dimensions;
    int max_iterations;
    double w;  // Inercia
    double c1; // Coeficiente cognitivo
    double c2; // Coeficiente social
    double min_bound;
    double max_bound;
    
    vector<Particle> swarm;
    vector<double> global_best_position;
    double global_best_fitness;
    
    mt19937 gen;
    uniform_real_distribution<double> rand_dist;
    
    // Función objetivo
    double (*objective_function)(const vector<double>&);
    
public:
    PSO(int n_particles, int dim, int max_iter, 
        double min_b, double max_b, 
        double (*obj_func)(const vector<double>&))
        : num_particles(n_particles), dimensions(dim), 
          max_iterations(max_iter), min_bound(min_b), 
          max_bound(max_b), objective_function(obj_func),
          gen(random_device{}()), rand_dist(0.0, 1.0) {
        
        // Parámetros estándar de PSO
        w = 0.7;   // Inercia
        c1 = 1.5;  // Coeficiente cognitivo
        c2 = 1.5;  // Coeficiente social
        
        global_best_position.resize(dim);
        global_best_fitness = numeric_limits<double>::max();
        
        initializeSwarm();
    }
    
    void initializeSwarm() {
        swarm.clear();
        
        for (int i = 0; i < num_particles; i++) {
            Particle p(dimensions);
            
            // Inicializar posición aleatoria
            for (int j = 0; j < dimensions; j++) {
                p.position[j] = min_bound + rand_dist(gen) * (max_bound - min_bound);
                p.velocity[j] = (rand_dist(gen) - 0.5) * (max_bound - min_bound) * 0.1;
                p.best_position[j] = p.position[j];
            }
            
            // Evaluar fitness inicial
            p.fitness = objective_function(p.position);
            p.best_fitness = p.fitness;
            
            // Actualizar mejor global
            if (p.fitness < global_best_fitness) {
                global_best_fitness = p.fitness;
                global_best_position = p.position;
            }
            
            swarm.push_back(p);
        }
    }
    
    void optimize() {
        ofstream convergence_file("pso_convergence.csv");
        convergence_file << "Iteration,Best_Fitness,Average_Fitness\n";
        
        for (int iter = 0; iter < max_iterations; iter++) {
            double avg_fitness = 0.0;
            
            for (auto& particle : swarm) {
                // Actualizar velocidad
                for (int j = 0; j < dimensions; j++) {
                    double r1 = rand_dist(gen);
                    double r2 = rand_dist(gen);
                    
                    double cognitive = c1 * r1 * (particle.best_position[j] - particle.position[j]);
                    double social = c2 * r2 * (global_best_position[j] - particle.position[j]);
                    
                    particle.velocity[j] = w * particle.velocity[j] + cognitive + social;
                    
                    // Limitar velocidad
                    double v_max = (max_bound - min_bound) * 0.2;
                    if (particle.velocity[j] > v_max) particle.velocity[j] = v_max;
                    if (particle.velocity[j] < -v_max) particle.velocity[j] = -v_max;
                }
                
                // Actualizar posición
                for (int j = 0; j < dimensions; j++) {
                    particle.position[j] += particle.velocity[j];
                    
                    // Mantener dentro de límites
                    if (particle.position[j] > max_bound) particle.position[j] = max_bound;
                    if (particle.position[j] < min_bound) particle.position[j] = min_bound;
                }
                
                // Evaluar nueva posición
                particle.fitness = objective_function(particle.position);
                avg_fitness += particle.fitness;
                
                // Actualizar mejor personal
                if (particle.fitness < particle.best_fitness) {
                    particle.best_fitness = particle.fitness;
                    particle.best_position = particle.position;
                }
                
                // Actualizar mejor global
                if (particle.fitness < global_best_fitness) {
                    global_best_fitness = particle.fitness;
                    global_best_position = particle.position;
                }
            }
            
            avg_fitness /= num_particles;
            
            // Guardar convergencia
            convergence_file << iter << "," << global_best_fitness << "," << avg_fitness << "\n";
            
            // Mostrar progreso cada 10 iteraciones
            if (iter % 10 == 0) {
                cout << "Iter " << iter << " - Best Fitness: " << scientific 
                     << setprecision(6) << global_best_fitness << endl;
            }
        }
        
        convergence_file.close();
    }
    
    void printResults() {
        cout << "\n=== RESULTADOS FINALES ===" << endl;
        cout << "Mejor fitness encontrado: " << scientific << setprecision(10) 
             << global_best_fitness << endl;
        cout << "Posicion optima encontrada:" << endl;
        for (int i = 0; i < dimensions; i++) {
            cout << "  x[" << i << "] = " << fixed << setprecision(6) 
                 << global_best_position[i] << endl;
        }
    }
    
    // Métodos para ajustar parámetros
    void setInertia(double inertia) { w = inertia; }
    void setCognitive(double cognitive) { c1 = cognitive; }
    void setSocial(double social) { c2 = social; }
};

// ==================== FUNCIONES DE PRUEBA ====================

// 1. Función Sphere (Mínimo global en 0,0,...,0 con f=0)
double sphere(const vector<double>& x) {
    double sum = 0.0;
    for (double xi : x) {
        sum += xi * xi;
    }
    return sum;
}

// 2. Función Rastrigin (Mínimo global en 0,0,...,0 con f=0)
double rastrigin(const vector<double>& x) {
    double sum = 10.0 * x.size();
    for (double xi : x) {
        sum += xi * xi - 10.0 * cos(2.0 * M_PI * xi);
    }
    return sum;
}

// 3. Función Rosenbrock (Mínimo global en 1,1,...,1 con f=0)
double rosenbrock(const vector<double>& x) {
    double sum = 0.0;
    for (size_t i = 0; i < x.size() - 1; i++) {
        sum += 100.0 * pow(x[i+1] - x[i]*x[i], 2) + pow(1 - x[i], 2);
    }
    return sum;
}

// 4. Función Ackley (Mínimo global en 0,0,...,0 con f=0)
double ackley(const vector<double>& x) {
    double sum1 = 0.0, sum2 = 0.0;
    int n = x.size();
    
    for (double xi : x) {
        sum1 += xi * xi;
        sum2 += cos(2.0 * M_PI * xi);
    }
    
    return -20.0 * exp(-0.2 * sqrt(sum1 / n)) - exp(sum2 / n) + 20.0 + M_E;
}

// 5. Función Griewank (Mínimo global en 0,0,...,0 con f=0)
double griewank(const vector<double>& x) {
    double sum = 0.0;
    double prod = 1.0;
    
    for (size_t i = 0; i < x.size(); i++) {
        sum += x[i] * x[i] / 4000.0;
        prod *= cos(x[i] / sqrt(i + 1.0));
    }
    
    return sum - prod + 1.0;
}

// 6. Función Beale (2D) (Mínimo en (3, 0.5) con f=0)
double beale(const vector<double>& x) {
    double x1 = x[0], x2 = x[1];
    double term1 = pow(1.5 - x1 + x1*x2, 2);
    double term2 = pow(2.25 - x1 + x1*x2*x2, 2);
    double term3 = pow(2.625 - x1 + x1*x2*x2*x2, 2);
    return term1 + term2 + term3;
}

// ==================== MAIN ====================
int main() {
    cout << "=== PARTICLE SWARM OPTIMIZATION ===" << endl;
    cout << "Optimizacion por Enjambre de Particulas\n" << endl;
    
    // Configuración
    int num_particles = 30;
    int dimensions = 2;
    int max_iterations = 100;
    
    // Menú de funciones
    cout << "Seleccione la funcion a optimizar:" << endl;
    cout << "1. Sphere" << endl;
    cout << "2. Rastrigin" << endl;
    cout << "3. Rosenbrock" << endl;
    cout << "4. Ackley" << endl;
    cout << "5. Griewank" << endl;
    cout << "6. Beale" << endl;
    
    int choice;
    cout << "\nOpcion: ";
    cin >> choice;
    
    double (*func)(const vector<double>&);
    double min_bound, max_bound;
    string func_name;
    
    switch(choice) {
        case 1:
            func = sphere;
            min_bound = -5.0;
            max_bound = 5.0;
            func_name = "Sphere";
            break;
        case 2:
            func = rastrigin;
            min_bound = -5.12;
            max_bound = 5.12;
            func_name = "Rastrigin";
            break;
        case 3:
            func = rosenbrock;
            min_bound = -5.0;
            max_bound = 10.0;
            func_name = "Rosenbrock";
            break;
        case 4:
            func = ackley;
            min_bound = -5.0;
            max_bound = 5.0;
            func_name = "Ackley";
            break;
        case 5:
            func = griewank;
            min_bound = -600.0;
            max_bound = 600.0;
            func_name = "Griewank";
            break;
        case 6:
            func = beale;
            min_bound = -4.5;
            max_bound = 4.5;
            func_name = "Beale";
            break;
        default:
            cout << "Opcion invalida. Usando Sphere por defecto." << endl;
            func = sphere;
            min_bound = -5.0;
            max_bound = 5.0;
            func_name = "Sphere";
    }
    
    cout << "\nOptimizando funcion " << func_name << "..." << endl;
    
    // Crear y ejecutar PSO
    PSO pso(num_particles, dimensions, max_iterations, min_bound, max_bound, func);
    
    // Opciones de configuración avanzada
    cout << "\nDesea usar parametros personalizados? (1=Si, 0=No): ";
    int custom;
    cin >> custom;
    
    if (custom == 1) {
        double w, c1, c2;
        cout << "Inercia (w): ";
        cin >> w;
        cout << "Coeficiente cognitivo (c1): ";
        cin >> c1;
        cout << "Coeficiente social (c2): ";
        cin >> c2;
        
        pso.setInertia(w);
        pso.setCognitive(c1);
        pso.setSocial(c2);
    }
    
    cout << "\nIniciando optimizacion..." << endl;
    cout << "Particulas: " << num_particles << endl;
    cout << "Dimensiones: " << dimensions << endl;
    cout << "Iteraciones: " << max_iterations << endl;
    cout << "Limites: [" << min_bound << ", " << max_bound << "]\n" << endl;
    
    pso.optimize();
    pso.printResults();
    
    cout << "\nDatos de convergencia guardados en 'pso_convergence.csv'" << endl;
    
    return 0;
}