





##  Tailwind CSS  

##### ¿Qué es el CSS atómico?

Antes de adentrarnos en Tailwind CSS, vamos a entender qué es Atomic CSS. Según [CSS Tricks](https://css-tricks.com/lets-define-exactly-atomic-css/)

> [!note]
> *__"__CSS atómico es el enfoque de la arquitectura CSS que favorece las clases pequeñas y de propósito único con nombres basados en la función visual.__"__*

Es como hacer clases que se *supone* que tienen un único propósito. Por ejemplo, hagamos una clase `bg-blue` con el siguiente CSS:

```css
.bg-blue {
  background-color: rgb(81, 191, 255);
}

```

Esta clase si se queda asi seguiria la arquitectura que favorece las clases pequeñas y de proposito unico. 

**Una clase unicamente tiene el css para lo que su nombre indica que va ha hacer.**


###  ¿Qué es Tailwind?

**Tailwind es una librería de estilos que te permite separar y agilizar el diseño web .**

Según su propio sitio web, es un "framework CSS que prioriza las utilidades" que proporciona varias de estas clases de utilidades de un solo propósito que puedes utilizar directamente dentro de tu marcado para diseñar un elemento.

---

#### 1. Crear el proyecto Vite

```bash
npm create vite@latest my-project
cd my-project
```

- Crea una plantilla de proyecto con Vite.
    
- Puede ser con Vanilla, React, Vue, Svelte, etc. ([Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite "Installing Tailwind CSS with Vite - Tailwind CSS"))
    

---

#### 2. Instalar Tailwind como plugin de Vite

```bash
npm install tailwindcss @tailwindcss/vite
```

- Instala tanto Tailwind como el plugin específico para Vite.
    
- Esto hace que Tailwind funcione directamente con la compilación de Vite. ([Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite "Installing Tailwind CSS with Vite - Tailwind CSS"))
    

---

#### 3. Configurar Vite para usar Tailwind

Puedes crear el archivo de configuracion pero yo prefiero inicializarlo con : 

```shell 
npx tailwind init 
```

- Copia el siguiente texto a   `vite.config.js` o `vite.config.ts`:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

- Agrega el plugin `tailwindcss()` dentro del arreglo `plugins`.    
- Esto permite a Vite procesar las clases de Tailwind. ([Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite "Installing Tailwind CSS with Vite - Tailwind CSS"))

Despues importa tailwind en cualquier archivo css que utilices.  A mi me gusta en App.css me parece mas limpio que index. 

```css 
@import "tailwindcss";
```

---

#### 4. Importar Tailwind en tu CSS

En tu archivo CSS principal (por ejemplo `src/style.css`):

```css
@import "tailwindcss";
```

- Esto incluye todas las utilidades de Tailwind en tu proyecto.
    
- Puedes renombrar o añadir más reglas si quieres extender estilos. ([Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite "Installing Tailwind CSS with Vite - Tailwind CSS"))
    

---

#### 5. Inicia el servidor de desarrollo

```bash
npm run dev
```

- Inicia Vite y Tailwind compila automáticamente tu CSS basado en las clases usadas.
    
- Tailwind escanea tus archivos para generar solamente lo que usas. ([Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite "Installing Tailwind CSS with Vite - Tailwind CSS"))
    

---

#### 6. Usa clases de Tailwind en tu HTML

Ejemplo simple:

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/src/style.css" rel="stylesheet">
  </head>
  <body>
    <h1 class="text-3xl font-bold underline">Hello world!</h1>
  </body>
</html>
```

- Tailwind genera estilos solo para las clases que detecta en tus archivos. ([Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite "Installing Tailwind CSS with Vite - Tailwind CSS"))
    

---

### 🧠 Consejos útiles

- Asegúrate de que tu archivo CSS (`@import "tailwindcss"`) está **incluido** correctamente en tu HTML o entrada JS si usas frameworks.
    
- Tailwind **analiza tus archivos** (HTML, JS, JSX, TS, etc.) para generar CSS.
    
- Si ves que no se aplican estilos, revisa rutas y nombres de archivos. ([Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite "Installing Tailwind CSS with Vite - Tailwind CSS"))
    

---

### 🧩 Notas adicionales (según reacciones comunes)

- En algunos setups con React, puede ser necesario ajustar cómo se importa el CSS.
    
- A veces Vite necesita detección explícita de rutas de archivos para estilos Tailwind.  
    _(no parte directa de la guía oficial, pero útil al practicar)_.
    

--- 

## notas
cuando usar defualt y cuando no 
 export default componente grande

  zustand, redux  gestion del estado global 