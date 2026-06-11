
> [!tip]
> Por defecto, **Ctrl + b** es el _prefix_ de tmux.  

## 💼 Sesiones

| Comando                                  | Descripción                 |
| ---------------------------------------- | --------------------------- |
| `tmux` / `tmux new` / `tmux new-session` | Iniciar nueva sesión        |
| `tmux new -s <name>`                     | Iniciar sesión con nombre   |
| `tmux new-session -A -s <name>`          | Iniciar o adjuntar a sesión |
| `tmux ls` / `tmux list-sessions`         | Listar sesiones             |
| `tmux attach` / `tmux a`                 | Adjuntar a última sesión    |
| `tmux attach -t <name>`                  | Adjuntar a sesión nombrada  |
| `Ctrl+b d`                               | Desconectar (detach)        |
| `Ctrl+b $`                               | Renombrar sesión            |
| `Ctrl+b s`                               | Mostrar todas las sesiones  |
| `Ctrl+b (` / `Ctrl+b )`                  | Sesión anterior / siguiente |

---

## 🪟 Ventanas (Windows)

| Comando      | Descripción               |
| ------------ | ------------------------- |
| `Ctrl+b c`   | Crear nueva ventana       |
| `Ctrl+b ,`   | Renombrar ventana         |
| `Ctrl+b &`   | Cerrar ventana            |
| `Ctrl+b w`   | Listar ventanas           |
| `Ctrl+b p`   | Ventana anterior          |
| `Ctrl+b n`   | Ventana siguiente         |
| `Ctrl+b 0…9` | Ir a ventana por número   |
| `Ctrl+b l`   | Alternar a última ventana |

Además (comandos tmux):  
`: swap-window -s <src> -t <dst>` — Intercambia ventanas ([tmuxcheatsheet.com](https://tmuxcheatsheet.com/ "Tmux Cheat Sheet & Quick Reference | Session, window, pane and more"))

---

## ▗ Panes (Divisiones)

| Atajo                   | Acción                            |
| ----------------------- | --------------------------------- |
| `Ctrl+b %`              | Dividir vertical (columna)        |
| `Ctrl+b "`              | Dividir horizontal (fila)         |
| `Ctrl+b o`              | Siguiente panel                   |
| `Ctrl+b ;`              | Panel activo anterior             |
| `Ctrl+b q`              | Mostrar números de panel          |
| `Ctrl+b z`              | Zoom (expandir panel)             |
| `Ctrl+b x`              | Cerrar panel                      |
| `Ctrl+b {` / `Ctrl+b }` | Mover panel izquierdo / derecho   |
| `Ctrl+b Space`          | Cambiar layout (orden de paneles) |

> [!note] 
Navegar entre paneles con clásicas teclas de flecha después del _prefix_ ([tmuxcheatsheet.com](https://tmuxcheatsheet.com/ "Tmux Cheat Sheet & Quick Reference | Session, window, pane and more"))

---

## 📋 Modo Copia / Scroll

| Acción                  | Atajo                    |
| ----------------------- | ------------------------ |
| Entrar en modo copia    | `Ctrl+b [`               |
| Scroll arriba           | `PageUp` / flecha arriba |
| Salir modo copia        | `q`                      |
| Empezar selección       | `Space`                  |
| Copiar selección        | `Enter`                  |
| Pegar buffer            | `Ctrl+b ]`               |
| Ir a inicio / fin       | `g` / `G`                |
| Buscar adelante / atrás | `/` / `?`                |
| Siguiente / anterior    | `n` / `N`                |

---

## 🧠 Buffers y Portapapeles

| Comando tmux             | Acción                       |
| ------------------------ | ---------------------------- |
| `: capture-pane`         | Capturar contenido del panel |
| `: save-buffer <file>`   | Guardar buffer a archivo     |
| `: list-buffers`         | Listar buffers               |
| `: show-buffer`          | Mostrar contenido buffer     |
| `: choose-buffer`        | Elegir y pegar buffer        |
| `: delete-buffer -b <n>` | Borrar buffer n              |

---

## ⚙️ Configuración y Misc

| Atajo / Comando          | Descripción                          |
| ------------------------ | ------------------------------------ |
| `Ctrl+b :`               | Modo comando                         |
| `: set -g <op> <val>`    | Establecer opción global             |
| `: setw -g <op> <val>`   | Establecer opción en ventana         |
| `: setw -g mode-keys vi` | Modo copia estilo Vim                |
| `: set -g mouse on`      | Habilitar mouse (scroll y selección) |

---

## 📌 Tips Rápidos

- **Listar atajos**: `Ctrl+b ?`
    
- **Ver todos los binds**: `tmux list-keys` ([tmuxcheatsheet.com](https://tmuxcheatsheet.com/ "Tmux Cheat Sheet & Quick Reference | Session, window, pane and more"))
    

---

¿Quieres que lo complete con **ejemplos de configuración (`.tmux.conf`)** o **atajos de teclado extendidos (vim-style, navegación avanzada, etc.)**?