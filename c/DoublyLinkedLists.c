#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct Node *Start = NULL;

struct Node {
    struct Node *prev;
    int info;
    struct Node *next;
};

struct Node* getNode(int n);
void insert_beginning();
void insert_second_position();
void insert_end();
void traverse();
struct Node* access_second_last();
int count();
void display_end();
void print_middle();
void print_alternate();
void swap(struct Node*, struct Node*);
void swap_alternate();
void concatenate(struct Node* Start1, struct Node* Start2);
bool check_null();
struct Node* access_end(struct Node* startNode);
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
        printf("11. Delete Middle\n12. Display Alternate\n13. Swap Alternate\n14. Concatenate\n15. Sort\n100. Exit\n");
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
                // Assume Start1 and Start2 are initialized
                // concatenate(Start1, Start2);  // Uncomment when Start1 and Start2 are defined
                break;
            case 15:
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
    struct Node* p = malloc(sizeof *p);
    if (p == NULL) {
        printf("No memory allocated.\n");
        return NULL;
    }
    p->info = n;
    p->next = p->prev = NULL;
    return p;
}



void traverse() {
    struct Node* temp = Start;
    if (temp == NULL) {
        printf("List is empty.\n");
        return;
    }
    printf("Linked list: ");
    while (temp != NULL) {
        printf("%d -> ", temp->info);
        temp = temp->next;
    }
    printf("NULL\n");
}

void insert_beginning() {
    int n;
    printf("Enter value to insert: ");
    scanf("%d", &n);
    struct Node* new_node = getNode(n);
    if (Start != NULL) {
        new_node->next = Start;
        Start->prev = new_node;
    }
    Start = new_node;
    traverse();
}

void insert_second_position() {
    int n;
    printf("Enter value to insert at second position: ");
    scanf("%d", &n);
    struct Node* new_node = getNode(n);
    if (Start == NULL) {
        Start = new_node;
    } else if (Start->next == NULL) {
        Start->next = new_node;
        new_node->prev = Start;
    } else {
        new_node->next = Start->next;
        Start->next->prev = new_node;
        Start->next = new_node;
        new_node->prev = Start;
    }
    traverse();
}

void insert_end() {
    int n;
    printf("Enter value to insert at end: ");
    scanf("%d", &n);
    struct Node* new_node = getNode(n);
    if (Start == NULL) {
        Start = new_node;
    } else {
        struct Node* last_node = access_end(Start);
        last_node->next = new_node;
        new_node->prev = last_node;
    }
    traverse();
}

void delete_front() {
    if (Start == NULL) {
        printf("List is empty!\n");
        return;
    }
    struct Node* temp = Start;
    Start = Start->next;
    if (Start != NULL) {
        Start->prev = NULL;
    }
    free(temp);
    traverse();
}

int count() {
    int i = 0;
    struct Node* temp = Start;
    while (temp != NULL) {
        i++;
        temp = temp->next;
    }
    return i;
}

void delete_end() {
    if (Start == NULL) {
        printf("List is empty!\n");
        return;
    }
    struct Node* temp = Start;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    
    temp->prev->next = NULL;

    free(temp);
    traverse();
}

void display_end() {
    if (Start == NULL) {
        printf("List is empty\n");
        return;
    }
    struct Node* last_node = access_end(Start);
    printf("Last Node: %d\n", last_node->info);
}

void print_middle() {
    int total = count();
    int middle = total / 2;
    int i = 0;
    struct Node* temp = Start;
    while (temp != NULL) {
        if (i == middle) {
            printf("Middle Node: %d\n", temp->info);
            break;
        }
        i++;
        temp = temp->next;
    }
}

void delete_middle() {
    int total = count();
    int middle = total / 2;
    int i = 0;
    struct Node* temp = Start;
    if (Start == NULL || Start->next == NULL) {
        printf("Cannot delete middle from empty or single-node list.\n");
        return;
    }
    while (temp != NULL) {
        if (i == middle) {
            if (temp->prev != NULL) temp->prev->next = temp->next;
            if (temp->next != NULL) temp->next->prev = temp->prev;
            free(temp);
            break;
        }
        i++;
        temp = temp->next;
    }
    traverse();
}

void print_alternate() {
    struct Node* temp = Start;
    int i = 0;
    printf("Alternate nodes: ");
    while (temp != NULL) {
        if (i % 2 == 0) {
            printf("%d ", temp->info);
        }
        i++;
        temp = temp->next;
    }
    printf("\n");
}

void swap(struct Node* p, struct Node* q) {
    int temp = p->info;
    p->info = q->info;
    q->info = temp;
}

void swap_alternate() {
    struct Node* temp = Start;
    while (temp != NULL && temp->next != NULL) {
        swap(temp, temp->next);
        temp = temp->next->next;
    }
}

void concatenate(struct Node* Start1, struct Node* Start2) {
    struct Node* end1 = access_end(Start1);
    if (Start2 == NULL) {
        printf("Cannot concatenate. Start2 is empty.\n");
        return;
    }
    if (end1 != NULL) {
        end1->next = Start2;
        Start2->prev = end1;
        printf("The lists have been concatenated.\n");
    } else {
        Start1 = Start2;
    }
}

bool check_null() {
    if (Start == NULL) {
        printf("List is empty!\n");
        return true;
    }
    return false;
}

struct Node* access_end(struct Node* startNode) {
    if (startNode == NULL) return NULL;
    struct Node* temp = startNode;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    return temp;
}

struct Node* access_second_last() {
    if (Start == NULL || Start->next == NULL) return NULL;
    struct Node* temp = Start;
    while (temp->next->next != NULL) {
        temp = temp->next;
    }
    return temp;
}

void bubble_sort() {
    if (check_null()) {
        return;
    }
    int swapped;
    struct Node* ptr1;
    struct Node* lptr = NULL;

    do {
        swapped = 0;
        ptr1 = Start;
        while (ptr1->next != lptr) {
            if (ptr1->info > ptr1->next->info) {
                swap(ptr1, ptr1->next);
                swapped = 1;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1;
    } while (swapped);
}
