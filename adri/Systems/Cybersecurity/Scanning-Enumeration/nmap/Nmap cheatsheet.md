## ⚡️ Metadatos rápidos

- Versión recomendada: mantener Nmap actualizado para tener los scripts NSE más recientes.
    
- Salidas recomendadas: `-oN`, `-oX`, `-oG`.
    

---

## 1) Descubrir hosts (Host discovery / ping sweep)

- `-sn` — ping scan (no puertos)
    

```bash
nmap -sn 192.168.1.0/24
```

- Usar ICMP + TCP probes (cuando ICMP esté bloqueado)
    

```bash
sudo nmap -PE -PS22,80,443 192.168.1.0/24
```

- Forzar tratar todas las IP como vivas (útil si los probes son bloqueados)
    

```bash
nmap -Pn 192.168.1.0/24
```

> [!note] Tips
> 
> - `-sn` es la opción más rápida para mapear hosts.
>     
> - Combina probes (`-PE`, `-PP`, `-PS`, `-PA`, `-PU`) según la política del perímetro.
>     

---

## 2) Descubrir puertos (Port scanning)

- Escaneo SYN (rápido, requiere root):
    

```bash
sudo nmap -sS -p- 10.0.0.5
# -p- escanea 1-65535
```

- Escaneo TCP connect (sin root):
    

```bash
nmap -sT -p22,80,443 example.com
```

- Escaneo UDP (más lento):
    

```bash
sudo nmap -sU -p53,123 target
```

- Detección de versiones de servicios:
    

```bash
nmap -sV -p80,443 target
```

- Modo agresivo (sV + OS + scripts + traceroute):
    

```bash
sudo nmap -A target
```


Si tiene firewall y el puerto de este te revienta el nmap, tira este comando donde 1000 es le puerto que te revienta el nmap : 

```bash 
sudo nmap -sS -v -v -Pn -g 1000 
``` 

### Opciones de rendimiento / evasión

- `-T0..-T5` — control de timing (`-T4` es usualmente rápido).
    
- `--min-rate` / `--max-retries` — para ajustar ritmo y reintentos.
    

### Guardar salida

```bash
nmap -sS -sV -p- -T4 -oN salida.txt target
nmap -oX salida.xml target
nmap -oG salida.gnmap target
```

---

## 3) Enumeración WordPress (plugins, temas, usuarios)

Nmap incluye scripts NSE específicos para WordPress.

- Enumerar plugins/temas (básico):


```bash
sudo nmap -p80,443 --script http-wordpress-enum example.com
```

- Enumerar plugins (script dedicado):
    

```bash
sudo nmap -p80,443 --script http-wordpress-plugins example.com
```

- Enumerar usuarios:
    

```bash
sudo nmap -p80,443 --script http-wordpress-users example.com
```

> [!note] Observaciones
> 
> - Los scripts usan listas conocidas; pueden necesitar ajustes para mayor profundidad.
>     
> - WAFs/CDNs pueden entorpecer resultados.
>     

---

## 4) Otras funcionalidades útiles / NSE (Nmap Scripting Engine)

- Ejecutar una categoría de scripts:
    

```bash
nmap --script discovery target
```

- `http-enum` — enumera rutas y ficheros web comunes:
    

```bash
nmap -p80,443 --script http-enum target
```

- `ssl-enum-ciphers` — auditoría de ciphers TLS/SSL:
    

```bash
nmap --script ssl-enum-ciphers -p 443 target
```

- Scripts de vulnerabilidad (usar solo con permiso):
    

```bash
nmap --script vuln target
```

### Escaneo recomendado inicial (rápido y útil)

```bash
sudo nmap -sS -sV -p- -T4 --script "default or safe" -oN resumen.txt target
```

---

## Plantillas útiles (para copiar rápido)

- Host discovery + listado de hosts vivos (archivo):
    

```bash
nmap -sn 10.0.0.0/24 -oN hosts_vivos.txt
```

- Escaneo completo de puertos + versión + scripts por defecto:
    

```bash
sudo nmap -sS -sV -p- -T4 --script default -oN full_scan.txt target
```

- Enumeración WordPress detallada:
    

```bash
sudo nmap -p80,443 --script http-wordpress-enum,http-wordpress-plugins,http-wordpress-users -oN wp_enum.txt example.com
```

---

## Buenas prácticas

    
- Empezar con `-sn` y luego scanea puertos conocidos.
    
- Evitar `-A` en entornos productivos sin notificar (ruido).
    
- Guardar y versionar resultados (`-oN`/`-oX`).
    

---
  