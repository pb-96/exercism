#include <string.h>
#include "list_ops.h"

list_t *new_list(size_t length, list_element_t values[])
{
    list_t *list = malloc(sizeof(*list) + sizeof(list_element_t) * length);
    if (!list)
        return NULL;
    list->length = length;
    if (values)
        memcpy(list->elements, values, sizeof(*values) * length);

    return list;
}

list_t *append_list(list_t * list1, list_t * list2)
{
    if (!list1 || !list2)
        return NULL;

    list_t *list = new_list(list1->length + list2->length, NULL);
    if (!list)
        return NULL;
    memcpy(list->elements, list1->elements, sizeof(list_element_t) * list1->length);
    memcpy(list->elements + list1->length, list2->elements, sizeof(list_element_t) * list2->length);

    return list;
}

list_t *filter_list(list_t * list, bool(*filter) (list_element_t value))
{
    if (!list)
        return NULL;

    list_t *filtered = new_list(list->length, NULL);;
    if (!filtered)
        return NULL;

    filtered->length = 0;
    for (size_t i = 0; i < list->length; i++) {
        list_element_t v = list->elements[i];
        if (filter(v))
            filtered->elements[filtered->length++] = v;
    }

    /* Probably unnecessary */
    filtered = realloc(filtered, sizeof(list_t) + sizeof(list_element_t) * filtered->length);

    return filtered;
}

size_t length_list(list_t * list)
{
    return list->length;
}

list_t *map_list(list_t * list, list_element_t(*map) (list_element_t value))
{
    list_t *mapped = new_list(list->length, NULL);
    if (!mapped)
        return NULL;

    for (size_t i = 0; i < list->length; i++)
        mapped->elements[i] = map(list->elements[i]);
    return mapped;
}


list_element_t foldl_list(list_t * list, list_element_t initial,
           list_element_t(*foldl) (list_element_t value, list_element_t initial))
{
    if (!list)
        return initial;

    for (size_t i = 0; i < list->length; i++)
        initial = foldl(list->elements[i], initial);
    return initial;
}

list_element_t foldr_list(list_t * list, list_element_t initial,
           list_element_t(*foldr) (list_element_t value, list_element_t initial))
{
    if (!list)
        return initial;

    for (int i = list->length - 1; i >= 0; i--)
        initial = foldr(list->elements[i], initial);
    return initial;
}

static void swap(list_element_t *left, list_element_t *right)
{
    list_element_t tmp = *left;
    *left = *right;
    *right = tmp;
}

list_t *reverse_list(list_t * list)
{
    if (!list)
        return NULL;

    list_t *rev = new_list(list->length, list->elements);
    if (!rev)
        return NULL;
    for (size_t i = 0; i < list->length / 2; i++)
        swap(&rev->elements[i], &rev->elements[list->length - i - 1]);
    return rev;
}

void delete_list(list_t * list)
{
    free(list);
}
