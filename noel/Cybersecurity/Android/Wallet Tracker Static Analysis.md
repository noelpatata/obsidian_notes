# Análisis Estático de Vulnerabilidades — WalletTracker

**Fecha:** 2026-03-16
**Versión analizada:** branch `main` (commit `6fa4d50`)
**Alcance:** codebase completo (Kotlin + AndroidManifest + Gradle)

---

## Índice

1. [JWT Validation](#1-jwt-validation)
2. [Logs / printStackTrace](#2-logs--printstacktrace)
3. [Certificate Pinning](#3-certificate-pinning)
4. [Intent expuesto para CSV](#4-intent-expuesto-para-csv)
5. [MainActivity sin permisos](#5-mainactivity-sin-permisos)
6. [Contraseña en texto plano en memoria](#6-contraseña-en-texto-plano-en-memoria)
7. [Cifrado biométrico AES-CBC](#7-cifrado-biométrico-aes-cbc)
8. [Resumen de prioridades](#resumen-de-prioridades)

---

## 1. JWT Validation

**Archivo:** `util/Cryptography.kt:191-201`
**Severidad:** Alta

### Código vulnerable

```kotlin
fun isTokenValid(jwt: String): Boolean {
    return try {
        val payload = jwt.split(".").getOrNull(1) ?: return false
        val padded = payload.padEnd((payload.length + 3) / 4 * 4, '=')
        val decoded = String(Base64.getDecoder().decode(padded))
        val exp = Regex("\"exp\":(\\d+)").find(decoded)?.groupValues?.get(1)?.toLong() ?: return false
        System.currentTimeMillis() / 1000 < exp
    } catch (e: Exception) {
        false
    }
}
```

### Por qué es vulnerable

Un JWT tiene la estructura `header.payload.signature`. Los tres segmentos son Base64url-encoded. La **firma** (`signature`) es un HMAC-SHA256 o RSA-SHA256 del `header.payload` con la clave secreta del servidor. Es lo único que garantiza que el token fue emitido por el servidor.

El código:
- Parte el JWT por `.` y coge solo el índice `[1]` → el payload
- Decodifica el payload en JSON
- Extrae el campo `exp` con una regex
- **Nunca toca el índice `[2]`** (la firma)

Esto significa que la validación es completamente ciega a si el token es auténtico. Cualquier string con formato `xxx.<base64({"exp":9999999999})>.xxx` pasa la validación.

En `LoginActivity.kt:122`:
```kotlin
if (session.token.isNotEmpty() && Cryptography.isTokenValid(session.token)) {
    appMode.isOnline = true
    navigateToMain()  // ← entra directamente
    return true
}
```
Si alguien puede escribir en la BD local (dispositivo rooteado, backup extraído), inyecta un token con `exp` grande → auto-login sin haber tocado el servidor.

### Cómo arreglarlo

La validación de firma de un JWT **pertenece al servidor**, no al cliente. El cliente no tiene la clave secreta del servidor para verificarla. El fix correcto es dejar que sea el propio servidor quien rechace tokens inválidos con HTTP 401.

Renombrar `isTokenValid` para dejar claro que solo comprueba expiración local (para evitar llamadas innecesarias al servidor con un token obviamente expirado):

```kotlin
// Solo sirve para evitar llamadas con token claramente expirado.
// La validación real la hace el servidor con 401.
fun isTokenExpired(jwt: String): Boolean {
    return try {
        val payload = jwt.split(".").getOrNull(1) ?: return true
        val padded = payload.padEnd((payload.length + 3) / 4 * 4, '=')
        val decoded = String(Base64.getDecoder().decode(padded))
        val exp = Regex("\"exp\":(\\d+)").find(decoded)
            ?.groupValues?.get(1)?.toLong() ?: return true
        System.currentTimeMillis() / 1000 >= exp  // true = expirado
    } catch (e: Exception) {
        true  // si no se puede parsear, tratar como expirado
    }
}
```

Y en `LoginActivity.kt`:
```kotlin
// En lugar de "token es válido → entrar":
if (session.token.isNotEmpty() && !Cryptography.isTokenExpired(session.token)) {
    // No navegamos directamente. Hacemos una llamada de verificación al servidor.
    lifecycleScope.launch {
        val result = loginRepo.verifyToken(session.token)  // endpoint GET /me o /health
        if (result is AppResult.Success) {
            appMode.isOnline = true
            navigateToMain()
        }
        // Si es 401, el servidor lo rechaza y el usuario va al login normal
    }
    return true
}
```

---

## 2. Logs / printStackTrace

**Archivos:** `util/Cryptography.kt:86,121,157` · `util/AppResultHandler.kt:13`
**Severidad:** Media-Alta

### Código vulnerable

```kotlin
// Cryptography.kt — aparece en verify(), hybridDecrypt(), hybridEncrypt()
} catch (e: Exception) {
    e.printStackTrace()
    false
}

// AppResultHandler.kt
if (BuildConfig.DEBUG) {
    Log.d(LogTag.DEBUG, "${result.message}\n${result.stackTrace}")
}
```

### Por qué es vulnerable

En Android, `e.printStackTrace()` escribe en `System.err`, que el runtime redirige al buffer de logcat con prioridad `WARN`. Logcat es un buffer circular en memoria del kernel (`/dev/log/`). Hasta Android 4.0 era legible por cualquier app. Desde Android 4.1+ requiere permiso `READ_LOGS`, pero:

- Cualquier app con `READ_LOGS` (apps de sistema, apps de debug preinstaladas por el fabricante) puede leerlo
- Con ADB conectado (modo debug activado en el dispositivo), `adb logcat` lo lee todo sin restricciones
- En dispositivos rooteados, cualquier proceso con `su` puede leerlo

Lo que se expone en los stack traces de `Cryptography.kt`:
- Nombres exactos de clases internas y métodos
- Números de línea exactos → facilita que un decompilado se mapee 1:1 con el código real
- En `hybridDecrypt` (línea 121): si falla el descifrado, el stack trace puede revelar qué paso exacto falló (RSA vs AES), lo que da información sobre el formato de datos esperado
- En `verify` (línea 86): expone detalles del mecanismo de firma RSA-PSS

Para `AppResultHandler.kt`: aunque esté bajo `BuildConfig.DEBUG`, si alguien tiene un build de debug del APK (común en CI/CD expuesto), la totalidad del stack trace interno sale al logcat.

### Cómo arreglarlo

```kotlin
// util/Logger.kt — centralizar todos los logs
object Logger {
    fun log(tag: String, message: String) {
        if (BuildConfig.DEBUG) {
            Log.d(tag, message)
        }
        // En producción: no hacer nada, o enviar a un servicio de crash reporting
        // como Firebase Crashlytics (que envía de forma segura, no a logcat)
    }

    fun logError(tag: String, e: Exception) {
        if (BuildConfig.DEBUG) {
            Log.e(tag, e.message ?: "Error", e)  // solo en debug
        }
        // En producción: FirebaseCrashlytics.getInstance().recordException(e)
    }
}
```

```kotlin
// Cryptography.kt — reemplazar todos los e.printStackTrace()
} catch (e: Exception) {
    Logger.logError("Cryptography", e)
    false  // o null
}
```

```kotlin
// AppResultHandler.kt
fun handleError(context: Context, result: AppResult.Error) {
    Logger.logError("AppResult", Exception(result.stackTrace))
    // En producción, result.stackTrace nunca sale al logcat
    val message = if (result.isControlled) result.message else unexpectedError
    Toast.makeText(context, message, Toast.LENGTH_LONG).show()
}
```

---

## 3. Certificate Pinning

**Archivo:** `data/api/ApiClient.kt:23-29`
**Severidad:** Media-Alta

### Código vulnerable

```kotlin
private val okHttpClient by lazy {
    OkHttpClient.Builder()
        .retryOnConnectionFailure(true)
        .connectionPool(ConnectionPool(5, 5, TimeUnit.MINUTES))
        .build()  // ← sin CertificatePinner, sin custom TrustManager
}
```

### Por qué es vulnerable

TLS sin pinning confía en cualquier certificado firmado por cualquier CA en el trust store del sistema. El trust store de Android incluye ~150 CAs raíz. Un atacante solo necesita que **una** de esas CAs (o cualquier CA subordinada que emita) firme un certificado para el dominio objetivo.

Vectores reales:
- **CA comprometida**: varias CAs han sido comprometidas históricamente (DigiNotar 2011, Comodo 2011). Si una CA del trust store emite un cert fraudulento para tu dominio, el cliente lo acepta.
- **MDM/Corporate proxy**: en dispositivos empresariales, el departamento de IT instala su propia CA raíz. Cualquier tráfico HTTPS pasa por su proxy de inspección (Zscaler, Palo Alto, etc.) sin que el usuario lo sepa.
- **Dispositivo rooteado con MagiskTrustUserCerts**: el usuario o una app privilegiada añade su CA al sistema. Herramientas como Frida + Objection o Burp Suite pueden interceptar todo el tráfico con un certificado propio.

Sin pinning, cualquiera de estos escenarios permite ver en claro: tokens JWT en los headers `Authorization`, credenciales en el cuerpo de `/login`, claves públicas en los intercambios.

### Cómo arreglarlo

```kotlin
private val okHttpClient by lazy {
    val certificatePinner = CertificatePinner.Builder()
        // El pin es el hash SHA-256 de la clave pública del certificado (SubjectPublicKeyInfo).
        // Obtenerlo:
        // openssl s_client -connect tu-servidor.com:443 | \
        //   openssl x509 -pubkey -noout | \
        //   openssl pkey -pubin -outform der | \
        //   openssl dgst -sha256 -binary | base64
        .add("tu-servidor.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
        // Siempre añadir un backup pin (del cert de renovación o de la CA intermedia)
        .add("tu-servidor.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")
        .build()

    OkHttpClient.Builder()
        .retryOnConnectionFailure(true)
        .connectionPool(ConnectionPool(5, 5, TimeUnit.MINUTES))
        .certificatePinner(certificatePinner)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
}
```

> El pin se calcula sobre la **clave pública** (no el certificado completo) para sobrevivir renovaciones del certificado mientras se mantenga el mismo par de claves. Siempre incluir al menos dos pins (cert actual + CA intermedia o cert de backup) para evitar que un pin incorrecto bloquee todos los usuarios.

---

## 4. Intent expuesto para CSV

**Archivos:** `AndroidManifest.xml:26-40` · `ui/login/LoginActivity.kt:321-332`
**Severidad:** Media

### Código vulnerable

```xml
<!-- AndroidManifest.xml -->
<activity android:name=".ui.login.LoginActivity" android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/csv" />
    </intent-filter>
    <!-- también text/plain y application/csv -->
</activity>
```

```kotlin
// LoginActivity.kt:321-332
private fun navigateToMain() {
    val currentIntent = intent
    if (currentIntent.action == Intent.ACTION_SEND) {
        val newIntent = Intent(currentIntent)  // ← copia el intent original COMPLETO
        newIntent.setClass(this, MainActivity::class.java)
        newIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        startActivity(newIntent)  // ← lanza MainActivity con datos controlados por el atacante
    } else {
        startActivity(Intent(this, MainActivity::class.java))
    }
    finish()
}
```

### Por qué es vulnerable

El intent-filter convierte a `LoginActivity` en un **target público** para cualquier app del dispositivo. El problema real está en `navigateToMain()`:

1. Una app maliciosa construye un `Intent(Intent.ACTION_SEND)` con MIME `text/csv` y lo envía a `LoginActivity`
2. `LoginActivity` lo recibe. Si ya hay una sesión válida, `tryAutoLogin()` → `navigateToMain()` se ejecuta inmediatamente
3. `navigateToMain()` hace `Intent(currentIntent)` → **copia los extras del intent del atacante** → lo lanza como `MainActivity`
4. `MainActivity` procesa los extras sin saber que vienen de una app maliciosa

Adicionalmente, el intent-filter de `text/plain` es especialmente amplio — básicamente cualquier app que "comparta texto" puede apuntar a `LoginActivity`.

### Cómo arreglarlo

El intent filter de compartir CSV debería estar en `MainActivity`, no en `LoginActivity`. `LoginActivity` no debería recibir datos externos, solo autenticar:

```xml
<!-- AndroidManifest.xml -->
<activity android:name=".ui.login.LoginActivity" android:exported="true">
    <!-- Solo el launcher intent -->
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>

<activity
    android:name=".MainActivity"
    android:exported="true"
    android:launchMode="singleTop"
    android:label="@string/app_name"
    android:theme="@style/Theme.WalletTracker.NoActionBar">
    <!-- Mover el share intent aquí -->
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/csv" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="application/csv" />
    </intent-filter>
</activity>
```

```kotlin
// LoginActivity.kt — eliminar el forwarding de intent
private fun navigateToMain() {
    // Nunca copiar el intent entrante. Siempre crear uno limpio.
    startActivity(Intent(this, MainActivity::class.java))
    finish()
}
```

```kotlin
// MainActivity.kt — procesar el share intent aquí, con validación de sesión
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    // Verificar sesión activa antes de procesar cualquier intent externo
    if (!sessionRepo.hasValidSession()) {
        startActivity(Intent(this, LoginActivity::class.java))
        finish()
        return
    }
    // Ahora es seguro procesar el intent
    handleIncomingIntent(intent)
}
```

---

## 5. MainActivity sin permisos

**Archivo:** `AndroidManifest.xml:47-53`
**Severidad:** Alta

### Código vulnerable

```xml
<activity
    android:name=".MainActivity"
    android:exported="true"
    android:launchMode="singleTop"
    android:label="@string/app_name"
    android:theme="@style/Theme.WalletTracker.NoActionBar">
    <!-- sin android:permission -->
</activity>
```

### Por qué es vulnerable

`android:exported="true"` sin `android:permission` significa que el componente es accesible por **cualquier app instalada en el dispositivo**, sin ninguna restricción.

`MainActivity` no tiene ninguna comprobación de autenticación en su `onCreate`. Si una app maliciosa ejecuta:

```kotlin
// Desde una app atacante
val intent = Intent()
intent.setClassName("win.downops.wallettracker", "win.downops.wallettracker.MainActivity")
startActivity(intent)
```

Android lanzará `MainActivity` directamente, saltándose `LoginActivity` por completo. El usuario ve el dashboard de la app sin haberse autenticado. Toda la funcionalidad de la app queda expuesta: leer gastos, crear importes, ver métricas.

Combinado con la vulnerabilidad anterior (intent de CSV → `navigateToMain()` → `MainActivity`), hay dos rutas distintas para llegar a `MainActivity` sin login.

### Cómo arreglarlo

Dos capas de defensa:

**Capa 1: Manifiesto** — Si `MainActivity` solo debe ser lanzada desde dentro de la misma app, debe ser no exportada:

```xml
<activity
    android:name=".MainActivity"
    android:exported="false"   <!-- solo apps con el mismo UID pueden lanzarla -->
    android:launchMode="singleTop"
    android:label="@string/app_name"
    android:theme="@style/Theme.WalletTracker.NoActionBar">
    <!-- Sin intent-filters de terceros aquí -->
</activity>
```

> Si se implementa el fix del punto 4 (mover el share intent aquí), `exported` debe ser `true`. En ese caso, el guard en código es aún más crítico.

**Capa 2: Código** — `MainActivity` nunca debe confiar ciegamente en que alguien hizo login antes. Añadir guard en `onCreate`:

```kotlin
// MainActivity.kt
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {

    @Inject lateinit var sessionRepo: SessionRepository
    @Inject lateinit var appMode: AppMode

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Guard de autenticación — defensa en profundidad
        if (!isSessionValid()) {
            startActivity(Intent(this, LoginActivity::class.java).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
            })
            finish()
            return
        }

        // resto del onCreate...
    }

    private fun isSessionValid(): Boolean {
        val session = sessionRepo.getFirstSession() ?: return false
        if (!session.online) return true  // modo offline siempre válido
        return session.token.isNotEmpty() && !Cryptography.isTokenExpired(session.token)
    }
}
```

---

## 6. Contraseña en texto plano en memoria

**Archivo:** `ui/login/LoginActivity.kt:214,224,233-234`
**Severidad:** Media

### Código vulnerable

```kotlin
// LoginActivity.kt:214
val input = "${binding.inputUsername.text};${binding.inputPassword.text}".toByteArray(Charset.defaultCharset())

// LoginActivity.kt:224
doLogin(binding.inputUsername.text.toString(), binding.inputPassword.text.toString(), cipheredCredentials)

// LoginActivity.kt:233-234
val username = binding.inputUsername.text.toString().trim()
val password = binding.inputPassword.text.toString().trim()
```

### Por qué es vulnerable

En la JVM, `String` es **inmutable e internable**. Cuando se llama a `.toString()` sobre un `Editable`, se crea un objeto `String` en el heap que:

1. **No puede ser zeroed**: no hay referencia al array de chars interno después de la creación, así que `Arrays.fill` no es aplicable
2. **Puede ser interned**: el JIT puede mover la referencia al intern pool, donde vive hasta que la JVM se apaga
3. **No hay garantía de GC**: aunque no haya referencias, el GC puede tardar segundos, minutos, o indefinidamente en recolectarlo

Vectores de extracción:
- **Android Profiler / DDMS con debugging habilitado**: `Heap Dump` captura todos los objetos vivos en el heap, incluyendo `String`. Cualquier desarrollador con ADB puede ejecutar `adb shell am dumpheap <pid> /sdcard/heap.hprof` y analizarlo con MAT (Memory Analyzer Tool)
- **Dispositivo rooteado**: `su -c "cat /proc/<pid>/mem"` permite leer la memoria del proceso directamente
- **App con `DUMP` permission**: puede invocar `Debug.dumpHprofData()` en otras apps

La contraseña existe como `String` en memoria desde que el usuario la teclea hasta que el GC la recolecta, que puede ser mucho después de que el login haya terminado.

### Cómo arreglarlo

Usar `CharArray` en lugar de `String`. `CharArray` es mutable y puede zeroearse explícitamente:

```kotlin
// Extensión para extraer el contenido de un Editable como CharArray sin crear String
private fun Editable.toCharArray(): CharArray {
    val chars = CharArray(this.length)
    this.getChars(0, this.length, chars, 0)
    return chars
}

private fun CharArray.toByteArray(charset: Charset = Charsets.UTF_8): ByteArray {
    val charBuffer = java.nio.CharBuffer.wrap(this)
    val byteBuffer = charset.encode(charBuffer)
    return byteBuffer.array().copyOf(byteBuffer.limit())
}
```

```kotlin
// encryptAndLoginCredentials — sin crear String de la contraseña
private fun encryptAndLoginCredentials(result: BiometricPrompt.AuthenticationResult) {
    var usernameChars: CharArray? = null
    var passwordChars: CharArray? = null
    var inputBytes: ByteArray? = null

    try {
        usernameChars = binding.inputUsername.text.toCharArray()
        passwordChars = binding.inputPassword.text.toCharArray()

        val separator = ";".toByteArray()
        val usernameBytes = usernameChars.toByteArray()
        val passwordBytes = passwordChars.toByteArray()

        inputBytes = usernameBytes + separator + passwordBytes

        val encryptedBytes = result.cryptoObject?.cipher?.doFinal(inputBytes)
        val iv = result.cryptoObject?.cipher?.iv ?: throw Exception("Invalid iv")

        val cipheredCredentials = CipheredCredentials(
            Base64.getEncoder().encodeToString(encryptedBytes),
            Base64.getEncoder().encodeToString(iv)
        )

        lifecycleScope.launch {
            doLogin(String(usernameChars), passwordChars, cipheredCredentials)
        }
    } catch (e: Exception) {
        Logger.logError("LoginActivity", e)
    } finally {
        // Zerear todos los arrays sensibles inmediatamente
        usernameChars?.fill('\u0000')
        passwordChars?.fill('\u0000')
        inputBytes?.fill(0)
    }
}
```

```kotlin
// attemptLogin — usar CharArray
private fun attemptLogin() {
    val username = binding.inputUsername.text.toString().trim()
    var passwordChars: CharArray? = null

    try {
        passwordChars = binding.inputPassword.text.toCharArray()
        if (username.isEmpty() || passwordChars.isEmpty()) return

        if (isFingerprintActive) {
            promptAuthentication()
        } else {
            lifecycleScope.launch {
                doLogin(username, passwordChars)
            }
        }
    } finally {
        if (!isFingerprintActive) passwordChars?.fill('\u0000')
        // Si es fingerprint, el CharArray se pasa adelante y se zeroa en encryptAndLoginCredentials
    }
}
```

---

## 7. Cifrado biométrico AES-CBC

**Archivos:** `util/Biometrics.kt:24-28` · `ui/login/LoginActivity.kt:246-261`
**Severidad:** Media

### Código vulnerable

```kotlin
// Biometrics.kt:24-28
fun getCipher(): Cipher {
    return Cipher.getInstance(
        KeyProperties.KEY_ALGORITHM_AES + "/" +
        KeyProperties.BLOCK_MODE_CBC + "/" +
        KeyProperties.ENCRYPTION_PADDING_PKCS7  // ← AES/CBC/PKCS7Padding
    )
}

// LoginActivity.kt:250-251
.setBlockModes(KeyProperties.BLOCK_MODE_CBC)
.setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_PKCS7)

// LoginActivity.kt:148
cipher.init(Cipher.DECRYPT_MODE, secretKey, IvParameterSpec(Base64.getDecoder().decode(iv)))
```

### Por qué es vulnerable

**CBC (Cipher Block Chaining)** es un modo de cifrado que **solo provee confidencialidad, no autenticidad**. Esto lo hace vulnerable a dos ataques:

#### Ataque 1 — Bit-flipping

En CBC, el bloque en claro `P[i]` se calcula como `P[i] = D(C[i]) XOR C[i-1]`, donde `D` es el descifrado del bloque. Si un atacante modifica un byte en `C[i-1]`, el byte correspondiente en `P[i]` se voltea de forma predecible (XOR). Esto permite modificar el plaintext descifrado sin conocer la clave. En el contexto de credenciales `"usuario;password"`, un atacante con acceso a la BD local podría modificar el campo `cipheredCredentials` para alterar el username o password que se descifra.

#### Ataque 2 — PKCS#7 Padding Oracle

Este es el más serio. El esquema:

1. PKCS#7 padding rellena el último bloque hasta 16 bytes. Si el bloque tiene 13 bytes, añade `\x03\x03\x03`.
2. Al descifrar, el sistema verifica que el padding es correcto. Si no lo es, lanza una excepción (`BadPaddingException`).
3. Un atacante observa si el descifrado produce `BadPaddingException` o no → **oracle de padding**.

Con este oracle, el atacante puede descifrar el ciphertext byte a byte:
- Para descifrar 1 byte, prueba los 256 valores posibles modificando `C[i-1][ultimo_byte]`
- Cuando no hay `BadPaddingException`, el último byte del plaintext es `\x01` (padding válido de 1 byte)
- Con esto deduce el plaintext real: `P[i][ultimo_byte] = \x01 XOR C_modificado XOR C_original`
- Repite para cada byte → descifra el bloque completo en ~128 intentos promedio por byte

Con el IV y las credenciales cifradas almacenados juntos en la misma fila de SQLite, un atacante con acceso a la BD tiene todos los ingredientes.

#### Por qué AES-GCM soluciona esto

GCM (Galois/Counter Mode) es un modo **AEAD** (Authenticated Encryption with Associated Data). Internamente usa AES en modo CTR (sin padding → no hay padding oracle) más un MAC (GHASH). Produce un **authentication tag** de 16 bytes que es un MAC sobre el ciphertext completo. Al descifrar, si el tag no coincide, el descifrado falla con `AEADBadTagException` **antes de devolver ningún dato**. Esto hace imposible tanto el bit-flipping como el padding oracle porque cualquier modificación del ciphertext invalida el tag.

### Cómo arreglarlo

```kotlin
// Biometrics.kt — cambiar a GCM
object Biometrics {
    fun generateSecretKey(keyGenParameterSpec: KeyGenParameterSpec) {
        val keyGenerator = KeyGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        keyGenerator.init(keyGenParameterSpec)
        keyGenerator.generateKey()
    }

    fun getSecretKey(): SecretKey {
        val keyStore = KeyStore.getInstance("AndroidKeyStore")
        keyStore.load(null)
        return keyStore.getKey("USER_KEY", null) as SecretKey
    }

    fun getCipher(): Cipher {
        // GCM/NoPadding: AEAD, sin padding, con authentication tag
        return Cipher.getInstance("AES/GCM/NoPadding")
    }
}
```

```kotlin
// LoginActivity.kt — promptAuthentication con GCM
private fun promptAuthentication() {
    val keySpec = KeyGenParameterSpec.Builder(
        "USER_KEY",
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
    )
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setKeySize(256)
        .setUserAuthenticationRequired(true)
        .setInvalidatedByBiometricEnrollment(true)
        .build()

    Biometrics.generateSecretKey(keySpec)
    val secretKey = Biometrics.getSecretKey()
    val cipher = Biometrics.getCipher()
    cipher.init(Cipher.ENCRYPT_MODE, secretKey)
    biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
}
```

```kotlin
// LoginActivity.kt — loginWithFingerprint con GCMParameterSpec
private fun loginWithFingerprint(iv: String) {
    try {
        val cipher = Biometrics.getCipher()
        val secretKey = Biometrics.getSecretKey()
        // GCM necesita GCMParameterSpec con el tag length (128 bits)
        val ivBytes = Base64.getDecoder().decode(iv)
        cipher.init(
            Cipher.DECRYPT_MODE,
            secretKey,
            GCMParameterSpec(128, ivBytes)  // ← GCMParameterSpec en vez de IvParameterSpec
        )
        biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
    } catch (e: UnrecoverableKeyException) {
        Logger.log("Key not found")
    } catch (e: Exception) {
        Logger.log(e)
    }
}
```

> **Nota de migración:** Al pasar de CBC a GCM, los IVs almacenados en la BD tienen 16 bytes (CBC) pero GCM espera 12 bytes. Detectar si `iv.length == 16` al descifrar y forzar un re-cifrado con la nueva configuración la primera vez que el usuario haga login tras la actualización.

---

## Resumen de prioridades

| # | Vulnerabilidad | Archivo | Dificultad | Impacto |
|---|---------------|---------|------------|---------|
| 5 | MainActivity sin permisos | `AndroidManifest.xml:47` | Baja | Bypass de autenticación completo |
| 4 | Intent CSV en LoginActivity | `AndroidManifest.xml:26` + `LoginActivity.kt:321` | Baja | Inyección de datos en MainActivity |
| 1 | JWT sin verificar firma | `Cryptography.kt:191` | Media | Auto-login con token forjado |
| 2 | printStackTrace / logs | `Cryptography.kt:86,121,157` + `AppResultHandler.kt:13` | Baja | Reconnaissance para otros ataques |
| 3 | Certificate pinning | `ApiClient.kt:23` | Media | MITM en redes hostiles |
| 6 | Password en String en memoria | `LoginActivity.kt:214,224,233` | Media | Extracción de credenciales del heap |
| 7 | AES-CBC → AES-GCM | `Biometrics.kt:24` + `LoginActivity.kt:250` | Media | Descifrado de credenciales guardadas |
