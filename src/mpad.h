#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <termios.h>
#include <unistd.h>

#include <termios.h>


#ifndef MPAD_H_
#define MPAD_H_

#define MPAD_VERSION "0.0.1"
#define CTRL_KEY(k) ((k) & 0x1f)

#define MPAD_TAB_STOP 8

enum editor_keys {
    BACKSPACE = 127,
    ARROW_LEFT = 1000,
    ARROW_RIGHT,
    ARROW_UP,
    ARROW_DOWN,
    DELETE_KEY,
    HOME_KEY,
    END_KEY,
    PAGE_UP,
    PAGE_DOWN
};


typedef struct editor_row {
    char *characters;
    char *render;
    size_t size;
    size_t render_size;
} editor_row;


typedef struct editor_configuration {
    size_t x_position;
    size_t y_position;
    size_t render_x_position;
    size_t row_offset;
    size_t column_offset;
    size_t screen_rows;
    size_t screen_columns;
    size_t number_rows;
    editor_row *row;
    char *filename;
    struct termios original_termios;
} editor_configuration;


typedef struct editor_buffer {
    char *data;
    ssize_t length;
} editor_buffer;


editor_configuration editor;


void quit(const char *message);

void disable_raw_mode(void);

void enable_raw_mode(void);

size_t read_key(void);

ssize_t get_terminal_size(size_t *rows, size_t *columns);

size_t convert_row_to_render(editor_row *row, size_t current_x_position);

void update_row(editor_row *row);

void append_row(char *string, size_t length);

void insert_row_character(editor_row *row, size_t index, size_t character);

void insert_character(size_t character);

char *rows_to_string(size_t *buffer_length);

void open_file(char *filename);

void save_file(void);

void append_to_buffer(editor_buffer *buffer, const char *string, ssize_t length);

void free_buffer(editor_buffer *buffer);

void draw_editor_rows(editor_buffer *buffer);

void draw_editor_status_bar(editor_buffer *buffer);

void scroll_editor(void);

void refresh_screen(void);

void move_cursor(size_t key);

void process_keypress(void);

void initialize_editor(void);


#endif
