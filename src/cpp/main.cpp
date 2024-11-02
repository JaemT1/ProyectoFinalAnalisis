#include <iostream>
#include <fstream>
#include <random>
#include <vector>
#include <iomanip>
#include <chrono>
#include <string>
#include <thread>
#include <filesystem>
#include <algorithm>

using Matrix = std::vector<std::vector<long long>>;
using namespace std;
using namespace chrono;


//---------------------------------------Algorithms---------------------------------------


Matrix multiplicacionNaiv(const Matrix &A, const Matrix &B, int n) {
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            for (int k = 0; k < n; ++k)
                C[i][j] += A[i][k] * B[k][j];
    return C;
}

Matrix NaivLoopUnrollingTwo(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n / 2 * 2; k += 2) {
                C[i][j] += A[i][k] * B[k][j];
                C[i][j] += A[i][k + 1] * B[k + 1][j];
            }
            if (n % 2 != 0)
                C[i][j] += A[i][n - 1] * B[n - 1][j];
        }
    return C;
}

Matrix NaivLoopUnrollingFour(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n / 4 * 4; k += 4) {
                C[i][j] += A[i][k] * B[k][j];
                C[i][j] += A[i][k + 1] * B[k + 1][j];
                C[i][j] += A[i][k + 2] * B[k + 2][j];
                C[i][j] += A[i][k + 3] * B[k + 3][j];
            }
            for (int k = n / 4 * 4; k < n; k++)
                C[i][j] += A[i][k] * B[k][j];
        }
    return C;
}

Matrix WinogradOriginal(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    std::vector<long long> rowFactor(n, 0), colFactor(n, 0);

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            rowFactor[i] += A[i][2 * j] * A[i][2 * j + 1];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            colFactor[i] += B[2 * j][i] * B[2 * j + 1][i];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            C[i][j] = -rowFactor[i] - colFactor[j];
            for (int k = 0; k < n / 2; k++)
                C[i][j] += (A[i][2 * k] + B[2 * k + 1][j]) * (A[i][2 * k + 1] + B[2 * k][j]);
            if (n % 2 == 1)
                C[i][j] += A[i][n - 1] * B[n - 1][j];
        }
    return C;
}

Matrix WinogradScaled(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    std::vector<long long> rowFactor(n, 0), colFactor(n, 0);

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            rowFactor[i] += A[i][2 * j] * A[i][2 * j + 1];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            colFactor[i] += B[2 * j][i] * B[2 * j + 1][i];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            C[i][j] = -rowFactor[i] - colFactor[j];
            for (int k = 0; k < n / 2; k++)
                C[i][j] += (A[i][2 * k] + B[2 * k + 1][j]) * (A[i][2 * k + 1] + B[2 * k][j]);
            if (n % 2 == 1)
                C[i][j] += A[i][n - 1] * B[n - 1][j];
        }
    return C;
}

Matrix SequentialBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    for (int ii = 0; ii < n; ii += blockSize)
        for (int jj = 0; jj < n; jj += blockSize)
            for (int kk = 0; kk < n; kk += blockSize)
                for (int i = ii; i < std::min(ii + blockSize, n); i++)
                    for (int j = jj; j < std::min(jj + blockSize, n); j++)
                        for (int k = kk; k < std::min(kk + blockSize, n); k++)
                            C[i][j] += A[i][k] * B[k][j];
    return C;
}

void multiplyBlock(const Matrix& A, const Matrix& B, Matrix& C, int ii, int jj, int kk, int blockSize) {
    int n = A.size();
    for (int i = ii; i < std::min(ii + blockSize, n); i++)
        for (int j = jj; j < std::min(jj + blockSize, n); j++)
            for (int k = kk; k < std::min(kk + blockSize, n); k++)
                C[i][j] += A[i][k] * B[k][j];
}

Matrix ParallelBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    std::vector<std::thread> threads;

    for (int ii = 0; ii < n; ii += blockSize)
        for (int jj = 0; jj < n; jj += blockSize)
            for (int kk = 0; kk < n; kk += blockSize)
                threads.emplace_back(multiplyBlock, std::cref(A), std::cref(B), std::ref(C), ii, jj, kk, blockSize);

    for (auto& t : threads) t.join();
    return C;
}

Matrix IV_3_SequentialBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));

    for (int ii = 0; ii < n; ii += blockSize)
        for (int jj = 0; jj < n; jj += blockSize)
            for (int kk = 0; kk < n; kk += blockSize)
                multiplyBlock(A, B, C, ii, jj, kk, blockSize);

    return C;
}

Matrix IV_4_ParallelBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    std::vector<std::thread> threads;

    for (int ii = 0; ii < n; ii += blockSize)
        for (int jj = 0; jj < n; jj += blockSize)
            for (int kk = 0; kk < n; kk += blockSize)
                threads.emplace_back(multiplyBlock, std::cref(A), std::cref(B), std::ref(C), ii, jj, kk, blockSize);

    for (auto& t : threads) t.join();
    return C;
}


Matrix IV_5_EnhancedParallelBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    std::vector<std::thread> threads;
    int maxThreads = std::thread::hardware_concurrency();  // Número máximo de hilos disponibles

    auto worker = [&](int threadId) {
        for (int ii = threadId * blockSize; ii < n; ii += blockSize * maxThreads)
            for (int jj = 0; jj < n; jj += blockSize)
                for (int kk = 0; kk < n; kk += blockSize)
                    multiplyBlock(A, B, C, ii, jj, kk, blockSize);
    };

    for (int t = 0; t < maxThreads; ++t)
        threads.emplace_back(worker, t);

    for (auto& t : threads) t.join();
    return C;
}

//---------------------------------------Utils---------------------------------------
void generarMatrizPrueba(int n, const std::string &nombreArchivo) {
    // Crear el directorio para guardar las matrices de prueba si no existe
    std::filesystem::create_directories("../src/data/test_cases");

    std::ofstream archivo(nombreArchivo);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(100000, 999999);

    if (archivo.is_open()) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                archivo << dist(gen) << " ";
            }
            archivo << "\n";
        }
        archivo.close();
    } else {
        std::cerr << "No se pudo abrir el archivo para escribir la matriz.\n";
    }
}

std::vector<std::vector<long long>> cargarMatriz(const std::string &nombreArchivo, int n) {
    std::vector<std::vector<long long>> matriz(n, std::vector<long long>(n));
    std::ifstream archivo(nombreArchivo);

    if (archivo.is_open()) {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                archivo >> matriz[i][j];
        archivo.close();
    } else {
        std::cerr << "No se pudo abrir el archivo para leer la matriz.\n";
    }
    return matriz;
}


void registrarTiempo(const std::string &algoritmo, int tamanoMatriz, double tiempo) {
    // Establecer la ruta relativa desde el directorio de trabajo actual
    std::string ruta = "../src/data/results/times/resultadosC++_n" + std::to_string(tamanoMatriz) + ".csv";

    // Crear el directorio si no existe
    std::filesystem::create_directories("../src/data/results");

    // Intentar abrir el archivo en modo de agregar
    std::ofstream archivo(ruta, std::ios::app);
    if (archivo.is_open()) {
        archivo << algoritmo << "," << tamanoMatriz << "," << tiempo << "\n";
        archivo.close();
    } else {
        std::cerr << "No se pudo abrir el archivo para registrar el tiempo de ejecución.\n";
    }
}

void agregarEncabezadoSiEsNecesario(const std::string &ruta) {
    // Comprobación de si el archivo ya contiene datos
    std::ifstream archivoLectura(ruta);
    bool archivoVacio = archivoLectura.peek() == std::ifstream::traits_type::eof();
    archivoLectura.close();

    // Si el archivo está vacío, agregamos el encabezado
    if (archivoVacio) {
        std::ofstream archivoEscritura(ruta);
        if (archivoEscritura.is_open()) {
            archivoEscritura << "Algoritmo,Tamaño,Tiempo(s)\n";
            archivoEscritura.close();
        } else {
            std::cerr << "No se pudo abrir el archivo para escribir el encabezado.\n";
        }
    }
}

void guardarResultadoEnArchivo(const std::vector<std::vector<long long>> &matriz, const std::string &nombreArchivo) {
    // Crear el directorio para los resultados de matrices si no existe
    std::filesystem::create_directories("../src/data/results/matrices");

    std::ofstream archivo(nombreArchivo);
    if (archivo.is_open()) {
        for (const auto &fila : matriz) {
            for (const auto &valor : fila) {
                archivo << valor << " ";
            }
            archivo << "\n";
        }
        archivo.close();
    } else {
        std::cerr << "No se pudo abrir el archivo para escribir el resultado de la matriz.\n";
    }
}

void ejecutarAlgoritmo(const std::string &algoritmo, const std::string &archivoA, const std::string &archivoB, int n) {
    auto A = cargarMatriz(archivoA, n);
    auto B = cargarMatriz(archivoB, n);

    auto inicio = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<long long>> resultado;

    if (algoritmo == "Naiv") {
        resultado = multiplicacionNaiv(A, B, n);
    } else if (algoritmo == "LoopUnrollingTwo") {
        resultado = NaivLoopUnrollingTwo(A, B);
    } else if (algoritmo == "LoopUnrollingFour") {
        resultado = NaivLoopUnrollingFour(A, B);
    } else if (algoritmo == "WinogradOriginal") {
        resultado = WinogradOriginal(A, B);
    } else if (algoritmo == "WinogradScaled") {
        resultado = WinogradScaled(A, B);
    } else if (algoritmo == "SequentialBlock") {
        resultado = SequentialBlock(A, B, 16);
    } else if (algoritmo == "ParallelBlock") {
        resultado = ParallelBlock(A, B, 16);
    } else if (algoritmo == "IV_3_SequentialBlock") {
        resultado = IV_3_SequentialBlock(A, B, 16);
    } else if (algoritmo == "IV_4_ParallelBlock") {
        resultado = IV_4_ParallelBlock(A, B, 16);
    } else if (algoritmo == "IV_5_EnhancedParallelBlock") {
        resultado = IV_5_EnhancedParallelBlock(A, B, 16);
    } else {
        std::cerr << "Algoritmo no reconocido: " << algoritmo << std::endl;
        return;
    }

    auto fin = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> tiempo = fin - inicio;

    registrarTiempo(algoritmo, n, tiempo.count());

    // Generar el nombre del archivo de resultado
    std::string nombreArchivoResultado = "../src/data/results/matrices/resultado_" + algoritmo + "_n" + std::to_string(n) + ".txt";
    guardarResultadoEnArchivo(resultado, nombreArchivoResultado);
}

int main() {
    for(int i = 1; i < 9; i++) {
        const int n = pow(2,i);  // Tamaño de la matriz (ajustable)
        const std::string archivoA = "../src/data/test_cases/matrizA" + std::to_string(n) + ".txt";
        const std::string archivoB = "../src/data/test_cases/matrizB" + std::to_string(n) + ".txt";
        std::string rutaCSV = "../src/data/results/times/resultadosC++_n" + std::to_string(n) + ".csv";

        // Generación de matrices de prueba si aún no existen
        //if (!std::ifstream(archivoA)) generarMatrizPrueba(n, archivoA);
        //if (!std::ifstream(archivoB)) generarMatrizPrueba(n, archivoB);

        std::string ruta = "../src/data/results/times/resultadosC++_n" + std::to_string(n) + ".csv";
        std::ofstream archivo(ruta, std::ios::trunc);
        archivo << "";
        archivo.close();

        // Agregar el encabezado si el archivo está vacío
        agregarEncabezadoSiEsNecesario(rutaCSV);

        // Ejecución de los algoritmos y medición de tiempo
        ejecutarAlgoritmo("Naiv", archivoA, archivoB, n);
        ejecutarAlgoritmo("LoopUnrollingTwo", archivoA, archivoB, n);
        ejecutarAlgoritmo("LoopUnrollingFour", archivoA, archivoB, n);
        ejecutarAlgoritmo("WinogradOriginal", archivoA, archivoB, n);
        ejecutarAlgoritmo("WinogradScaled", archivoA, archivoB, n);
        ejecutarAlgoritmo("SequentialBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("ParallelBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("IV_3_SequentialBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("IV_4_ParallelBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("IV_5_EnhancedParallelBlock", archivoA, archivoB, n);

        std::cout << "Ejecución de algoritmos completada. Resultados guardados en resultados.csv\n";
    }

    return 0;
}