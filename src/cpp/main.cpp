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
#include <cmath>
#include <climits>

using Matrix = std::vector<std::vector<long long>>;
using namespace std;
using namespace chrono;


//---------------------------------------Algorithms---------------------------------------


Matrix multiplicacionNaiv(const Matrix& A, const Matrix& B, int n)
{
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            for (int k = 0; k < n; ++k)
                C[i][j] += A[i][k] * B[k][j];
    return C;
}

Matrix NaivLoopUnrollingTwo(const Matrix& A, const Matrix& B)
{
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
        {
            for (int k = 0; k < n / 2 * 2; k += 2)
            {
                C[i][j] += A[i][k] * B[k][j];
                C[i][j] += A[i][k + 1] * B[k + 1][j];
            }
            if (n % 2 != 0)
                C[i][j] += A[i][n - 1] * B[n - 1][j];
        }
    return C;
}

Matrix NaivLoopUnrollingFour(const Matrix& A, const Matrix& B)
{
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
        {
            for (int k = 0; k < n / 4 * 4; k += 4)
            {
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

#include <vector>

using Matrix = std::vector<std::vector<long long>>;

// Implementación de WinogradOriginal manteniendo la lógica original
Matrix WinogradOriginal(const Matrix& A, const Matrix& B) {
    int N = A.size();  // Asumimos que A y B son matrices cuadradas de tamaño N x N
    Matrix Result(N, std::vector<long long>(N, 0));
    std::vector<long long> y(N, 0), z(N, 0);
    long long aux;

    // Calcular el vector y (suma auxiliar para las filas de A)
    for (int i = 0; i < N; i++) {
        aux = 0;
        for (int j = 0; j < N - 1; j += 2) {
            aux += A[i][j] * A[i][j + 1];
        }
        y[i] = aux;
    }

    // Calcular el vector z (suma auxiliar para las columnas de B)
    for (int i = 0; i < N; i++) {
        aux = 0;
        for (int j = 0; j < N - 1; j += 2) {
            aux += B[j][i] * B[j + 1][i];
        }
        z[i] = aux;
    }

    // Calcular la matriz Result usando los factores auxiliares y, z
    for (int i = 0; i < N; i++) {
        for (int k = 0; k < N; k++) {
            aux = 0;
            for (int j = 0; j < N - 1; j += 2) {
                aux += (A[i][j] + B[j + 1][k]) * (A[i][j + 1] + B[j][k]);
            }
            Result[i][k] = aux - y[i] - z[k];

            // Si N es impar, se necesita un ajuste adicional
            if (N % 2 == 1) {
                Result[i][k] += A[i][N - 1] * B[N - 1][k];
            }
        }
    }

    return Result;
}

// Función para sumar dos matrices
Matrix add(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            C[i][j] = A[i][j] + B[i][j];
    return C;
}

// Función para restar dos matrices
Matrix subtract(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            C[i][j] = A[i][j] - B[i][j];
    return C;
}

// Algoritmo de Strassen
Matrix Strassen(const Matrix& A, const Matrix& B) {
    int n = A.size();
    if (n == 1) {
        return {{A[0][0] * B[0][0]}};
    }

    int newSize = n / 2;

    // Crear submatrices
    Matrix A11(newSize, std::vector<long long>(newSize));
    Matrix A12(newSize, std::vector<long long>(newSize));
    Matrix A21(newSize, std::vector<long long>(newSize));
    Matrix A22(newSize, std::vector<long long>(newSize));

    Matrix B11(newSize, std::vector<long long>(newSize));
    Matrix B12(newSize, std::vector<long long>(newSize));
    Matrix B21(newSize, std::vector<long long>(newSize));
    Matrix B22(newSize, std::vector<long long>(newSize));

    // Dividir matrices A y B en submatrices
    for (int i = 0; i < newSize; i++) {
        for (int j = 0; j < newSize; j++) {
            A11[i][j] = A[i][j];
            A12[i][j] = A[i][j + newSize];
            A21[i][j] = A[i + newSize][j];
            A22[i][j] = A[i + newSize][j + newSize];

            B11[i][j] = B[i][j];
            B12[i][j] = B[i][j + newSize];
            B21[i][j] = B[i + newSize][j];
            B22[i][j] = B[i + newSize][j + newSize];
        }
    }

    // Calcular los productos intermedios de Strassen
    Matrix M1 = Strassen(add(A11, A22), add(B11, B22));
    Matrix M2 = Strassen(add(A21, A22), B11);
    Matrix M3 = Strassen(A11, subtract(B12, B22));
    Matrix M4 = Strassen(A22, subtract(B21, B11));
    Matrix M5 = Strassen(add(A11, A12), B22);
    Matrix M6 = Strassen(subtract(A21, A11), add(B11, B12));
    Matrix M7 = Strassen(subtract(A12, A22), add(B21, B22));

    // Combinar los productos intermedios para obtener las submatrices de C
    Matrix C11 = add(subtract(add(M1, M4), M5), M7);
    Matrix C12 = add(M3, M5);
    Matrix C21 = add(M2, M4);
    Matrix C22 = add(subtract(add(M1, M3), M2), M6);

    // Combinar submatrices en la matriz resultado
    Matrix C(n, std::vector<long long>(n));
    for (int i = 0; i < newSize; i++) {
        for (int j = 0; j < newSize; j++) {
            C[i][j] = C11[i][j];
            C[i][j + newSize] = C12[i][j];
            C[i + newSize][j] = C21[i][j];
            C[i + newSize][j + newSize] = C22[i][j];
        }
    }

    return C;
}

Matrix III_3_SequentialBlock(const Matrix& A, const Matrix& B, int blockSize)
{
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

void multiplyBlock(const Matrix& A, const Matrix& B, Matrix& C, int ii, int jj, int kk, int blockSize)
{
    int n = A.size();
    for (int i = ii; i < std::min(ii + blockSize, n); i++)
        for (int j = jj; j < std::min(jj + blockSize, n); j++)
            for (int k = kk; k < std::min(kk + blockSize, n); k++)
                C[i][j] += A[i][k] * B[k][j];
}

Matrix III_4_ParallelBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));

    // Paralelización de los bucles principales utilizando OpenMP
#pragma omp parallel for collapse(2) // Paraleliza las dos primeras dimensiones ii y jj
    for (int ii = 0; ii < n; ii += blockSize) {
        for (int jj = 0; jj < n; jj += blockSize) {
            // Aquí, paralelizamos el bucle más interno (el cálculo real de la multiplicación)
#pragma omp parallel for collapse(2) // Paraleliza las iteraciones i y j
            for (int i = ii; i < std::min(ii + blockSize, n); i++) {
                for (int j = jj; j < std::min(jj + blockSize, n); j++) {
                    // Usamos un bucle separado para el cálculo de la multiplicación de bloques
                    for (int k = 0; k < n; k++) {
                        C[i][j] += A[i][k] * B[k][j];
                    }
                }
            }
        }
    }

    return C;
}

Matrix IV_3_SequentialBlock(const Matrix& A, const Matrix& B, int blockSize)
{
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));

    // Convertimos las matrices A y B a matrices planas para mejorar el acceso a memoria
    std::vector<long long> A_flat(n * n), B_flat(n * n);

    // Llenamos las matrices planas A_flat y B_flat
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            A_flat[i * n + j] = A[i][j];
            B_flat[i * n + j] = B[i][j];
        }
    }

    for (int ii = 0; ii < n; ii += blockSize) {
        for (int jj = 0; jj < n; jj += blockSize) {
            for (int kk = 0; kk < n; kk += blockSize) {
                // Definimos los límites de los bloques
                int ii_end = std::min(ii + blockSize, n);
                int jj_end = std::min(jj + blockSize, n);
                int kk_end = std::min(kk + blockSize, n);

                // Multiplicación de bloques optimizada
                for (int i = ii; i < ii_end; ++i) {
                    for (int j = jj; j < jj_end; ++j) {
                        long long sum = 0;
                        for (int k = kk; k < kk_end; ++k) {
                            sum += A_flat[i * n + k] * B_flat[k * n + j];
                        }
                        C[i][j] += sum;  // Sumamos directamente en C
                    }
                }
            }
        }
    }

    return C;
}

Matrix IV_4_ParallelBlock(const Matrix& A, const Matrix& B, int blockSize) {
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));

    // Convertimos las matrices A y B a matrices planas para mejorar el acceso a memoria
    std::vector<long long> A_flat(n * n), B_flat(n * n);

    // Llenamos las matrices planas A_flat y B_flat
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            A_flat[i * n + j] = A[i][j];
            B_flat[i * n + j] = B[i][j];
        }
    }

    // Paralelización de los bucles principales utilizando OpenMP
#pragma omp parallel for collapse(2) // Paraleliza las dos primeras dimensiones ii y jj
    for (int ii = 0; ii < n; ii += blockSize) {
        for (int jj = 0; jj < n; jj += blockSize) {
            // Precalculamos los límites de los bloques
            int ii_end = std::min(ii + blockSize, n);
            int jj_end = std::min(jj + blockSize, n);

            // Multiplicación de bloques optimizada con OpenMP
            for (int kk = 0; kk < n; kk += blockSize) {
                int kk_end = std::min(kk + blockSize, n);

                // Paralelización de la multiplicación de bloques
#pragma omp parallel for collapse(2) // Paraleliza las iteraciones i y j dentro del bloque
                for (int i = ii; i < ii_end; ++i) {
                    for (int j = jj; j < jj_end; ++j) {
                        long long sum = 0;
                        // Calculamos la multiplicación de bloques
                        for (int k = kk; k < kk_end; ++k) {
                            sum += A_flat[i * n + k] * B_flat[k * n + j];
                        }
#pragma omp atomic
                        C[i][j] += sum;  // Asegura que la actualización de C sea atómica
                    }
                }
            }
        }
    }

    return C;
}



Matrix IV_5_EnhancedParallelBlock(const Matrix& A, const Matrix& B, int blockSize)
{
    int n = A.size();
    Matrix C(n, std::vector<long long>(n, 0));
    std::vector<std::thread> threads;
    int maxThreads = std::thread::hardware_concurrency(); // Número máximo de hilos disponibles

    auto worker = [&](int threadId)
    {
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
void generarMatrizPrueba(int n, const std::string& nombreArchivo)
{
    // Crear el directorio para guardar las matrices de prueba si no existe
    std::filesystem::create_directories("../src/data/test_cases");

    std::ofstream archivo(nombreArchivo);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(100000, 999999);

    if (archivo.is_open())
    {
        for (int i = 0; i < n; ++i)
        {
            for (int j = 0; j < n; ++j)
            {
                archivo << dist(gen) << " ";
            }
            archivo << "\n";
        }
        archivo.close();
    }
    else
    {
        std::cerr << "No se pudo abrir el archivo para escribir la matriz.\n";
    }
}

std::vector<std::vector<long long>> cargarMatriz(const std::string& nombreArchivo, int n)
{
    std::vector<std::vector<long long>> matriz(n, std::vector<long long>(n));
    std::ifstream archivo(nombreArchivo);

    if (archivo.is_open())
    {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                archivo >> matriz[i][j];
        archivo.close();
    }
    else
    {
        std::cerr << "No se pudo abrir el archivo para leer la matriz.\n";
    }
    return matriz;
}


void registrarTiempo(const std::string& algoritmo, int tamanoMatriz, double tiempo)
{
    // Establecer la ruta relativa desde el directorio de trabajo actual
    std::string ruta = "../src/data/results/times/resultadosC++_n" + std::to_string(tamanoMatriz) + ".csv";

    // Crear el directorio si no existe
    std::filesystem::create_directories("../src/data/results");

    // Intentar abrir el archivo en modo de agregar
    std::ofstream archivo(ruta, std::ios::app);
    if (archivo.is_open())
    {
        archivo << algoritmo << "," << tamanoMatriz << "," << tiempo << "\n";
        archivo.close();
    }
    else
    {
        std::cerr << "No se pudo abrir el archivo para registrar el tiempo de ejecución.\n";
    }
}

void agregarEncabezadoSiEsNecesario(const std::string& ruta)
{
    // Comprobación de si el archivo ya contiene datos
    std::ifstream archivoLectura(ruta);
    bool archivoVacio = archivoLectura.peek() == std::ifstream::traits_type::eof();
    archivoLectura.close();

    // Si el archivo está vacío, agregamos el encabezado
    if (archivoVacio)
    {
        std::ofstream archivoEscritura(ruta);
        if (archivoEscritura.is_open())
        {
            archivoEscritura << "Algoritmo,Tamaño,Tiempo(s)\n";
            archivoEscritura.close();
        }
        else
        {
            std::cerr << "No se pudo abrir el archivo para escribir el encabezado.\n";
        }
    }
}

// Función auxiliar para extraer el algoritmo del nombre del archivo
std::string extraerAlgoritmo(const std::string& nombreArchivo)
{
    // Buscar la posición de "resultado_" y "_n"
    size_t inicio = nombreArchivo.find("resultado_") + 10; // Longitud de "resultado_"
    size_t fin = nombreArchivo.find("_n");

    // Extraer la parte que corresponde al algoritmo
    if (inicio != std::string::npos && fin != std::string::npos && fin > inicio) {
        return nombreArchivo.substr(inicio, fin - inicio);
    }

    // Si no se encuentra el formato esperado, devolver un identificador genérico
    return "Desconocido";
}

// Función para guardar resultados en la carpeta correspondiente al algoritmo
void guardarResultadoEnArchivo(const std::vector<std::vector<long long>>& matriz, const std::string& nombreArchivo)
{
    // Extraer el algoritmo del nombre del archivo
    std::string algoritmo = extraerAlgoritmo(nombreArchivo);

    // Crear el directorio específico para el algoritmo si no existe
    std::string rutaDirectorio = "../src/data/results/matrices/" + algoritmo;
    std::filesystem::create_directories(rutaDirectorio);

    // Generar la ruta completa del archivo dentro del directorio del algoritmo
    std::string rutaArchivo = rutaDirectorio + "/" + nombreArchivo.substr(nombreArchivo.find_last_of("/\\") + 1);

    // Abrir archivo en modo sobrescritura
    std::ofstream archivo(rutaArchivo, std::ios::out | std::ios::trunc);
    if (archivo.is_open())
    {
        // Escribir la matriz en el archivo
        for (const auto& fila : matriz)
        {
            for (const auto& valor : fila)
            {
                archivo << valor << " ";
            }
            archivo << "\n";
        }
        archivo.close(); // Cerrar el archivo después de escribir
    }
    else
    {
        // Mensaje de error si no se puede abrir el archivo
        std::cerr << "No se pudo abrir el archivo para escribir el resultado de la matriz.\n";
    }
}

void ejecutarAlgoritmo(const std::string& algoritmo, const std::string& archivoA, const std::string& archivoB, int n)
{
    auto A = cargarMatriz(archivoA, n);
    auto B = cargarMatriz(archivoB, n);

    auto inicio = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<long long>> resultado;

    if (algoritmo == "Naiv")
    {
        resultado = multiplicacionNaiv(A, B, n);
    }
    else if (algoritmo == "LoopUnrollingTwo")
    {
        resultado = NaivLoopUnrollingTwo(A, B);
    }
    else if (algoritmo == "LoopUnrollingFour")
    {
        resultado = NaivLoopUnrollingFour(A, B);
    }
    else if (algoritmo == "WinogradOriginal")
    {
        resultado = WinogradOriginal(A, B);
    }
    else if (algoritmo == "Strassen")
    {
        resultado = Strassen(A, B);
    }
    else if (algoritmo == "III_3_SequentialBlock")
    {
        resultado = III_3_SequentialBlock(A, B, 2);
    }
    else if (algoritmo == "III_4_ParallelBlock")
    {
        resultado = III_4_ParallelBlock(A, B, 2);
    }
    else if (algoritmo == "IV_3_SequentialBlock")
    {
        resultado = IV_3_SequentialBlock(A, B, 2);
    }
    else if (algoritmo == "IV_4_ParallelBlock")
    {
        resultado = IV_4_ParallelBlock(A, B, 2);
    }
    else if (algoritmo == "IV_5_EnhancedParallelBlock")
    {
        resultado = IV_5_EnhancedParallelBlock(A, B, 2);
    }
    else
    {
        std::cerr << "Algoritmo no reconocido: " << algoritmo << std::endl;
        return;
    }

    auto fin = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> tiempo = fin - inicio;

    registrarTiempo(algoritmo, n, tiempo.count());

    // Generar el nombre del archivo de resultado
    std::string nombreArchivoResultado = "../src/data/results/matrices/resultado_" + algoritmo + "_n" +
        std::to_string(n) + ".txt";
    guardarResultadoEnArchivo(resultado, nombreArchivoResultado);
}

int main()
{
    for (int i = 1; i < 9; i++)
    {
        const int n = pow(2, i); // Tamaño de la matriz (ajustable)
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
        ejecutarAlgoritmo("Strassen", archivoA, archivoB,n);
        ejecutarAlgoritmo("III_3_SequentialBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("III_4_ParallelBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("IV_3_SequentialBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("IV_4_ParallelBlock", archivoA, archivoB, n);
        ejecutarAlgoritmo("IV_5_EnhancedParallelBlock", archivoA, archivoB, n);

        std::cout << "Ejecucion de los algoritmos en C++ para tamano " << n << "*" << n << " completada\n";
    }

    return 0;
}
