# The function

``` C
void strip_ext(char *fname)
{
    char *end = fname + strlen(fname) - 1;
    int i = 0;
    while (end > fname && *end != '.') {
        printf("%d: pointer: %p value: %c\n", i, (void*)end, *end);
        ++i;
        --end;
    }
    if (end > fname) {
        *end = '\0';
}
```

# Calling the function

``` C
int main() {
    char someString[MAX_PATH] = "hello.xyz";
    strip_ext(someString);
    printf("File name without extension: %s\n", someString);
}
```
