#include <stdio.h>
#include <stdlib.h>

#define MAX 100

typedef struct {
    int data[MAX];
    int top;
} Stack;

void initialize(Stack *s) {
    s->top = -1;
}

int isFull(Stack *s) {
    return s->top == MAX - 1;
}

int isEmpty(Stack *s) {
    return s->top == -1;
}

void push(Stack *s, int value) {
    if (isFull(s)) {
        printf("Stack overflow\n");
    } else {
        s->data[++(s->top)] = value;
        printf("%d pushed to stack\n", value);
    }
}

int pop(Stack *s) {
    if (isEmpty(s)) {
        printf("Stack underflow\n");
        return -1;
    } else {
        return s->data[(s->top)--];
    }
}

int peek(Stack *s) {
    if (isEmpty(s)) {
        printf("Stack is empty\n");
        return -1;
    } else {
        return s->data[s->top];
    }
}

void display(Stack *s) {
    if (isEmpty(s)) {
        printf("Stack is empty\n");
    } else {
        printf("Stack elements are:\n");
        for (int i = s->top; i >= 0; i--) {
            printf("%d\n", s->data[i]);
        }
    }
}

int main() {
    Stack s;
    initialize(&s);
    int choice, value;

    while (1) {
        printf("\n1. Push\n2. Pop\n3. Peek\n4. Display\n5.Towers of Hanoi\n10. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to push: ");
                scanf("%d", &value);
                push(&s, value);
                break;
            case 2:
                value = pop(&s);
                if (value != -1) {
                    printf("Popped value: %d\n", value);
                }
                break;
            case 3:
                value = peek(&s);
                if (value != -1) {
                    printf("Top value: %d\n", value);
                }
                break;
            case 4:
                display(&s);
                break;
            case 5: {
                int n;
                printf("Enter number of disks: ");
                scanf("%d", &n);
                TowersofHanoi(n, 'A', 'B', 'C');
                break;
            }
            case 10:
                exit(0);
            default:
                printf("Invalid choice\n");
        }
    }

    return 0;
}

int TowersofHanoi(int n, char source, char temp, char dest) {
    static int count = 0;
    count++;
    if (n == 1) {
        printf("Move disk 1 from %c to %c\n", source, dest);
        return 0;
    }
    TowersofHanoi(n - 1, source, dest, temp);
    printf("Move disk %d from %c to %c\n", n, source, dest);
    TowersofHanoi(n - 1, temp, source, dest);
    return count;
}

