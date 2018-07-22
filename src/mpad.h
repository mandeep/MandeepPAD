#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>


#ifndef MPAD_H_
#define MPAD_H_


#define MPAD_VERSION "0.0.5"
#define CTRL_KEY(k) ((k) & 0x1f)
#define MPAD_TAB_STOP 8
#define MPAD_QUIT_KEYPRESSES 1

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


/**
 * editor_row - data type for storing a row of text in the editor
 *
 * @characters: the characters in the row
 * @render: the actual characters to draw on the screen (accounting for tabs)
 * @size: the number of characters in the row
 * @render_size: the length of the contents in render
 */
typedef struct editor_row {
    char *characters;
    char *render;
    size_t size;
    size_t render_size;
} editor_row;


/**
 * editor_configuration - the settings for the editor instance
 *
 * @x_position: the position of the cursor on the x-axis (top left is origin)
 * @y_position: the position of the cursor on the y-axis
 * @render_x_position: the index into the render field of the editor row
 * @row_offset: the row where the cursor is currently positioned
 * @column_offset: the column where the cursor is currently positioned
 * @height: the screen height of the editor
 * @width: the screen width of the editor
 * @number_rows: the total number of rows in the editor that are filled with characters
 * @rows: the lines in all of the rows in the editor
 * @filename: the filename of the file currently read into the buffer
 * @status_message: the status message that will be displayed on screen
 * @status_message_time: the timestamp when the status message is displayed
 * @original_termios: the original terminal attributes before modification
 *
 */
typedef struct editor_configuration {
    size_t x_position;
    size_t y_position;
    size_t render_x_position;
    size_t row_offset;
    size_t column_offset;
    size_t height;
    size_t width;
    size_t number_rows;
    editor_row *rows;
    size_t dirty;
    char *filename;
    char status_message[80];
    time_t status_message_time;
    struct termios original_termios;
} editor_configuration;


/**
 * editor_buffer - the buffer that contains all of the characters prior to writing
 *
 * @data: the data held by the buffer
 * @length: the length of the buffer
 *
 */
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

void insert_row(size_t index, char *string, size_t length);

void free_row(editor_row *row);

void delete_row(size_t index);

void insert_row_character(editor_row *row, size_t index, size_t character);

void insert_character(size_t character);

void append_row_string(editor_row *row, char *string, size_t length);

void insert_newline(void);

void delete_row_character(editor_row *row, size_t index);

void delete_character(void);

char *rows_to_string(size_t *buffer_length);

void open_file(char *filename);

void save_file(void);

void append_to_buffer(editor_buffer *buffer, const char *string, ssize_t length);

void free_buffer(editor_buffer *buffer);

void draw_editor_rows(editor_buffer *buffer);

void draw_editor_status_bar(editor_buffer *buffer);

void draw_editor_status_message(editor_buffer *buffer);

void scroll_editor(void);

void refresh_screen(void);

void set_status_message(const char *format, ...);

char *show_prompt(char *prompt);

void move_cursor(size_t key);

void process_keypress(void);

void initialize_editor(void);


#endif
