#include "binary_search_tree.h"
#include <stdlib.h>
//test
static node_t *NewNode(int Number);
static node_t *Branch(int Number, node_t *Tree);
static int Sort(int size, node_t *Tree, int *data);

node_t *build_tree(int *tree_data, size_t tree_data_len)
{
   int TreeSize = tree_data_len;
   int Count;

   node_t *Tree;
   Tree = malloc(sizeof(struct node));

   free_tree(Tree);

   for(Count = 0; Count < TreeSize; Count++)
   {
        Tree = Branch(tree_data[Count], Tree);
   }

   return Tree;
}

static node_t *NewNode(int Number)
{
   node_t *TempNode;
   TempNode = malloc(sizeof(struct node));
   TempNode->data = Number;
   TempNode->right = NULL;
   TempNode->left = NULL;

   return TempNode;
}

static node_t *Branch(int Number, node_t *Tree)
{
   if(Tree->data == 0)
   {
        return NewNode(Number);
   }

   if(Tree->data >= Number)
   {
      if(Tree->left != NULL)
      {
        Branch(Number, Tree->left);
      }
      else
      {
        Tree->left = NewNode(Number);
      }
   }

   if(Tree->data < Number)
   {
      if(Tree->right != NULL)
      {
        Branch(Number, Tree->right);
      }
      else
      {
        Tree->right = NewNode(Number);
      }
   }

   return Tree;
}

void free_tree(node_t *Erase_Tree)
{
   Erase_Tree->data = 0;
   Erase_Tree->right = NULL;
   Erase_Tree->left = NULL;
}

int *sorted_data(node_t *tree)
{
   int *Sorted_Data;
   int element = 0;

   Sorted_Data = (int *)malloc(100*sizeof(int));

   Sort(element, tree, Sorted_Data);

   return Sorted_Data;
}

static int Sort(int element, node_t *Tree, int *dataArray)
{
   if(Tree->left != NULL)
   {
        element = Sort(element, Tree->left, dataArray);
   }

   dataArray[element++] = Tree->data;

   if(Tree->right != NULL)
   {
        element = Sort(element, Tree->right, dataArray);
   }

   return element;
}

