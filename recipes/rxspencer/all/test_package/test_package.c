#include <rxspencer/regex.h>
#include <stdio.h>

int main() {
    const char *test_string = "123";
    regex_t regex;
    int ret = 1;

    if (0 != regcomp(&regex, "^[0-9]+$", REG_EXTENDED)) {
        printf("Regex compilation failed\n");
        return 1;
    }
    ret = regexec(&regex, test_string, 0, NULL, 0);
    if (0 == ret) {
        printf("String matches the pattern\n");
    } else {
        printf("String does not match the pattern\n");
    }

    regfree(&regex);
    return ret;
}
