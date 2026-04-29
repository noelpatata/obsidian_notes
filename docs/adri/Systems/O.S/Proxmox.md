
# Instalacion

Aqui ira la docu de como se instala.
# Configuracion posterior

> [!tip] 
>  *Esto son configuraciones simples solo tomo un par de anotaciones por si me olvido de las rutas o paquetes en alpine poder consultar rapidamente*

---
## 📦 Docker dentro de LXC en Proxmox

### 🚨 **Por qué Docker falla dentro de un contenedor LXC**

Docker necesita acceso a componentes del kernel como:

- **sysctl** (ej. `net.ipv4.ip_unprivileged_port_start`)
- **cgroups v2** completos
- **namespaces** totalmente funcionales
- **capacidades** del kernel (CAP_SYS_ADMIN, CAP_NET_ADMIN…)
- **AppArmor sin restricciones**    
- Montaje de **/sys**, **/proc** y cgroups sin límites

Un LXC **unprivileged** en Proxmox bloquea la mayoría de estas funciones por seguridad.  
Por eso aparece el típico error:

`failed to create task for container permission denied sysctl ... open: permission denied`

>[!note] En resumen: 
**Docker no puede crear contenedores dentro del LXC porque el LXC no tiene permisos suficientes.**


### 🧩 **Qué necesita Docker para funcionar dentro de LXC**

1. **Acceso completo a namespaces**    
2. **Cgroups v2 sin restricciones**
3. **AppArmor desactivado o muy relajado**
4. **Capacidades completas del kernel**
5. **Permitir contenedores dentro de contenedores (nesting)**
6. **Permitir FUSE** (necesario para ciertos drivers de Docker)


>[!tip] 
>  Todo esto hace mas facil convertir el contenedor a una **VM**, no un contenedor limitado.

**Pero si aun asi decides continuar:** 

### 🛠️ **Configuración recomendada del archivo `<ID>.conf`**

```bash 
# unprivileged: (eliminar la línea completamente)
features: nesting=1,keyctl=1,fuse=1 
lxc.apparmor.profile: unconfined 
lxc.cap.drop: lxc.cgroup2.devices.allow: a lxc.mount.auto: "proc:rw sys:rw"`
```

### ✔ Por qué funciona esta configuración

- **Contenedor privilegiado**
    - Tienes acceso directo a namespaces y sysctl → Docker puede funcionar.
- **nesting=1**
    - Permite contenedores dentro de contenedores.
    - Es lo que habilita Docker dentro de LXC.
- **keyctl=1**
    - Permite operaciones de claves del kernel que Docker necesita.
- **fuse=1**
    - Necesario para algunos sistemas de archivos y drivers FUSE.
- **AppArmor unconfined**
    - Evita que AppArmor bloquee syscalls internas de Docker.
- **lxc.cap.drop vacía**
    - No se eliminan capacidades esenciales que Docker requiere.
- **cgroup2.devices.allow: a**
    - Permite a Docker controlar dispositivos dentro del contenedor.
- **sys y proc montados en modo rw**
    - Necesario para acceso a subsistemas del kernel.

### 🔥 **Por qué `nesting` y `fuse` pueden ser _overrideados_**

En Proxmox/LXC, **el orden del archivo de configuración importa**.  
Proxmox procesa el archivo de arriba hacia abajo.

### 🟥 Problema

Si tienes, por ejemplo:

`features: nesting=1 ... lxc.apparmor.profile: generated`

O:

`features: fuse=1 ... lxc.cap.drop = mknod sys_admin net_admin ...`

Las líneas de abajo:

- **redefinen capacidades**
    
- **reaplican AppArmor**
    
- **vuelven a montar sysctl con restricciones**
    

Y entonces:

> 🔥 **Aunque `nesting=1` esté activado, queda completamente anulado.**

Esto genera un LXC que "parece" permitir Docker, pero realmente no.