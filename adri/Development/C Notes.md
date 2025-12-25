
## **1. Configuración Inicial**

### **Herramientas necesarias:**
- **Compilador de C:**  
  - En Windows: [MinGW](https://www.mingw-w64.org/) o usar WSL.  
  - En macOS: `Xcode Command Line Tools` (`xcode-select --install`).  
  - En Linux: `gcc` (normalmente ya instalado).  
- **Editor de código:** VS Code, Sublime, Notepad++ o cualquier editor de texto.  

---

## **2. Estructura básica de un programa en C**

```c
// Incluir bibliotecas
#include <stdio.h>  // Para entrada/salida (printf, scanf)

// Función principal: punto de entrada del programa
int main() {
    // Código del programa
    
    printf("¡Hola, mundo!\n");  // Imprime en pantalla
    
    return 0;  // Indica que el programa terminó correctamente
}
```

---

## **3. Pasos para crear y ejecutar tu primer programa**

### **a. Crear el archivo**
- Crea un archivo llamado `hola_mundo.c` (extensión `.c` obligatoria).

### **b. Compilar**
Abre la terminal/consola y navega a la carpeta del archivo:
```bash
gcc hola_mundo.c -o hola_mundo
```
Esto genera un ejecutable llamado `hola_mundo` (o `hola_mundo.exe` en Windows).

### **c. Ejecutar:**
```bash
# En Linux/macOS:
./hola_mundo

# En Windows:
hola_mundo.exe
```

---

## **4. Conceptos básicos

### **Variables y tipos de datos:**
```c
int edad = 25;            // Entero
float precio = 19.99;     // Decimal
char letra = 'A';         // Carácter
char nombre[] = "Juan";   // Cadena de texto
```

### **Entrada y salida:**
```c
int numero;
printf("Introduce un número: ");
scanf("%d", &numero);     // Lee un entero
printf("El número es: %d\n", numero);
```

### **Estructuras de control:**
```c
// Condicional
if (edad >= 18) {
    printf("Mayor de edad\n");
} else {
    printf("Menor de edad\n");
}

// Bucle for
for (int i = 0; i < 5; i++) {
    printf("Iteración %d\n", i);
}
```

---

## **5. Ejemplo completo (programa interactivo)**

```c
#include <stdio.h>

int main() {
    char nombre[50];
    int edad;
    
    printf("¿Cómo te llamas? ");
    scanf("%s", nombre);
    
    printf("¿Cuántos años tienes? ");
    scanf("%d", &edad);
    
    printf("\nHola %s, tienes %d años.\n", nombre, edad);
    
    if (edad >= 18) {
        printf("Eres mayor de edad.\n");
    } else {
        printf("Eres menor de edad.\n");
    }
    
    return 0;
}
```

--- 

## **6. Declaración de Punteros**

```c
tipo *nombre_puntero;           // Declaración
tipo *nombre_puntero = NULL;    // Declaración + inicialización
```

**Ejemplos:**

```c
int *ptr_entero;
float *ptr_float;
char *ptr_char;
```

---
## **📌 Operadores Esenciales**

```c
&variable    // Dirección de memoria de la variable
*puntero     // Valor almacenado en la dirección (desreferenciar)
```

**Ejemplo:**

```c
int x = 10;
int *p = &x;    // p guarda la dirección de x
printf("%d", *p); // Imprime 10 (valor de x)
```

---

## **📌 Memoria Dinámica: Reserva**

### **malloc() - Memory Allocation**

```c
#include <stdlib.h>

// Reservar para un entero
int *p = (int*)malloc(sizeof(int));

// Reservar array de N elementos
int N = 10;
int *array = (int*)malloc(N * sizeof(int));

// ¡SIEMPRE verificar!
if (p == NULL) {
    printf("Error de memoria\n");
    exit(1);
}
```

### **calloc() - Contiguous Allocation**
```c
// Reserva e INICIALIZA a cero
int *p = (int*)calloc(5, sizeof(int));  // 5 enteros a 0
```

### **realloc() - Reallocation**
```c
// Redimensionar memoria existente
int *nuevo = (int*)realloc(p, 20 * sizeof(int));
```

---

## **📌 Memoria Dinámica: Liberación**

### **free() - Liberar Memoria**
```c
// Liberar un puntero
free(p);
p = NULL;  // ¡IMPORTANTE! Evita dangling pointer

// Para arrays 2D (liberar en orden inverso)
for(int i = 0; i < filas; i++) {
    free(matriz[i]);
}
free(matriz);
matriz = NULL;
```

---

## **📌 Errores Comunes (¡EVITAR!)**

### **1. Memory Leak (Fuga de Memoria)**
```c
// ❌ MAL
void funcion() {
    int *p = malloc(sizeof(int));
    // Olvidar free(p) -> LEAK
}

// ✅ BIEN
void funcion() {
    int *p = malloc(sizeof(int));
    // ... usar ...
    free(p);
    p = NULL;
}
```

### **2. Dangling Pointer**
```c
int *p = malloc(sizeof(int));
free(p);
*p = 10;  // ❌ PELIGRO: memoria ya liberada
p = NULL; // ✅ Solución
```

### **3. Double Free**
```c
free(p);
free(p);  // ❌ COMPORTAMIENTO INDEFINIDO
```

---

## **📌 Buenas Prácticas**

### **Patrón Seguro de Reserva/Liberación**
```c
// 1. Declarar e inicializar a NULL
int *p = NULL;

// 2. Reservar verificando
p = (int*)malloc(sizeof(int));
if (p == NULL) {
    // Manejo de error
    return;
}

// 3. Usar la memoria
*p = 100;

// 4. Liberar y anular
free(p);
p = NULL;  // ¡CRUCIAL!
```

### **Para Arrays Dinámicos**
```c
// Reserva
int n = 10;
int *arr = (int*)malloc(n * sizeof(int));

// Verificación
if (arr == NULL) {
    perror("malloc failed");
    exit(EXIT_FAILURE);
}

// Uso
for(int i = 0; i < n; i++) {
    arr[i] = i * 2;
}

// Liberación
free(arr);
arr = NULL;
```

---

## **📌 Ejemplo Completo: Gestión Segura**
```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *datos = NULL;
    int tamaño = 5;
    
    // 1. RESERVAR
    datos = (int*)malloc(tamaño * sizeof(int));
    if (datos == NULL) {
        fprintf(stderr, "Error reservando memoria\n");
        return 1;
    }
    
    // 2. USAR
    for(int i = 0; i < tamaño; i++) {
        datos[i] = (i + 1) * 10;
        printf("datos[%d] = %d\n", i, datos[i]);
    }
    
    // 3. REDIMENSIONAR
    tamaño = 10;
    int *temp = (int*)realloc(datos, tamaño * sizeof(int));
    if (temp == NULL) {
        free(datos);  // Liberar la original antes de salir
        datos = NULL;
        return 1;
    }
    datos = temp;
    
    // 4. LIBERAR
    free(datos);
    datos = NULL;
    
    printf("Memoria liberada correctamente\n");
    return 0;
}
```

---

## **📌 Herramientas de Depuración**

### **Valgrind (Linux/macOS)**
```bash
# Compilar con info de depuración
gcc -g programa.c -o programa

# Ejecutar con valgrind
valgrind --leak-check=full --show-leak-kinds=all ./programa
```

### **Comandos útiles:**
```bash
# Verificar fugas
valgrind ./programa

# Detalles completos
valgrind --leak-check=full --track-origins=yes ./programa
```

---

## **📌 Reglas Mnemotécnicas**
```
1. "A cada malloc, su free"
2. "NULL después de free"
3. "Verifica siempre el retorno de malloc"
4. "Libera en orden inverso a como reservaste"
5. "Un puntero, una responsabilidad"
```

---

## **📌 Cheatsheet Rápido**
```c
// DECLARAR
tipo *p;

// RESERVAR
p = (tipo*)malloc(cantidad * sizeof(tipo));

// VERIFICAR
if (p == NULL) { error; }

// USAR
*p = valor;
p[indice] = valor;

// LIBERAR
free(p);
p = NULL;
```

---

**📍 Nota para Obsidian:** Crea un archivo llamado `Punteros_C.md` y pega este contenido. Luego puedes enlazarlo desde tus otros apuntes usando `[[Punteros_C]]`.