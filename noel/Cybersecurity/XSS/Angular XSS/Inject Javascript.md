# Angular Directives & Security Cheatsheet

This cheatsheet covers common Angular directives and their security implications regarding XSS and JavaScript injection.

## 1. Types of Directives
- **Structural Directives**: Change the DOM layout (e.g., `*ngIf`, `*ngFor`).
- **Attribute Directives**: Change the appearance or behavior of elements (e.g., `ngClass`, `ngStyle`).
- **Component Directives**: A directive with a template.

### Common Directives
| Directive | Type | Purpose |
|---|---|---|
| `*ngIf` | Structural | Conditionally includes an element. |
| `*ngFor` | Structural | Iterates over a list. |
| `[ngClass]` | Attribute | Adds/removes CSS classes. |
| `[ngStyle]` | Attribute | Sets inline styles. |
| `[(ngModel)]`| Attribute | Two-way data binding (requires `FormsModule`). |

---

## 2. XSS and Security in Angular

Angular has built-in protection against XSS by sanitizing values before displaying them. However, developers can bypass these protections.

### Safe Binding (Auto-Sanitization)
Angular automatically sanitizes data when using interpolation or property binding.
```html
<!-- Angular sanitizes this to prevent XSS -->
<p>{{ userInput }}</p>
<div [textContent]="userInput"></div>
```

### Dangerous: `innerHTML` Binding
Binding directly to `innerHTML` can be dangerous if the input isn't trusted. Angular sanitizes this, but it's still a risk.
```html
<!-- Angular sanitizes this, but be cautious! -->
<div [innerHTML]="trustedHtml"></div>
```

### How to Bypass Security (The "Dangerous" Way)
If you *must* use raw HTML/JavaScript, you can use `DomSanitizer`. **WARNING**: Only use this on trusted content!

#### Component Logic:
```typescript
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

constructor(private sanitizer: DomSanitizer) {}

get safeHtml(): SafeHtml {
  return this.sanitizer.bypassSecurityTrustHtml(' ');
}
```

#### Template:
```html
<div [innerHTML]="safeHtml"></div>
```

### XSS Injection Risks
1.  **Direct DOM Manipulation**: Avoid using `document.getElementById()` or similar. Use Angular's `Renderer2` or `ElementRef`.
2.  **Attribute Injection**: Be careful with `[href]` or `[src]` if the URL is user-controlled.
    - `[href]="'javascript:alert(1)'"` will be blocked by Angular unless you bypass security.
3.  **Template Injection**: Avoid generating templates on the server-side with user-controlled data.

### Security Best Practices
- **Never** bypass security trust unless absolutely necessary and with fully sanitized data.
- **Keep Angular updated** to the latest version to benefit from security fixes.
- **Content Security Policy (CSP)**: Implement a strong CSP on your server.