#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void convert_line(char *line) {
    line[strcspn(line, "\n")] = 0;
    if (strstr(line, "int ") == line) {
        char *var_name = line + 4;
        char *semicolon = strchr(var_name, ';');
        if (semicolon) *semicolon = '\0';
        printf("\n%s = 0", var_name);
    } else if (strstr(line, "float ") == line) {
        char *var_name = line + 6;
        char *semicolon = strchr(var_name, ';');
        if (semicolon) *semicolon = '\0';
        printf("\n%s = 0.0", var_name);
    } else if (strstr(line, "printf") != NULL) {
        char *start = strstr(line, "\"");
        char *end = strrchr(line, '\"');
        if (start && end && start != end) {
            *end = 0;
            printf("\nprint(%s)", start + 1);
        }
    } else if (strstr(line, "if") != NULL) {
        char *condition = strchr(line, '(') + 1;
        char *end_condition = strchr(condition, ')');
        if (end_condition) {
            *end_condition = 0;
            printf("\nif %s:", condition);
        }
    } else if (strstr(line, "for") != NULL) {
    char *start = strchr(line, '(') + 1;
    char *end = strchr(start, ')');
    if (end) {
        *end = 0;
        char init[50], cond[50], incr[50];
        sscanf(start, "%[^;];%[^;];%[^)]", init, cond, incr);
        char var[50], start_val[50], end_val[50];
        sscanf(init, "%*s %[^=]=%s", var, start_val);
        sscanf(cond, "%*[^<]<%s", end_val);

        printf("for %s in range(%s, %s):\n", var, start_val, end_val);
    }
}

     else if (strchr(line, '=') != NULL && strchr(line, ';') != NULL) {
        char *semicolon = strchr(line, ';');
        *semicolon = '\0';
        printf("\n%s", line);
    } else if (strstr(line, "}") != NULL) {
        printf("    # End of block\n");
    } else {
        printf("# Unhandled line: %s\n", line);
    }


}
int main() {
    char line[256];
    printf("Enter C code:\n");
    while (fgets(line, sizeof(line), stdin)) {
        convert_line(line);
    }
    return 0;
}



/*SAMPLE INPUT:
int a;
float b;
printf("Hello, World!\n");
if (a > 0) {
    b = 1.5;
}
for (int i = 0; i < 10; i++) {
}
*/