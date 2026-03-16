# Sentry Android Integration Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Basic Integration](#basic-integration)
4. [Advanced Configuration](#advanced-configuration)
5. [Logger Implementation](#logger-implementation)
6. [ProGuard/R8 Configuration](#proguardr8-configuration)
7. [Testing](#testing)
8. [Best Practices](#best-practices)
9. [Performance Monitoring](#performance-monitoring)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Android Studio Arctic Fox or newer
- Minimum SDK version: 21 (Android 5.0)
- Sentry self-hosted instance running (from installation guide)
- DSN from your Sentry project

**Get your DSN:**

1. Login to Sentry: `http://your-sentry-ip:9000`
2. Go to Projects → Wallet Tracker → Settings → Client Keys (DSN)
3. Copy the DSN: `http://public_key@your-sentry-ip:9000/project_id`

---

## Project Setup

### 1. Add Sentry Gradle Plugin

**build.gradle (Project level)**

```gradle
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.2'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.20'
        
        // Add Sentry Gradle Plugin
        classpath 'io.sentry:sentry-android-gradle-plugin:3.14.0'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
```

### 2. Apply Plugin and Add Dependencies

**build.gradle (App level)**

```gradle
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'io.sentry.android.gradle' version '3.14.0'
}

android {
    compileSdk 34
    
    defaultConfig {
        applicationId "win.downops.wallettracker"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }
    
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        debug {
            minifyEnabled false
        }
    }
}

dependencies {
    // Sentry SDK
    implementation 'io.sentry:sentry-android:6.34.0'
    
    // If using OkHttp for networking (for interceptor)
    implementation 'io.sentry:sentry-android-okhttp:6.34.0'
    
    // If using Timber for logging
    implementation 'io.sentry:sentry-android-timber:6.34.0'
    
    // If using Fragment tracking
    implementation 'io.sentry:sentry-android-fragment:6.34.0'
    
    // Other dependencies...
}

// Sentry configuration
sentry {
    // Generates a JVM (Java, Kotlin, etc.) source bundle and uploads your source code to Sentry.
    // This enables source context, allowing you to see your source
    // code as part of your stack traces in Sentry.
    includeSourceContext = true
    
    // Upload native symbols for NDK
    uploadNativeSymbols = false
    
    // Enable or disable the automatic configuration of Native Symbols
    autoUploadNativeSymbols = false
    
    // Enable or disable the automatic upload of ProGuard mapping files
    autoUploadProguardMapping = true
    
    // Disables or enables debug log output during the build
    debug = false
}
```

---

## Basic Integration

### 1. Create Sentry Configuration File

**Create file:** `app/src/main/res/values/sentry.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Replace with your actual DSN from Sentry -->
    <string name="sentry_dsn" translatable="false">http://public_key@your-sentry-ip:9000/1</string>
</resources>
```

### 2. Initialize Sentry in Application Class

**WalletTrackerApplication.kt**

```kotlin
package win.downops.wallettracker

import android.app.Application
import io.sentry.android.core.SentryAndroid
import io.sentry.SentryLevel
import io.sentry.SentryOptions

class WalletTrackerApplication : Application() {
    
    override fun onCreate() {
        super.onCreate()
        
        initializeSentry()
    }
    
    private fun initializeSentry() {
        SentryAndroid.init(this) { options ->
            // DSN from resources
            options.dsn = getString(R.string.sentry_dsn)
            
            // Set environment
            options.environment = if (BuildConfig.DEBUG) "development" else "production"
            
            // Set release version
            options.release = "wallet-tracker@${BuildConfig.VERSION_NAME}"
            
            // Enable debug logging in debug builds only
            options.isDebug = BuildConfig.DEBUG
            options.setDiagnosticLevel(if (BuildConfig.DEBUG) SentryLevel.DEBUG else SentryLevel.ERROR)
            
            // Sample rate for error events (1.0 = 100%)
            options.sampleRate = 1.0
            
            // Enable automatic session tracking
            options.isEnableAutoSessionTracking = true
            
            // Session tracking timeout (30 seconds default)
            options.sessionTrackingIntervalMillis = 30000
            
            // Enable ANR (Application Not Responding) detection
            options.isAnrEnabled = true
            options.anrTimeoutIntervalMillis = 5000
            
            // Enable automatic breadcrumbs
            options.isEnableActivityLifecycleBreadcrumbs = true
            options.isEnableAppLifecycleBreadcrumbs = true
            options.isEnableSystemEventBreadcrumbs = true
            options.isEnableAppComponentBreadcrumbs = true
            
            // Enable performance monitoring (tracing)
            options.tracesSampleRate = if (BuildConfig.DEBUG) 1.0 else 0.2
            
            // Enable network breadcrumbs
            options.isEnableNetworkEventBreadcrumbs = true
            
            // Attach screenshots on errors (optional)
            options.isAttachScreenshot = true
            
            // Attach view hierarchy (optional)
            options.isAttachViewHierarchy = true
            
            // Set maximum breadcrumbs
            options.maxBreadcrumbs = 100
            
            // Before send callback - filter sensitive data
            options.beforeSend = SentryOptions.BeforeSendCallback { event, hint ->
                // Don't send events in debug builds (optional)
                if (BuildConfig.DEBUG) {
                    null // Return null to drop the event
                } else {
                    // Filter sensitive data from event
                    filterSensitiveData(event)
                    event
                }
            }
            
            // Before breadcrumb callback - filter sensitive breadcrumbs
            options.beforeBreadcrumb = SentryOptions.BeforeBreadcrumbCallback { breadcrumb, hint ->
                // Filter sensitive data from breadcrumbs
                if (breadcrumb.message?.contains("password", ignoreCase = true) == true) {
                    null // Drop breadcrumb
                } else {
                    breadcrumb
                }
            }
        }
    }
    
    private fun filterSensitiveData(event: io.sentry.SentryEvent): io.sentry.SentryEvent {
        // Remove sensitive data from extra context
        event.contexts.apply {
            // Don't send device info if sensitive
            // remove("device")
        }
        
        // Filter sensitive tags
        event.tags?.apply {
            remove("password")
            remove("token")
            remove("api_key")
        }
        
        return event
    }
}
```

**Don't forget to register in AndroidManifest.xml:**

```xml
<application
    android:name=".WalletTrackerApplication"
    ...>
```

---

## Advanced Configuration

### 1. Create Centralized Logger Utility

**util/Logger.kt**

```kotlin
package win.downops.wallettracker.util

import android.util.Log
import io.sentry.Breadcrumb
import io.sentry.Sentry
import io.sentry.SentryLevel
import io.sentry.protocol.User
import win.downops.wallettracker.BuildConfig

object Logger {
    private const val TAG = "WalletTracker"
    
    // ========== INFO LOGGING ==========
    
    fun log(message: String) {
        if (BuildConfig.DEBUG) {
            Log.d(TAG, message)
        }
        Sentry.captureMessage(message, SentryLevel.INFO)
    }
    
    fun log(tag: String, message: String) {
        if (BuildConfig.DEBUG) {
            Log.d(tag, message)
        }
        Sentry.captureMessage("[$tag] $message", SentryLevel.INFO)
    }
    
    // ========== ERROR LOGGING ==========
    
    fun logError(tag: String, e: Exception) {
        val errorMessage = "Error in $tag: ${e.message}"
        
        if (BuildConfig.DEBUG) {
            Log.e(tag, errorMessage, e)
        }
        
        // Send to Sentry with context
        Sentry.withScope { scope ->
            scope.setTag("error_location", tag)
            scope.setLevel(SentryLevel.ERROR)
            Sentry.captureException(e)
        }
    }
    
    fun logError(tag: String, message: String) {
        if (BuildConfig.DEBUG) {
            Log.e(tag, message)
        }
        
        Sentry.withScope { scope ->
            scope.setTag("error_location", tag)
            scope.setLevel(SentryLevel.ERROR)
            Sentry.captureMessage(message, SentryLevel.ERROR)
        }
    }
    
    fun logError(tag: String, message: String, e: Exception) {
        val fullMessage = "$message: ${e.message}"
        
        if (BuildConfig.DEBUG) {
            Log.e(tag, fullMessage, e)
        }
        
        Sentry.withScope { scope ->
            scope.setTag("error_location", tag)
            scope.setExtra("error_message", message)
            scope.setLevel(SentryLevel.ERROR)
            Sentry.captureException(e)
        }
    }
    
    // ========== WARNING LOGGING ==========
    
    fun logWarning(tag: String, message: String) {
        if (BuildConfig.DEBUG) {
            Log.w(tag, message)
        }
        
        Sentry.captureMessage("[$tag] $message", SentryLevel.WARNING)
    }
    
    // ========== BREADCRUMBS ==========
    
    fun breadcrumb(message: String, category: String = "default") {
        if (BuildConfig.DEBUG) {
            Log.d(TAG, "[BREADCRUMB] $message")
        }
        
        val breadcrumb = Breadcrumb().apply {
            this.message = message
            this.category = category
            this.level = SentryLevel.INFO
        }
        Sentry.addBreadcrumb(breadcrumb)
    }
    
    fun breadcrumbNavigation(from: String, to: String) {
        breadcrumb("Navigation: $from → $to", "navigation")
    }
    
    fun breadcrumbNetwork(method: String, url: String, statusCode: Int? = null) {
        val message = if (statusCode != null) {
            "$method $url - Status: $statusCode"
        } else {
            "$method $url"
        }
        breadcrumb(message, "http")
    }
    
    fun breadcrumbUser(action: String) {
        breadcrumb("User action: $action", "user")
    }
    
    // ========== USER CONTEXT ==========
    
    fun setUser(userId: String, email: String? = null, username: String? = null) {
        Sentry.setUser(User().apply {
            id = userId
            this.email = email
            this.username = username
        })
    }
    
    fun clearUser() {
        Sentry.setUser(null)
    }
    
    // ========== CUSTOM CONTEXT ==========
    
    fun setContext(key: String, value: String) {
        Sentry.setTag(key, value)
    }
    
    fun setContext(key: String, value: Map<String, Any>) {
        Sentry.setContext(key, value)
    }
    
    fun setExtra(key: String, value: String) {
        Sentry.setExtra(key, value)
    }
    
    // ========== PERFORMANCE TRACKING ==========
    
    fun startTransaction(name: String, operation: String): io.sentry.ITransaction {
        return Sentry.startTransaction(name, operation)
    }
    
    fun finishTransaction(transaction: io.sentry.ITransaction) {
        transaction.finish()
    }
    
    // ========== CUSTOM EVENTS ==========
    
    fun logEvent(eventName: String, data: Map<String, Any>? = null) {
        Sentry.withScope { scope ->
            data?.forEach { (key, value) ->
                scope.setExtra(key, value.toString())
            }
            Sentry.captureMessage(eventName, SentryLevel.INFO)
        }
    }
    
    // ========== NETWORK ERRORS ==========
    
    fun logNetworkError(url: String, statusCode: Int, errorBody: String? = null) {
        Sentry.withScope { scope ->
            scope.setTag("error_type", "network")
            scope.setExtra("url", url)
            scope.setExtra("status_code", statusCode.toString())
            errorBody?.let { scope.setExtra("error_body", it) }
            
            Sentry.captureMessage(
                "Network Error: HTTP $statusCode at $url",
                SentryLevel.ERROR
            )
        }
    }
    
    // ========== CRYPTOGRAPHY ERRORS ==========
    
    fun logCryptoError(operation: String, e: Exception) {
        Sentry.withScope { scope ->
            scope.setTag("error_type", "cryptography")
            scope.setExtra("crypto_operation", operation)
            scope.setLevel(SentryLevel.ERROR)
            Sentry.captureException(e)
        }
    }
    
    // ========== DATABASE ERRORS ==========
    
    fun logDatabaseError(operation: String, e: Exception) {
        Sentry.withScope { scope ->
            scope.setTag("error_type", "database")
            scope.setExtra("db_operation", operation)
            scope.setLevel(SentryLevel.ERROR)
            Sentry.captureException(e)
        }
    }
}
```

---

## Logger Implementation in Existing Code

### 3. Update ApiClient.kt (Network Monitoring)

```kotlin
// ApiClient.kt
package win.downops.wallettracker.data.remote

import io.sentry.Sentry
import io.sentry.SpanStatus
import okhttp3.*
import win.downops.wallettracker.util.Logger
import java.io.IOException
import java.util.concurrent.TimeUnit

object ApiClient {
    
    private val okHttpClient by lazy {
        OkHttpClient.Builder()
            .addInterceptor(SentryInterceptor())
            .addInterceptor(LoggingInterceptor())
            .retryOnConnectionFailure(true)
            .connectionPool(ConnectionPool(5, 5, TimeUnit.MINUTES))
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            // Add certificate pinning here if needed
            .build()
    }
    
    // Sentry OkHttp Interceptor
    private class SentryInterceptor : Interceptor {
        override fun intercept(chain: Interceptor.Chain): Response {
            val request = chain.request()
            val url = request.url.toString()
            
            // Create Sentry span for this request
            val span = Sentry.getSpan()?.startChild("http.client", request.method)
            span?.setData("url", url)
            
            try {
                val response = chain.proceed(request)
                
                span?.apply {
                    setData("http.status_code", response.code)
                    status = if (response.isSuccessful) {
                        SpanStatus.OK
                    } else {
                        SpanStatus.fromHttpStatusCode(response.code)
                    }
                }
                
                if (!response.isSuccessful) {
                    Logger.logNetworkError(url, response.code, response.message)
                }
                
                return response
            } catch (e: IOException) {
                span?.apply {
                    status = SpanStatus.INTERNAL_ERROR
                    throwable = e
                }
                Logger.logError("ApiClient", "Network request failed: $url", e)
                throw e
            } finally {
                span?.finish()
            }
        }
    }
    
    // Custom logging interceptor
    private class LoggingInterceptor : Interceptor {
        override fun intercept(chain: Interceptor.Chain): Response {
            val request = chain.request()
            
            Logger.breadcrumbNetwork(
                method = request.method,
                url = request.url.toString()
            )
            
            val response = chain.proceed(request)
            
            Logger.breadcrumbNetwork(
                method = request.method,
                url = request.url.toString(),
                statusCode = response.code
            )
            
            return response
        }
    }
}
```


---

## ProGuard/R8 Configuration

**proguard-rules.pro**

```proguard
# Sentry ProGuard rules
-keepattributes LineNumberTable,SourceFile
-dontwarn org.slf4j.**
-dontwarn javax.**
-keep class io.sentry.** { *; }
-dontwarn io.sentry.**

# Keep native methods for Sentry
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep Sentry context classes
-keep class io.sentry.protocol.** { *; }
-keep class io.sentry.vendor.gson.** { *; }

# Your app specific rules
-keep class win.downops.wallettracker.** { *; }
```

---

## Testing

### 1. Test Sentry Integration

**Create a test button in your app (debug builds only):**

```kotlin
// In debug build, add test button
if (BuildConfig.DEBUG) {
    binding.btnTestSentry.setOnClickListener {
        testSentryIntegration()
    }
}

private fun testSentryIntegration() {
    try {
        // Test 1: Send a message
        Logger.log("Test message from Android app")
        
        // Test 2: Send breadcrumbs
        Logger.breadcrumb("Test breadcrumb 1")
        Logger.breadcrumb("Test breadcrumb 2")
        
        // Test 3: Send an error
        Logger.logError("TestTag", Exception("Test exception"))
        
        // Test 4: Trigger a crash (comment out if not testing)
        // throw RuntimeException("Test crash")
        
        Toast.makeText(this, "Sentry events sent! Check your Sentry dashboard.", Toast.LENGTH_LONG).show()
    } catch (e: Exception) {
        Logger.logError("TestSentry", e)
    }
}
```

### 2. Verify Events in Sentry Dashboard

1. Open Sentry: `http://your-sentry-ip:9000`
2. Go to Projects → Wallet Tracker → Issues
3. You should see your test events appearing within seconds

### 3. Test Performance Monitoring

```kotlin
fun testPerformance() {
    val transaction = Logger.startTransaction("test-transaction", "test")
    
    // Simulate some work
    Thread.sleep(100)
    
    val span = transaction.startChild("database-query")
    Thread.sleep(50)
    span.finish()
    
    transaction.finish()
    
    // Check Performance tab in Sentry dashboard
}
```

---

## Performance Monitoring

### 1. Track Activity Load Times

```kotlin
class MainActivity : AppCompatActivity() {
    private var activityTransaction: ITransaction? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        activityTransaction = Sentry.startTransaction(
            "MainActivity",
            "ui.load"
        )
        
        super.onCreate(savedInstanceState)
        
        // ... your code ...
    }
    
    override fun onResume() {
        super.onResume()
        activityTransaction?.finish()
    }
}
```

### 2. Track API Calls

```kotlin
suspend fun fetchTransactions(): List<Transaction> {
    val transaction = Logger.startTransaction("fetch-transactions", "http")
    
    try {
        val response = api.getTransactions()
        transaction.status = SpanStatus.OK
        return response
    } catch (e: Exception) {
        transaction.status = SpanStatus.INTERNAL_ERROR
        transaction.throwable = e
        throw e
    } finally {
        transaction.finish()
    }
}
```

### 3. Track Database Operations

```kotlin
fun insertTransaction(transaction: Transaction) {
    val span = Sentry.getSpan()?.startChild("db.insert", "transaction")
    
    try {
        dao.insert(transaction)
        span?.status = SpanStatus.OK
    } catch (e: Exception) {
        span?.status = SpanStatus.INTERNAL_ERROR
        Logger.logDatabaseError("insertTransaction", e)
        throw e
    } finally {
        span?.finish()
    }
}
```

---