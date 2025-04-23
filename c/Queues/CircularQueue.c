#include <stdio.h>
#include <stdlib.h>

#define SIZE 5

typedef struct {
    int items[SIZE];
    int front, rear;
} CircularQueue;

void initialize(CircularQueue *q) {
    q->front = -1;
    q->rear = -1;
}

int isFull(CircularQueue *q) {
    if (q->front == (q->rear + 1) % SIZE) {
        return 1;
    }
    return 0;
}

int isEmpty(CircularQueue *q) {
    if (q->front == -1) {
        return 1;
    }
    return 0;
}

void enqueue(CircularQueue *q, int value) {
    if (isFull(q)) {
        printf("Queue is full\n");
        return;
    }
    if (q->front == -1) {
        q->front = 0;
    }
    q->rear = (q->rear + 1) % SIZE;
    q->items[q->rear] = value;
    printf("Inserted %d\n", value);
}

int dequeue(CircularQueue *q) {
    int element;
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return -1;
    }
    element = q->items[q->front];
    if (q->front == q->rear) {
        q->front = -1;
        q->rear = -1;
    } else {
        q->front = (q->front + 1) % SIZE;
    }
    return element;
}

void display(CircularQueue *q) {
    int i;
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return;
    }
    printf("Front -> %d\n", q->front);
    printf("Items -> ");
    for (i = q->front; i != q->rear; i = (i + 1) % SIZE) {
        printf("%d ", q->items[i]);
    }
    printf("%d ", q->items[i]);
    printf("\nRear -> %d\n", q->rear);
}

int main() {
    CircularQueue q;
    initialize(&q);

    enqueue(&q, 1);
    enqueue(&q, 2);
    enqueue(&q, 3);
    enqueue(&q, 4);
    enqueue(&q, 5);

    display(&q);

    printf("Dequeued element: %d\n", dequeue(&q));
    display(&q);

    enqueue(&q, 6);
    display(&q);

    return 0;
}