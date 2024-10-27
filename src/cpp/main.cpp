#include <iostream>
#include <fstream>
#include <random>
#include <vector>
#include <iomanip>
#include <chrono>
#include <string>
#include <thread>

using Matrix = std::vector<std::vector<int>>;
using namespace std;
using namespace chrono;


//---------------------------------------Algorithms---------------------------------------

std::vector<std::vector<int>> multiplicacionNaiv(const std::vector<std::vector<int>> &A, const std::vector<std::vector<int>> &B, int n) {
    std::vector<std::vector<int>> C(n, std::vector<int>(n, 0));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            for (int k = 0; k < n; ++k)
                C[i][j] += A[i][k] * B[k][j];
    return C;
}

Matrix NaivLoopUnrollingTwo(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<int>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n / 2 * 2; k += 2) {
                C[i][j] += A[i][k] * B[k][j];
                C[i][j] += A[i][k + 1] * B[k + 1][j];
            }
            if (n % 2 != 0)  // caso impar
                C[i][j] += A[i][n - 1] * B[n - 1][j];
        }
    return C;
}

Matrix NaivLoopUnrollingFour(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<int>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n / 4 * 4; k += 4) {
                C[i][j] += A[i][k] * B[k][j];
                C[i][j] += A[i][k + 1] * B[k + 1][j];
                C[i][j] += A[i][k + 2] * B[k + 2][j];
                C[i][j] += A[i][k + 3] * B[k + 3][j];
            }
            for (int k = n / 4 * 4; k < n; k++)  // elementos restantes
                C[i][j] += A[i][k] * B[k][j];
        }
    return C;
}

Matrix WinogradOriginal(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<int>(n, 0));
    std::vector<int> rowFactor(n, 0), colFactor(n, 0);

    // Precomputar los factores de fila y columna
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            rowFactor[i] += A[i][2 * j] * A[i][2 * j + 1];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            colFactor[i] += B[2 * j][i] * B[2 * j + 1][i];

    // Calcular la matriz de salida
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
    Matrix C(n, std::vector<int>(n, 0));
    std::vector<int> rowFactor(n, 0), colFactor(n, 0);

    // Calcular factores de fila y columna con optimización de escala
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            rowFactor[i] += A[i][2 * j] * A[i][2 * j + 1];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n / 2; j++)
            colFactor[i] += B[2 * j][i] * B[2 * j + 1][i];

    // Calcular matriz de salida usando factores precomputados
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
    Matrix C(n, std::vector<int>(n, 0));
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
    Matrix C(n, std::vector<int>(n, 0));
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
    Matrix C(n, std::vector<int>(n, 0));

    for (int ii = 0; ii < n; ii += blockSize)
        for (int jj = 0; jj < n; jj += blockSize)
            for (int kk = 0; kk < n; kk += blockSize)
                multiplyBlock(A, B, C, ii, jj, kk, blockSize);

    return C;
}

Matrix IV_4_ParallelBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<int>(n, 0));
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
    Matrix C(n, std::vector<int>(n, 0));
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

std::vector<std::vector<int>> cargarMatriz(const std::string &nombreArchivo, int n) {
    std::vector<std::vector<int>> matriz(n, std::vector<int>(n));
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
    std::ofstream archivo("resultados.csv", std::ios::app);
    if (archivo.is_open()) {
        archivo << algoritmo << "," << tamanoMatriz << "," << tiempo << "\n";
        archivo.close();
    } else {
        std::cerr << "No se pudo abrir el archivo para registrar el tiempo de ejecución.\n";
    }
}

void ejecutarAlgoritmo(const std::string &algoritmo, const std::string &archivoA, const std::string &archivoB, int n) {
    auto A = cargarMatriz(archivoA, n);
    auto B = cargarMatriz(archivoB, n);

    auto inicio = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<int>> resultado;

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
        resultado = SequentialBlock(A, B, 16); // Ajusta el tamaño del bloque según sea necesario
    } else if (algoritmo == "ParallelBlock") {
        resultado = ParallelBlock(A, B, 16); // Ajusta el tamaño del bloque según sea necesario
    } else if (algoritmo == "IV_3_SequentialBlock") {
        resultado = IV_3_SequentialBlock(A, B, 16); // Ajusta el tamaño del bloque según sea necesario
    } else if (algoritmo == "IV_4_ParallelBlock") {
        resultado = IV_4_ParallelBlock(A, B, 16); // Ajusta el tamaño del bloque según sea necesario
    } else if (algoritmo == "IV_5_EnhancedParallelBlock") {
        resultado = IV_5_EnhancedParallelBlock(A, B, 16); // Ajusta el tamaño del bloque según sea necesario
    } else {
        std::cerr << "Algoritmo no reconocido: " << algoritmo << std::endl;
        return;
    }

    auto fin = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> tiempo = fin - inicio;

    registrarTiempo(algoritmo, n, tiempo.count());
}




int main() {
    const int n = 128; // Ajusta el tamaño de la matriz según lo necesites
    const std::string archivoA = "matrizA128.txt"; // Nombre del archivo para la matriz A
    const std::string archivoB = "matrizB128.txt"; // Nombre del archivo para la matriz B

    // Generar matrices de prueba (descomentar si es necesario)
    generarMatrizPrueba(n, archivoA);
    generarMatrizPrueba(n, archivoB);

    // Ejecución de todos los algoritmos
    

    return 0;
}
