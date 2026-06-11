#vite #react #bundler #javascript #setup #frontend #npm

### Que es Vite. 

Vite es un bundler de JS o sus frameworks, transpila el codigo de tu app algo que entiende el navegador, sirve el servidor de tu app, gestiona frameworks, crea tu proyecto...

#### Que es un bundler. 

Un **bundler** es una herramienta que **prepara tu código para que pueda ejecutarse correctamente** (en un navegador, en un móvil o en producción). No es solo “empaquetar archivos”, hace **muchas cosas clave automáticamente**.
##### Qué hace el bundler.

Cuando tú escribes una app moderna:
- Usas muchos archivos (`.js`, `.ts`, `.jsx`, `.tsx`).
- Importas módulos (`import x from './utils'`).
- Usas frameworks (React, Vue, etc.)
- Usas código que el navegador **no entiende directamente** (TypeScript, JSX).
- Tienes imágenes, fuentes, CSS, etc.

> [!tip] El navegador o el móvil **no compilan eso**. 
> Ergo ahí entra vite y transpila el codigo de tu app algo que entiende el navegador aka el **bundler**.

--- 

te permite crear proyectos React, con plantilla directamente o a través del menú interactivo.


### Crear proyecto sin argumentos.

Si no especificas argumentos, Vite te mostrará un menú de shell interactivo con el que podrás elegir framework y variante:

```shell
npm create vite@latest 
```

Sigue el menú interactivo. 

>[!note] 
> Si le has dado que no al paso 5 tendrás que instalar npm manualmente en el proyecto y correr el servidor de desarrollo de vite:
> ```
> cd <nombre-del-proyecto>
> npm install
> npm run dev
> ```

El menú te pedirá:

1. **Nombre del proyecto** 
2. **Framework** → elige: `React`
3. **Variantes de lenguaje** → 
    - **`JavaScript`  
    - `JavaScript-SWC`
    - `TypeScript` 
    - 
4. **Rolldown**: (No, por defecto)
5. **Instalación y arranque automático**: Instala dependencias y arranca el servidor de desarrollo

### Opción B — Crear proyecto con plantilla 

```shell
npm create vite@latest my-app -- --template react
```

Mas rapido que la anterior ya que le pasamos como argumentos la plantilla para react, y el nombre del proyecto. 

> [!note]
> Ambas maneras activan el soporte para JSX automáticamente. No es necesario configurar Babel manualmente.

