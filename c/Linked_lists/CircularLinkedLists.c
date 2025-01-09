#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct Node *last = NULL;

struct Node {
    int info;
    struct Node *next;
};

struct Node* getNode(int n);
void insert_beginning();
void insert_second_position();
void insert_end();
void traverse();
int count();
void display_end();
void print_middle();
void print_alternate();
void swap(struct Node*, struct Node*);
void swap_alternate();
bool check_null();
void bubble_sort();
void delete_front();
void delete_end();
void delete_middle();

void main() {
    int choice, n;
    struct Node *p;

    do {
        printf("\nMenu:\n");
        printf("1. Get Node\n2. Insert at Beginning\n3. Insert at Second Position\n4. Display All\n5. Display End\n");
        printf("6. Insert at End\n7. Delete First Node\n8. Count Nodes\n9. Delete End\n10. Print Middle\n");
        printf("11. Delete Middle\n12. Display Alternate\n13. Swap Alternate\n14. Sort\n100. Exit\n");
        printf("Enter a choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the value of n: ");
                scanf("%d", &n);
                p = getNode(n);
                break;
            case 2:
                insert_beginning();
                break;
            case 3:
                insert_second_position();
                break;
            case 4:
                traverse();
                break;
            case 5:
                display_end();
                break;
            case 6:
                insert_end();
                break;
            case 7:
                delete_front();
                break;
            case 8:
                printf("Number of nodes in the list: %d\n", count());
                break;
            case 9:
                delete_end();
                break;
            case 10:
                print_middle();
                break;
            case 11:
                delete_middle();
                break;
            case 12:
                print_alternate();
                break;
            case 13:
                swap_alternate();
                traverse();
                break;
            case 14:
                bubble_sort();
                traverse();
                break;
            case 100:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid Option.\n");
                break;
        }
    } while (choice != 100);
}

struct Node* getNode(int n) {
    struct Node* p = (struct Node*)malloc(sizeof(struct Node));
    if (p == NULL) {
        printf("No memory allocated.\n");
        return NULL;
    }
    p->info = n;
    p->next = p;  // Point to itself for a new single-node circular list
    return p;
}

void traverse() {
    if (last == NULL) {
        printf("List is empty.\n");
        return;
    }
    struct Node* temp = last->next;
    printf("Circular linked list: ");
    do {
        printf("%d -> ", temp->info);
        temp = temp->next;
    } while (temp != last->next);
    printf("(back to start)\n");
}

void insert_beginning() {
    int n;
    printf("Enter value to insert at beginning: ");
    scanf("%d", &n);
    struct Node* new_node = getNode(n);
    if (last == NULL) {
        last = new_node;
    } else {
        new_node->next = last->next;
        last->next = new_node;
    }
    traverse();
}

void insert_second_position() {
    int n;
    printf("Enter value to insert at second position: ");
    scanf("%d", &n);
    struct Node* new_node = getNode(n);
    if (last == NULL) {
        last = new_node;
    } else {
        new_node->next = last->next->next;
        last->next->next = new_node;
    }
    traverse();
}

void insert_end() {
    int n;
    printf("Enter value to insert at end: ");
    scanf("%d", &n);
    struct Node* new_node = getNode(n);
    if (last == NULL) {
        last = new_node;
    } else {
        new_node->next = last->next;
        last->next = new_node;
        last = new_node;
    }
    traverse();
}

void delete_front() {
    if (last == NULL) {
        printf("List is empty!\n");
        return;
    }
    struct Node* temp = last->next;
    if (last->next == last) {
        last = NULL;
    } else {
        last->next = temp->next;
    }
    free(temp);
    traverse();
}

int count() {
    if (last == NULL) return 0;
    int i = 1;
    struct Node* temp = last->next;
    while (temp != last) {
        i++;
        temp = temp->next;
    }
    return i;
}

void delete_end() {
    if (last == NULL) {
        printf("List is empty!\n");
        return;
    }
    struct Node* temp = last->next;
    if (last->next == last) {
        free(last);
        last = NULL;
    } else {
        while (temp->next != last) {
            temp = temp->next;
        }
        temp->next = last->next;
        free(last);
        last = temp;
    }
    traverse();
}

void display_end() {
    if (last == NULL) {
        printf("List is empty\n");
        return;
    }
    printf("Last Node: %d\n", last->info);
}

void print_middle() {
    int total = count();
    int middle = total / 2;
    int i = 0;
    struct Node* temp = last->next;
    while (i < middle) {
        temp = temp->next;
        i++;
    }
    printf("Middle Node: %d\n", temp->info);
}

void delete_middle() {
    int total = count();
    int middle = total / 2;
    int i = 0;
    if (last == NULL || last->next == last) {
        printf("Cannot delete middle from empty or single-node list.\n");
        return;
    }
    struct Node* temp = last->next;
    while (i < middle - 1) {
        temp = temp->next;
        i++;
    }
    struct Node* temp1 = temp->next;
    temp->next = temp1->next;
    if (temp1 == last) last = temp;
    free(temp1);
    traverse();
}

void print_alternate() {
    if (last == NULL) return;
    struct Node* temp = last->next;
    int i = 0;
    printf("Alternate nodes: ");
    do {
        if (i % 2 == 0) printf("%d ", temp->info);
        temp = temp->next;
        i++;
    } while (temp != last->next);
    printf("\n");
}

void swap(struct Node* p, struct Node* q) {
    int temp = p->info;
    p->info = q->info;
    q->info = temp;
}

void swap_alternate() {
    if (last == NULL || last->next == last) return;
    struct Node* temp = last->next;
    do {
        if (temp->next != last->next) {
            swap(temp, temp->next);
            temp = temp->next->next;
        } else {
            break;
        }
    } while (temp != last->next && temp->next != last->next);
}

bool check_null() {
    if (last == NULL) {
        printf("List is empty!\n");
        return true;
    }
    return false;
}

void bubble_sort() {
    if (check_null()) return;

    int swapped;
    struct Node *ptr1, *lptr = last;

    do {
        swapped = 0;
        ptr1 = last->next;

        while (ptr1->next != last->next && ptr1->next != lptr) {
            if (ptr1->info > ptr1->next->info) {
                swap(ptr1, ptr1->next);
                swapped = 1;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1; // Move lptr to the last sorted node.
    } while (swapped);
}


void reverse_list(){
    if (last == NULL) return;
    struct Node* temp = last->next;
    struct Node* prev = NULL;
    struct Node* next = NULL;
    while (temp != last) {
        next = temp->next;
        temp->next = prev;
        prev = temp;
        temp = next;
    }
    last->next = prev;
    last = temp;
}