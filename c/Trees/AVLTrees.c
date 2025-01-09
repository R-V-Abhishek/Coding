#include <stdio.h>
#include <stdlib.h>

// AVL Tree Node structure
struct AVLNode {
    int key;
    struct AVLNode *left;
    struct AVLNode *right;
    int balanceFactor;
};

// Function to create a new AVL tree node
struct AVLNode* createNode(int key) {
    struct AVLNode* node = (struct AVLNode*)malloc(sizeof(struct AVLNode));
    node->key = key;
    node->left = NULL;
    node->right = NULL;
    node->balanceFactor = 0; // New node is initially balanced
    return(node);
}

int height(struct AVLNode *N) {
    if (N == NULL)
        return 0;
    return N->balanceFactor;
}

int getBalance(struct AVLNode *N) {
    if (N == NULL)
        return 0;
    return height(N->left) - height(N->right);
}

// Function to right rotate subtree rooted with y
struct AVLNode *rightRotate(struct AVLNode *x) {
    struct AVLNode *y = x->left;
    struct AVLNode *sub = y->right;
    struct AVLNode *z = y->left;

    // Perform rotation
    y->right = x;
    x->left = sub;
   
    // Update balance factors
    x->balanceFactor = height(x->left) - height(x->right);
    y->balanceFactor = height(y->left) - height(y->right);

    // Return new root
    return y;
}

// Function to left rotate subtree rooted with x
struct AVLNode *leftRotate(struct AVLNode *x) {
    struct AVLNode *y = x->right;
    struct AVLNode *sub = y->left;

    // Perform rotation
    y->left = x;
    x->right = sub;

    // Update balance factors
    x->balanceFactor = getBalance(x);
    y->balanceFactor = getBalance(y);

    // Return new root
    return y;
}

// Get Balance factor of node N


// Recursive function to insert a key in the subtree rooted
// with node and returns the new root of the subtree.
struct AVLNode* insert(struct AVLNode* node, int key) {
    // 1. Perform the normal BST insertion
    if (node == NULL)
        return(createNode(key));

    if (key < node->key)
        node->left = insert(node->left, key);
    else if (key > node->key)
        node->right = insert(node->right, key);
    else // Equal keys are not allowed in BST
        return node;

    // 2. Update balance factor of this ancestor node
    node->balanceFactor = getBalance(node);

    // 3. Get the balance factor of this ancestor
    // node to check whether this node became
    // unbalanced
    int balance = getBalance(node);

    // If this node becomes unbalanced, then there
    // are 4 cases

    // Left Left Case
    if (balance > 1 && key < node->left->key)
        return rightRotate(node);

    // Right Right Case
    if (balance < -1 && key > node->right->key)
        return leftRotate(node);

    // Left Right Case
    if (balance > 1 && key > node->left->key) {
        node->left = leftRotate(node->left);
        return rightRotate(node);
    }

    // Right Left Case
    if (balance < -1 && key < node->right->key) {
        node->right = rightRotate(node->right);
        return leftRotate(node);
    }

    // return the (unchanged) node pointer
    return node;
}

// Utility function to print preorder traversal of the tree.
void preOrder(struct AVLNode *root) {
    if(root != NULL) {
        printf("%d ", root->key);
        preOrder(root->left);
        preOrder(root->right);
    }
    printf("\n");
}

// Driver program to test above functions
int main() {
    struct AVLNode *root = NULL;

    /* Constructing tree given in the above figure */
    root = insert(root, 10);
    preOrder(root);
    root = insert(root, 20);
    preOrder(root);
    root = insert(root, 30);
    preOrder(root);
    root = insert(root, 40);
    preOrder(root);
    root = insert(root, 50);
    preOrder(root);
    root = insert(root, 25);

    /* The constructed AVL Tree would be
            30
           /  \
         20   40
        /  \     \
       10  25    50
    */

    printf("Preorder traversal of the constructed AVL tree is \n");
    preOrder(root);

    return 0;
}