#include <stdio.h>
#include <string.h>

void convert_python_to_c(const char *python_code) {
    char line[256];
    char var_name[50];
    int a, b;
    char *line_ptr = strtok((char *)python_code, "\n");
    while (line_ptr != NULL) {
        strcpy(line, line_ptr);
        if (strstr(line, "=")) {
            sscanf(line, "%[^=]=%d", var_name, &a);
            printf("%s = %d;\n", var_name, a);
        }
        else if (strstr(line, "print")) {
            char message[100];
            sscanf(line, "print(%[^\n])", message);
            printf("printf(%s);\n", message);
        }
        line_ptr = strtok(NULL, "\n");
    }
}
int main() {
    const char *python_code = 
        "num1 = 5\n"
        "num2 = 10\n"
        "result = num1 + num2\n"
        "print(\"The sum is: \", result)\n";

    printf("C code generated from Python code:\n");
    convert_python_to_c(python_code);

    return 0;
}