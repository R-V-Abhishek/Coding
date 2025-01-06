#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#define MAX 100

char stk[MAX];
int top = -1;

void push(char ch) {
    if (top == MAX - 1) {
        printf("Error: Stack overflow\n");
        return;
    }
    stk[++top] = ch;
}

char pop() {
    return (top >= 0) ? stk[top--] : '\0';
}

char peek() {
    return (top >= 0) ? stk[top] : '\0';
}

int prec(char op) {
    return (op == '+' || op == '-') ? 1 : (op == '*' || op == '/') ? 2 : (op == '^') ? 3 : 0;
}

void infixToPostfix(char* in, char* post) {
    int i, j;
    for (i = 0, j = 0; in[i]; i++) {
        if (isalnum(in[i])) {
            post[j++] = in[i];
        } else if (in[i] == '(') {
            push(in[i]);
        } else if (in[i] == ')') {
            while (peek() != '(') {
                post[j++] = pop();
            }            
            pop();
        } else {
            while (prec(in[i]) <= prec(peek())) {
                post[j++] = pop();
            }
            push(in[i]);
        }
    }
    while (top >= 0) {
        post[j++] = pop();
    }
    post[j] = '\0';
    
}

int main() {
    char in[MAX], post[MAX];
    int choice;

    while (1) {
        printf("Choose an option\n1. Infix to Postfix\n10. Stop\nEnter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            exit(1);
        }

        switch (choice) {
            case 1:
                printf("Enter infix: ");
                if (scanf("%s", in) == EOF) {
                    printf("Input ended. Exiting.\n");
                    exit(0);
                }
                infixToPostfix(in, post);
                printf("Postfix: %s\n", post);
                break;
            case 10:
                printf("Exiting.\n");
                exit(0);
            default:
                printf("Invalid choice. Try again.\n");
        }
    }

    return 0;
}
