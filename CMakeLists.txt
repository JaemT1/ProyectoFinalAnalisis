cmake_minimum_required(VERSION 3.29)
project(PRoyectoFinal)

# Establecer el estándar de C++
set(CMAKE_CXX_STANDARD 20)

# Configuración para vinculación estática
set(CMAKE_STATIC_LINKER_FLAGS "-static")

# Fuerza la vinculación estática de las bibliotecas estándar de C++
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++")

# Añadir el ejecutable
add_executable(PRoyectoFinal src/cpp/main.cpp
)

# Definir el directorio raíz del proyecto como una variable
add_compile_definitions(PROJECT_ROOT="${CMAKE_SOURCE_DIR}")
