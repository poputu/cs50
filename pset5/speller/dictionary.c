// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <stddef.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 27;
int count = 0;

// Hash table
node *table[N] = {NULL};

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    unsigned int bucket = 0;
    bucket = hash(word);
    node *pointer;
    pointer = table[bucket];
    
    while (pointer != NULL)
    {
        if (strcasecmp(pointer->word, word) == 0)
        {
            // delete here free(pointer); it's somehow block to fclose(dict_sourse) at 109; 
            return true;
        }
        else
        {
            pointer = pointer->next;
        }
    }
    //free(pointer);
    return false;
}
// http://www.cse.yorku.ca/~oz/hash.html
//djb2 with check for word is here and drop value 999900000 max, edit if needed
//complitly rewrite hash function, so now I can understand it 
unsigned int hash(const char *word)
{
    if (word == NULL)
    {
        return 0;
    }
    unsigned int hash;
    if (isupper(word[0]))
    {
        hash = (word[0]) - 'A';
    }
    else
    {
        hash = word[0] - 'a';
    }
    return hash;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char d_word[46];
    FILE *dict_source = fopen(dictionary, "r");
    if (dict_source == NULL)
    {
        return false;
    }
    while (!feof(dict_source))
    {
        count++;

        //fgets (d_word, 45, dict_source);
        fscanf(dict_source, "%s", d_word);
        //printf ("%s", d_word);
        int d_hash = hash(d_word);
        node *new_word = malloc(sizeof(node)); // we can malloc less memory, but here it's not the case
        if (new_word == NULL)
        {
            printf(" can't malloc for new_word");
            return 0;
        }
        strcpy(new_word -> word, d_word);
        new_word -> next = NULL;
        if (table[d_hash] == NULL)// check if 0 word in this table bucket
        {
            table[d_hash] = new_word;
        }
        else
        {
            new_word -> next = table[d_hash] -> next; // copy first pointer
            table[d_hash] -> next = new_word; // change table pointer to point into new node
        }



    }
    
    fclose(dict_source);
    return true;
    // TODO
    //return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return count - 1;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *pointer1;
        node *pointer2;
        pointer1 = table[i];
        
        while (pointer1 != NULL)
        {
            pointer2 = pointer1;
            pointer1 = pointer1 -> next;
            free(pointer2);
        }
        
    }
    // TODO
    return true;
}
