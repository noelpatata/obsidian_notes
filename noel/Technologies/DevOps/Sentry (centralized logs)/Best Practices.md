### 1. Don't Log Sensitive Data

```kotlin
// ❌ BAD - Logs password
Logger.log("User login: $username with password: $password")

// ✅ GOOD - Only logs username
Logger.log("User login attempt: $username")
```

### 2. Use Appropriate Log Levels

```kotlin
// Info - normal operations
Logger.log("User viewed dashboard")

// Warning - unexpected but handled
Logger.logWarning("API", "Rate limit approaching")

// Error - something went wrong
Logger.logError("Payment", exception)
```

### 3. Add Context to Errors

```kotlin
// ❌ BAD - No context
Logger.logError("Error", exception)

// ✅ GOOD - Rich context
Logger.setContext("operation", "payment_processing")
Logger.setExtra("amount", "100.00")
Logger.setExtra("currency", "USD")
Logger.logError("PaymentProcessor", exception)
```

### 4. Use Breadcrumbs Effectively

```kotlin
fun processPayment() {
    Logger.breadcrumb("Starting payment validation")
    validatePayment()
    
    Logger.breadcrumb("Connecting to payment gateway")
    connectToGateway()
    
    Logger.breadcrumb("Processing transaction")
    processTransaction()
    
    // If error occurs, all breadcrumbs will be sent with the event
}
```

### 5. Sample Production Events

```kotlin
// In production, sample events to reduce volume
SentryAndroid.init(this) { options ->
    options.sampleRate = 0.5  // Sample 50% of error events
    options.tracesSampleRate = 0.1  // Sample 10% of transactions
}
```

---

## Troubleshooting

### Issue 1: Events Not Appearing in Sentry

**Check DSN:**

```kotlin
// Add this in Application.onCreate()
Log.d("Sentry", "DSN: ${getString(R.string.sentry_dsn)}")
```

**Check network:**

```bash
# Test connectivity from Android device/emulator
adb shell
ping your-sentry-ip
```

**Enable debug logging:**

```kotlin
options.isDebug = true
options.setDiagnosticLevel(SentryLevel.DEBUG)
```

### Issue 2: ProGuard Stripping Stack Traces

Ensure these rules are in `proguard-rules.pro`:

```proguard
-keepattributes LineNumberTable,SourceFile
```

### Issue 3: App Crashes on Sentry Init

Check Sentry version compatibility:

```gradle
// Use latest stable version
implementation 'io.sentry:sentry-android:6.34.0'
```

### Issue 4: Too Many Events

Implement filtering:

```kotlin
options.beforeSend = SentryOptions.BeforeSendCallback { event, hint ->
    // Filter out certain errors
    if (event.message?.contains("known_harmless_error") == true) {
        null  // Drop event
    } else {
        event
    }
}
```

---