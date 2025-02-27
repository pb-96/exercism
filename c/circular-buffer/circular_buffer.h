#ifndef CIRCULAR_BUFFER_H
#define CIRCULAR_BUFFER_H
#include <stdint.h>
#include <stddef.h>


typedef uint16_t buffer_value_t;
typedef struct circular_buffer_t circular_buffer_t;

circular_buffer_t* new_circular_buffer(size_t capacity);

int16_t write(circular_buffer_t* self, buffer_value_t value);
int16_t overwrite(circular_buffer_t* self, buffer_value_t value);

int16_t read(circular_buffer_t* self, buffer_value_t* value);

void clear_buffer(circular_buffer_t* self);
void delete_buffer(circular_buffer_t* self);

#endif
