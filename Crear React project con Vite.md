
### Que es Vite. 

Vite es un bundler de JS o sus frameworks.

#### Que es un bundler. 

Un **bundler** es una herramienta que **prepara tu código para que pueda ejecutarse correctamente** (en un navegador, en un móvil o en producción). No es solo “empaquetar archivos”, hace **muchas cosas clave automáticamente**.
##### Qué hace el bundler.

Cuando tú escribes una app moderna:
- Usas muchos archivos (`.js`, `.ts`, `.jsx`, `.tsx`).
- Importas módulos (`import x from './utils'`).
- Usas frameworks (React, Vue, etc.)
- Usas código que el navegador **no entiende directamente** (TypeScript, JSX).
- Tienes imágenes, fuentes, CSS, etc.

> [!note] El navegador o el móvil **no compilan eso** 
> Asi que ahí entra el **bundler**.

--- 

te permite crear projectes React, con plantilla directamente o atraves del menú interactivo.


### Crear proyecto sin argumentos.

Si no especificas argumentos, Vite te mostra un menu de shell interactivo con el que podras elegir framework i variante:

```shell
npm create vite@latest 
```

Sigue el menu interactivo. 

>[!tip] Si le has dado que no a el paso 5 tendras que instalar npm manualmente en el proyecto y correr el servidor de desarrollo de vite:
>```
>cd <nom-del-projecte>
>npm install
>npm run dev
>```

El menú te pedira:

1. **Nom del projecte** 
2. **Framework** → tria: `React`
3. **Variantes de lenguaje** → 
    - **`JavaScript`  
    - `JavaScript-SWC`
    - `TypeScript` 
    - 
4. **Rolldown**: (No, per defecte)
5. **Instal·lació i arrancada automàtica**: Instal·la dependències i arrenca el servidor de desenvolupament

### Opción B — Crear proyecto con plantilla 

```shell
npm create vite@latest my-app -- --template react
```

Mas rapido que la anterior ya que le pasamos como argumentos la plantilla para react, y el nombre del proyecto. 

> [!note]
> Ambas maneras activan el soporte paraJSX automàticamente. No es necesario configurar Babel manualmente.

