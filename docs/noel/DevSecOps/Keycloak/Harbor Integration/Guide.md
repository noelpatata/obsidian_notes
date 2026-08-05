## 1. Environment & Architecture Overview

* **Keycloak Realm:** `downops`
* **Keycloak Public URL:** `https://keycloak.downops.win`
* **Harbor Public URL:** `https://registry.downops.win`
* **Network / Edge Routing:** Cloudflare Tunnel forwarding public HTTPS traffic (`https://registry.downops.win`) to local container port (`http://localhost:5000`).
* **Authentication Standard:** OpenID Connect (OIDC) with Group Membership mapping.

---

## 2. Keycloak Configuration

### Step 2.1: Create the Harbor OIDC Client
1. Log in to the Keycloak Admin Console (`https://keycloak.downops.win`) and switch to the **`downops`** realm.
2. In the left menu, navigate to **Clients** → **Create client**.
3. **General Settings:**
   - **Client type:** `OpenID Connect`
   - **Client ID:** `harbor`
   - **Name:** `Harbor Container Registry`
4. **Capability Config:**
   - **Client authentication:** `ON` (Confidential client mode)
   - **Standard flow:** `ON`
   - **Direct access grants:** `OFF`
   - **Implicit flow:** `OFF`
   - **Service accounts roles:** `OFF` (Optional)
5. **Login Settings:**
   - **Root URL:** `https://registry.downops.win`
   - **Home URL:** `https://registry.downops.win`
   - **Valid redirect URIs:**
     - `https://registry.downops.win/c/oidc/callback`
     - `https://registry.downops.win/*`
   - **Web origins:** `https://registry.downops.win`
6. Click **Save**.

### Step 2.2: Retrieve Client Secret
1. Open the **`harbor`** client details.
2. Go to the **Credentials** tab.
3. Copy the **Client Secret** (required for Harbor setup).

### Step 2.3: Configure `groups` Client Scope & Protocol Mapper
Keycloak does not natively register `groups` as an OIDC scope unless explicitly declared.

#### Create the `groups` Client Scope:
1. Navigate to **Client scopes** in the left sidebar → **Create client scope**.
2. **Name:** `groups`
3. **Type:** `Default`
4. **Protocol:** `OpenID Connect`
5. Click **Save**.

#### Add Group Membership Mapper:
1. Inside the `groups` scope, switch to the **Mappers** tab.
2. Click **Configure a new mapper** → Select **Group Membership**.
3. **Name:** `groups`
4. **Token Claim Name:** `groups`
5. **Full group path:** `OFF` *(Ensures clean array values like `["admin"]` rather than `["/admin"]`)*
6. **Add to ID token:** `ON`
7. **Add to access token:** `ON`
8. **Add to userinfo:** `ON`
9. Click **Save**.

#### Attach Scope to Harbor Client:
1. Go back to **Clients** → **`harbor`** → **Client scopes** tab.
2. Click **Add client scope**.
3. Select `groups` → Set assignment to **Default** → Click **Add**.

---

## 3. Harbor Prerequisites & Reverse Proxy Setup

### Step 3.1: Configure `harbor.yml`
When Harbor operates behind Cloudflare Tunnel or reverse proxies terminating TLS at the edge, Harbor must be explicitly informed of its public hostname and protocol scheme.

1. Open your `harbor.yml` configuration file:
   ```yaml
   hostname: registry.downops.win
   external_url: https://registry.downops.win
   ```
2. Re-generate configuration files and restart containers:
   ```bash
   sudo ./prepare
   sudo docker compose down
   sudo docker compose up -d
   ```

### Step 3.2: Cloudflare Tunnel Configuration
Ensure Cloudflare Tunnel (`cloudflared`) passes the correct HTTP Host headers to the backend:
- **Service:** `http://localhost:5000`
- **HTTP Host Header:** `registry.downops.win`

---

## 4. Harbor OIDC Setup

1. Log into Harbor as local administrator (`admin`).
2. Navigate to **Administration** → **Configuration** → **Authentication**.
3. Set fields as follows:

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Auth Mode** | `OIDC` | Switches Harbor from local DB authentication to OIDC SSO. |
| **OIDC Provider Name** | `Keycloak` | Label displayed on the login button. |
| **OIDC Endpoint** | `https://keycloak.downops.win/realms/downops` | Base URL of Keycloak realm endpoint. |
| **OIDC Client ID** | `harbor` | Client ID configured in Keycloak. |
| **OIDC Client Secret** | `<COPIED_CLIENT_SECRET>` | Secret obtained from Keycloak Credentials tab. |
| **OIDC Scope** | `openid,profile,email,groups` | Scopes requested during authentication. |
| **OIDC Group Name Claim**| `groups` | JSON key in token payload containing user groups. |
| **OIDC Admin Group** | `admin` | Users in this Keycloak group automatically receive Harbor System Admin rights. |
| **Verify Remote Cert** | `ON` | Verifies TLS certificates (disable only if using self-signed certs). |
| **Automatic Onboarding** | `ON` | Automatically creates Harbor user accounts upon first SSO login. |

4. Click **TEST OIDC SERVER**.
5. Upon green success banner, click **SAVE**.

---

## 5. Issues & Solutions Encountered

### Issue 1: `Invalid parameter: redirect_uri`
* **Symptom:** After clicking "LOGIN VIA OIDC PROVIDER", Keycloak displays an `Invalid parameter: redirect_uri` error.
* **Root Cause Analysis:** Inspecting the authorization request revealed:
  `redirect_uri=http://registry.downops.win:5000/c/oidc/callback`
  Because Harbor did not have `external_url` configured, `harbor-core` inferred its public URL from the incoming unencrypted HTTP request sent by Cloudflare Tunnel to port `5000`. Keycloak rejected this because it did not match `https://registry.downops.win/*`.
* **Resolution:** 
  1. Configured `external_url: https://registry.downops.win` in `harbor.yml`.
  2. Executed `./prepare` and restarted Docker containers.
  3. Added `https://registry.downops.win/c/oidc/callback` to Keycloak's **Valid redirect URIs**.

---

### Issue 2: `OIDC callback returned error: invalid_scope - Invalid scopes: openid profile email groups`
* **Symptom:** Harbor returned `code: "BAD_REQUEST"` during OIDC callback phase.
* **Root Cause Analysis:** Harbor requested the `groups` scope in the OIDC request, but Keycloak had no registered `groups` Client Scope defined for the realm or attached to the `harbor` client.
* **Resolution:**
  1. Created a new Client Scope named `groups` in Keycloak.
  2. Configured a **Group Membership** mapper named `groups` inside that scope (Token Claim Name: `groups`, Full Group Path: `OFF`).
  3. Attached the `groups` scope to the `harbor` client as a **Default** client scope.

---

## 6. Authenticating with Docker CLI & Usage

Because Docker CLI does not support interactive browser redirects, human users authenticate using a **CLI Secret**.

### Step 6.1: Obtain CLI Secret
1. Log into the Harbor Web UI (`https://registry.downops.win`) via Keycloak.
2. Click your username (top right) → **User Profile**.
3. Copy the **CLI Secret**.

### Step 6.2: Docker Login
```bash
docker login registry.downops.win
```
- **Username:** Your Keycloak username
- **Password:** *Paste your CLI Secret*

### Step 6.3: Tag and Push Images
```bash
# 1. Tag image (Syntax: registry.downops.win/<project>/<image>:<tag>)
docker tag alpine:latest registry.downops.win/devops/alpine:latest

# 2. Push image to Harbor
docker push registry.downops.win/devops/alpine:latest
```

### Step 6.4: Pull Images
```bash
docker pull registry.downops.win/devops/alpine:latest
```

---

## 7. Machine-to-Machine / CI/CD Automation

For automated pipelines (GitHub Actions, GitLab CI, Kubernetes imagePullSecrets):
1. Navigate to Harbor → **Projects** → Select target project.
2. Go to **Robot Accounts** → **+ NEW ROBOT ACCOUNT**.
3. Assign appropriate permissions (`push`, `pull`).
4. Copy the generated Robot Account credentials for CI/CD authentication.