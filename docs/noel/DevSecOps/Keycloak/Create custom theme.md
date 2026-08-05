# Creating a Custom Keycloak Theme

## 1. Disable Theme Caching (Development)

By default Keycloak caches themes. During development, disable caching so changes appear on browser refresh without restarting the container.

In `docker-compose.yml`, add these flags to the `keycloak` service `command`:

```yaml
command:
  - start
  - --spi-theme-static-max-age=-1
  - --spi-theme-cache-themes=false
  - --spi-theme-cache-templates=false
```

For Java-based configs:

```bash
/opt/keycloak/bin/kc.sh start \
  --spi-theme-static-max-age=-1 \
  --spi-theme-cache-themes=false \
  --spi-theme-cache-templates=false
```

---

## 2. Create the Theme Directory

Mount a local `themes/` folder into the container at `/opt/keycloak/themes`.

**docker-compose.yml:**

```yaml
services:
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    # ...
    volumes:
      - ./themes:/opt/keycloak/themes
```

**Directory structure:**

```
themes/
└── downops/
    └── login/
        ├── theme.properties
        ├── login.ftl                  (optional — custom HTML)
        ├── messages/
        │   └── messages_en.properties (optional — custom labels)
        └── resources/
            ├── css/
            │   └── custom.css
            └── img/
                ├── logo.svg
                └── bg.svg
```

The theme name is the directory name (`downops`). The `login/` subfolder scopes it to login pages. Other types (`email/`, `account/`, `admin/`) exist but are out of scope here.

---

## 3. Configure `theme.properties`

File: `themes/downops/login/theme.properties`

```properties
parent=keycloak.v2
styles=css/custom.css
```

- **`parent`** — Inherit from Keycloak's built-in theme (`keycloak.v2` for modern Keycloak 21+, `keycloak` for older). You only override what you specify; everything else falls back to the parent.
- **`styles`** — Space-separated list of CSS files (relative to `resources/`). Appended **after** the parent's stylesheets.

Other useful properties:

```properties
import=2.0
locales=en,fr,es
```

---

## 4. Add Custom CSS

File: `themes/downops/login/resources/css/custom.css`

```css
/* Dark page background with SVG image */
.login-pf body,
body {
  background: #0b1120 !important;
  background-image: url('../img/bg.svg') !important;
  background-size: cover !important;
}

/* Glass-style login card */
.card-pf,
.pf-v5-c-login__main {
  background-color: rgba(17, 24, 39, 0.92) !important;
  backdrop-filter: blur(6px);
  border-radius: 14px !important;
  border: 1px solid #1f2937 !important;
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.55) !important;
  padding: 28px !important;
}

/* Custom primary button */
#kc-login,
.pf-v5-c-button--primary {
  background-color: #d97706 !important;
  border-color: #d97706 !important;
  color: #1f1300 !important;
  border-radius: 8px !important;
  font-weight: 700 !important;
}

#kc-login:hover {
  background-color: #f59e0b !important;
}

/* Replace text logo with image logo */
.kc-logo-text {
  display: none !important;
}

#kc-header-wrapper {
  content: url('../img/logo.svg') !important;
  max-width: 220px;
  margin: 0 auto 24px auto !important;
}

/* Input fields */
input[type="text"],
input[type="password"],
input[type="email"] {
  background-color: #0f172a !important;
  border: 1px solid #334155 !important;
  border-radius: 8px !important;
  color: #e2e8f0 !important;
  padding: 11px 13px !important;
}

input:focus {
  outline: none !important;
  border-color: #f59e0b !important;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.25) !important;
}

/* Links */
a,
.pf-v5-c-link {
  color: #fbbf24 !important;
}

a:hover {
  color: #f59e0b !important;
  text-decoration: underline;
}
```

> `!important` is generally needed because the parent theme's styles load first.
> Keycloak 21+ uses PatternFly v5 (`pf-v5-*` classes). Older versions use `pf-c-*` (v4). Inspect the rendered page to identify which applies.

---

## 5. Add a Logo

Place your logo at:

```
themes/downops/login/resources/img/logo.svg
```

SVG is recommended (scales cleanly, small size). PNG also works.

Reference it in CSS:

```css
#kc-header-wrapper {
  content: url('../img/logo.svg') !important;
  max-width: 220px;
  margin: 0 auto 24px auto !important;
}
```

To change the logo later, just overwrite `logo.svg`. No code changes needed.

---

## 6. Add a Background

Place at `themes/downops/login/resources/img/bg.svg` and reference in CSS:

```css
body {
  background: url('../img/bg.svg') no-repeat center center fixed !important;
  background-size: cover !important;
}
```

---

## 7. Customize UI Labels (Text)

File: `themes/downops/login/messages/messages_en.properties`

```properties
loginAccountTitle=DownOps \u00b7 Sign in
usernameOrEmail=Operator email / username
password=Passphrase
doLogIn=Sign in
doRegister=Request access
doForgotPassword=Recover access
backToLogin=Return to login
```

### Important rules

- **Plain text only** — `.properties` files are not HTML. Keycloak outputs values verbatim into FreeMarker templates.
- **No HTML entities** — `&middot;` will render literally as the text `&middot;`, not `·`.
- **Use Unicode escapes** for special characters:

| Want | Write |
|------|-------|
| `·`  | `\u00b7` |
| `—`  | `\u2014` |
| `→`  | `\u2192` |
| `&`  | `\u0026` (or just `&` works in most contexts) |
| `'`  | `'` (single-quote, no escape needed) |

- **Locale per file** — `messages_en.properties` for English, `messages_fr.properties` for French, etc. Declare supported locales in `theme.properties`: `locales=en,fr,es`.

---

## 8. Custom HTML Layout (Advanced)

To change the HTML structure (not just styling), copy a FreeMarker template from the parent theme into your theme directory and edit it.

```bash
# Inside the running container, list the built-in templates:
docker exec keycloak ls /opt/keycloak/lib/quarkus/dist/deployed/keycloak-theme/login/

# Copy one out to your theme:
docker exec keycloak cat /opt/keycloak/lib/quarkus/dist/deployed/keycloak-theme/login/login.ftl \
  > themes/downops/login/login.ftl
```

Common templates to override:

| Template          | What it controls                          |
|-------------------|-------------------------------------------|
| `login.ftl`      | Main login form layout                     |
| `template.ftl`    | Outer page shell (head, header, footer)    |
| `login-username.ftl` | Username-only step (first factor)      |
| `login-password.ftl` | Password-only step (second factor)     |
| `register.ftl`    | Registration form                          |
| `login-config-totp.ftl` | TOTP setup page                       |
| `error.ftl`       | Error page                                 |
| `info.ftl`        | Info / success page                        |

Only copy the templates you actually change. Everything else falls back to the parent.

---

## 9. Activate the Theme

1. Log into the Keycloak Admin Console (`https://keycloak.example.com/admin`).
2. Select your realm from the dropdown (top-left).
3. Go to **Realm Settings → Themes**.
4. Set **Login Theme** to `downops` (the directory name).
5. Click **Save**.

The new theme takes effect immediately for new login flows. Existing sessions may need to re-authenticate to see it.

---

## 10. Reload Behavior

| What you change                          | Reload needed                          |
|------------------------------------------|----------------------------------------|
| CSS, images, SVG                         | Browser refresh (live, no restart)    |
| `theme.properties`                       | Browser refresh (live)                |
| FreeMarker templates (`*.ftl`)            | Browser refresh (live)                |
| `messages_*.properties` (labels, titles)  | **Container restart required**         |

To restart the container:

```bash
docker compose -f /root/keycloak/docker-compose.yml restart keycloak
```

The `--spi-theme-cache-*` flags enable live reload for static and template resources, but Java's `ResourceBundle` caches message bundles in the JVM until restart.

---

## 11. Production Notes

Before going to production:

1. **Remove the caching disable flags** from `docker-compose.yml`:

   ```yaml
   command: start
   ```

   These flags hurt performance and bypass static asset caching. Keep them only for dev.

2. **Minify CSS** if the file is large.

3. **Test all flows** — login, registration, password reset, TOTP setup, error pages, info pages. Each can have edge-case styling.

4. **Test multiple browsers** — backdrop-filter and some modern CSS features may need vendor prefixes.

5. **Verify the bundle mounts** — `docker exec keycloak ls /opt/keycloak/themes/downops/login/` should list your files.

---

## 12. Troubleshooting

### Theme doesn't appear in the dropdown
- Verify the `theme.properties` file exists at `themes/<name>/login/theme.properties`.
- Check the Docker volume mount: `docker exec keycloak ls /opt/keycloak/themes/`.
- Restart Keycloak after adding a new theme directory.

### Styles not applying
- Open browser DevTools → Network tab. Confirm `custom.css` loads with HTTP 200.
- Confirm `theme.properties` lists the path correctly: `styles=css/custom.css`.
- Check CSS specificity — the parent theme may win. Add `!important` or use more specific selectors.

### `&middot;` shows as literal text
- `.properties` files are plain text. Use `\u00b7` instead of `&middot;`.

### Image broken
- Confirm the path in CSS matches the file location under `resources/`.
- SVG must be valid XML. Open it directly in the browser to verify.
- Check the Network tab for 404s.

### Changes not showing
- Hard refresh the browser (Ctrl+Shift+R or Cmd+Shift+R).
- Confirm caching is disabled (dev flags present).
- For label changes, restart the container.
