## Qué es React Hook Form?

React Hook Form es una librería para gestionar los formularios en react de manera mas eficiente y limpia.  *En resumen:*

>[!tip] Te facilita: 
>1. **Manejar el estado del formulario por ti** - No necesitas usar `useState` para cada campo.
>2. **Validar los campos fácilmente** - Con reglas simples en `register()`.
>3. **Mejor performance** - Menos re-renders que con `useState`.
>4. **Manejar errores** - Los errores se muestran cuando hay validación fallida.

#### Como lo hace para ser mas eficiente ? 

Gracias a que no usa el hook `useState` para los formularios. 
#### Como lo hace? 

React hook forms evita esto usando referencias a el valor introducido en el campo de manera directa desde el **DOM**. 
Capturando el valor únicamente cuando es necesario. *(ej: validacion , submit... )* sin forzar el innecesario rerender.

#### Pero por que eso lo hace mas eficiente? 

***Primero hay que entender que hace useState.*** 

Cuando una variable que usa `useState` cambia de estado, react **rerenderiza** el *componente que usa el hook*, de manera que si usas `useState` para el formulario, ***por cada cambio de estado de un campo rerenderizas el formulario entero***. 

Solo con explicar eso se entiende lo ineficiente que es manejar un form con `useState` .

## Que es Zod ? 

Zod es un framework de declaracion y validacion de esquemas. Resumido te permite definir como deben ser tus datos ( en un schema ) y luego validar que los datos reales coinciden. 


## Instalar

```bash
npm install react-hook-form zod @hookform/resolvers
```

