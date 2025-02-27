#include "word_count.h"
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stddef.h>

#define STRING_SIZE (MAX_WORD_LENGTH + 1)

char* parse_un_wanted_strings(const char *sequence) {
    static char space[STRING_SIZE];
    size_t idx = 0;
    size_t len = strlen(sequence);

    for (size_t ptr = 0; ptr < len; ptr++) {
        char c = sequence[ptr];
        if ((c >= '0' && c <= '9') == 1) {
            space[idx++] = c;
        }
        else if (isalpha(c) == 1) {
            space[idx++] = tolower(c);
        }
        else if (c == '\'' && ptr > 0 && ptr + 1 < len && isalpha(sequence[ptr - 1]) && isalpha(sequence[ptr + 1])) {
            space[idx++] = c;
        }
        else if (c == ' ' && idx > 0 && space[idx - 1] != ' ') {
            space[idx++] = c;
        }
        else if (c == ',' && idx > 0 && space[idx - 1] != ' ') {
            space[idx++] = ' ';
        }
        else if (c == '\n') {
            continue;
        }
    }

    space[idx] = '\0';
    return space;
}

void slice(const char* str, char* result, size_t start, size_t end) {
    size_t len = 0;
    if (end == 0 ) len = end;
    else if (end > 0 ) len = end - start;
    strncpy(result, str + start, len);
    result[len] = '\0';
}


int append_to_struct(const char *sentence, int16_t found, size_t start_point, word_count_word_t *words, int index) {
    char sliced_char[STRING_SIZE] = "";
    slice(sentence, sliced_char, found, start_point);

    int dup_count = 0;
    for (int i = 0; i < index; i++) {
        if ( strcmp(words[i].text, sliced_char) == 0 ) {
            dup_count++;
            words[i].count++;
            break;
        }
    }

    if (dup_count > 0) {
        return 0;
    }

    strncpy(words[index].text ,sliced_char, STRING_SIZE);
    words[index].count = 1;
    index++;
    return index;
}


int count_words(const char *sentence, word_count_word_t *words) {
    int start_point = 0;
    int16_t found = 0;
    int index = 0; 
    char* new_sequence = parse_un_wanted_strings(sentence);
    int len = strlen(new_sequence);

    while ( start_point <= len ) {
        if (isspace((unsigned char)new_sequence[start_point]) ) {
            int tmp = append_to_struct(new_sequence, found, start_point, words, index);
            if (tmp > 0) {
                index = tmp;
            }
            found = start_point + 1;
        };
        start_point++;
    }

    unsigned short us_val = (unsigned short)found;
    if ( us_val < strlen(sentence) ) {
        int tmp = append_to_struct(new_sequence, found, start_point, words, index);
        if (tmp > 0) {
            index = tmp;
        }
    }
    
    return index;
}
