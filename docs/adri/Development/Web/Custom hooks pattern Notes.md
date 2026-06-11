## Introducción

A medida que las aplicaciones de React crecen en complejidad, gestionar la lógica de negocio, las llamadas a API y las actualizaciones de estado puede volverse desafiante. Un enfoque efectivo es organizar tu código en torno a **ganchos personalizados basados en funciones** que encapsulan la lógica para un dominio o función específica de tu aplicación.

> [!note]
> Asi que estuve en busqueda de cual era el mejor patron  o arquitectura para mantener el codigo react limpio y encontre el  patron que mas clean code me parecio. 

## Feature-Based Custom Hooks

Este patron de react se basa en hooks que contienen toda la logica de negocio, api calls, manejo de estado, navegacion relativa a la feature especifica, y dominio de la app.

Apartir de aqui he disenyado esta estructura que estara mejor o peor -> 

## 📁 **Estructura de Directorios en TS**

```sh
src/
├── App.css                            # (estilos globales de la app)
├── App.jsx                            # (componente raíz que monta layouts, rutas y providers)
├── assets/
│   └── react.svg                      # (recursos estáticos / imágenes)
├── features/                          # (carpeta principal por features)
│   ├── Auth/                          # (feature de autenticación)
│   │   ├── components/
│   │   │   ├── loginFormComponent.jsx     # (componente presentacional del formulario de login)
│   │   │   └── privateRoute.jsx          # (componente para proteger rutas según auth)
│   │   ├── context/
│   │   │   └── authContext.jsx           # (contexto para estado de autenticación y helpers)
│   │   ├── hooks/
│   │   │   ├── useAuth.jsx               # (hook principal: login, logout, estado del usuario)
│   │   │   └── useLoginForm.jsx          # (hook que encapsula la lógica del formulario de login)
│   │   ├── pages/
│   │   │   └── loginPage.jsx             # (página que compone loginForm y layout)
│   │   ├── schemas/
│   │   │   └── authFormSchema.jsx        # (definición/validación del schema del form — Zod/Yup/validators)
│   │   ├── services/
│   │   │   └── authService.jsx           # (llamadas a API relacionadas con auth)
│   │   └── ui/
│   │       └── loginForm.jsx             # (componente UI reutilizable del formulario de login)
│   └── TaskList/                      # (feature principal: listado y gestión de tareas)
│       ├── components/
│       │   ├── filterBarFormComponent.jsx  # (UI para el formulario de filtros — presentación)
│       │   ├── taskFormComponent.jsx       # (componente presentacional para crear/editar tarea)
│       │   └── taskListComponent.jsx       # (componente que lista tareas; usa hooks para datos)
│       ├── hooks/
│       │   ├── useFilteredList.jsx         # (hook que aplica filtros y retorna lista filtrada)
│       │   ├── useFilterForm.jsx           # (hook para la lógica del formulario de filtros)
│       │   ├── useTaskForm.jsx             # (hook que encapsula creación/edición de tareas)
│       │   └── useTaskList.jsx             # (hook principal: carga, CRUD, persistencia y sincronización)
│       ├── pages/
│       │   └── taskListPage.jsx            # (página que compone la UI del TaskList con layouts)
│       ├── schema/
│       │   ├── filterTaskBarSchema.jsx     # (schemas/validadores para el filtro)
│       │   └── taskFormSchema.jsx          # (schemas/validadores para el formulario de tarea)
│       └── ui/
│           ├── filterTaskBar.jsx           # (componentes UI concretos del filtro)
│           ├── taskForm.jsx                 # (componente UI del formulario; usa useTaskForm)
│           ├── taskItem.jsx                 # (representación visual de una tarea individual)
│           └── taskList.jsx                 # (componente visual que itera taskItem)
├── index.css                           # (reseteo / estilos globales base)
├── main.jsx                            # (punto de entrada que monta ReactDOM y providers)
└── shared/                             # (recursos compartidos entre features)
    ├── layouts/
    │   ├── authLayout.jsx              # (layout para páginas de autenticación)
    │   └── mainLayout.jsx              # (layout principal: header, nav, footer)
    └── ui/
        ├── button.jsx                  # (componente Button reutilizable, estilizado con Tailwind)
        └── form/
            ├── formContainer.jsx       # (contenedor general para formularios: grid/padding)
            ├── inputs/
            │   ├── checkboxInput.jsx   # (input checkbox estandarizado)
            │   ├── dateInput.jsx       # (input date personalizado)
            │   ├── radioInput.jsx      # (input radio estandarizado)
            │   ├── selectInput.jsx     # (select estilizado / con Controller support)
            │   ├── textareaInput.jsx   # (textarea estandarizado)
            │   └── textInput.jsx       # (input de texto estandarizado con errores/aria)
            └── submitButton.jsx        # (botón de submit con estados: loading/disabled)
```
## **Resumen del Flujo**

1. **App.tsx** → Provee contexto global  
2. **TaskProvider** → Inicializa `useTasks()`  
3. **TaskList** → Usa `useTaskContext()` + `useTaskFilters()`  
4. **TaskItem** → Usa acciones del contexto  
5. **TaskForm** → Usa `useTaskCreate()`  
6. **FilterBar** → Usa `useTaskFilters()` para actualizar filtros  
7. **UI Components** → Usan `useTheme()` y otros hooks UI
---

## 📝 **Ejemplo de cada archivo por una feature 
---

## 📊 **Resumen del Flujo**

1. main.jsx monta App.jsx dentro de providers (Auth, Theme, etc.).  
2. App.jsx define rutas y layouts; las páginas usan los componentes feature.  
3. Una página del TaskList (taskListPage.jsx) compone UI (taskList, filterBar, taskForm).  
4. La UI llama a hooks (useTaskList, useFilteredList, useTaskForm) que contienen la lógica: llamadas a services, validación con schemas, persistencia (localStorage / API).  
5. Los services encapsulan fetch/axios y transformaciones de payload.  
6. shared/ui y layouts ofrecen componentes y estilos reutilizables (botones, inputs, containers).


---

## 🎯 **Beneficios de esta Estructura**

1. **Modularidad**: Cada feature es independiente
2. **Reusabilidad**: Hooks se pueden usar en múltiples componentes
3. **Testabilidad**: Fácil de probar por separado
4. **Mantenibilidad**: Todo relacionado está junto
5. **Escalabilidad**: Fácil añadir nuevos features



---

*Tags: #react #hooks #task-list #feature-architecture #project-structure*