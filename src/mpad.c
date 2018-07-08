#define _GNU_SOURCE

#include "mpad.h"


/**
 * quit() - print an error messsage and exit the application
 *
 * @message: the message to print to stdout
 *
 */
void quit(const char *message) {
    // clear the screen and reposition the cursor
    write(STDOUT_FILENO, "\x1b[2J", 4);
    write(STDOUT_FILENO, "\x1b[H", 3);

    perror(message);
    exit(1);
}


/**
 * disable_raw_mode() - set the terminal configuration back to its original state
 *
 */
void disable_raw_mode(void) {
    if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &editor.original_termios) == -1) {
        quit("disable_raw_mode");
    }
}


/**
 * enable_raw_mode() - set the terminal configuration from canonical mode to raw mode
 *
 * In canonical mode, keyboard input is accepted only when the user presses enter. In
 * order to accept keyboard input after each key press, we need to set certain terminal
 * attributes with the termios header.
 *
 */
void enable_raw_mode(void) {
    if (tcgetattr(STDIN_FILENO, &editor.original_termios) == -1) {
        quit("enable_raw_mode");
    }
    atexit(disable_raw_mode);

    struct termios raw = editor.original_termios;

    // disable terminal flags that cause problems in raw mode
    raw.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);
    raw.c_oflag &= ~(OPOST);
    raw.c_cflag |= ~(CS8);
    raw.c_lflag &= ~(ECHO | ICANON | IEXTEN | ISIG);

    // set a timeout for the read() function
    raw.c_cc[VMIN] = 0;
    raw.c_cc[VTIME] = 1;

    if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw) == -1) {
        quit("tcsetattr");
    }
}


/**
 * read_key() - read key presses into the editor
 *
 * We read in each character from stdin and compare the character
 * to the escape sequence \x1b. Each escape sequence is handled
 * as a unique key press corresponding to an editor_key enum.
 * If the character is not an escape character, it is returned.
 *
 * Return: key press related to the given character
 *
 */
size_t read_key(void) {
    ssize_t read_output;
    char character;

    while ((read_output = read(STDIN_FILENO, &character, 1) != 1)) {
        if (read_output == -1 && errno != EAGAIN) {
            quit("read_key");
        }
    }

    if (character == '\x1b') {
        char sequence[3];

        if (read(STDIN_FILENO, &sequence[0], 1) != 1) {
            return '\x1b';
        }
        if (read(STDIN_FILENO, &sequence[1], 1) != 1) {
            return '\x1b';
        }

        if (sequence[0] == '[') {
            if (sequence[1] >= '0' && sequence[1] <= '9') {
                if (read(STDIN_FILENO, &sequence[2], 1) != 1) {
                    return '\x1b';
                }
                if (sequence[2] == '~') {
                    switch (sequence[1]) {
                        case '1':
                            return HOME_KEY;
                        case '2':
                            return DELETE_KEY;
                        case '4':
                            return END_KEY;
                        case '5':
                            return PAGE_UP;
                        case '6':
                            return PAGE_DOWN;
                        case '7':
                            return HOME_KEY;
                        case '8':
                            return END_KEY;
                    }
                }
        } else {
            switch (sequence[1]) {
                case 'A':
                    return ARROW_UP;
                case 'B':
                    return ARROW_DOWN;
                case 'C':
                    return ARROW_RIGHT;
                case 'D':
                    return ARROW_LEFT;
                case 'H':
                    return HOME_KEY;
                case 'F':
                    return END_KEY;
                }
            }
        } else if (sequence[0] == '0') {
            switch (sequence[1]) {
                case 'H':
                    return HOME_KEY;
                case 'F':
                    return END_KEY;
            }
        }

        return '\x1b';
    } else {
        return character;
    }
}


/**
 * get_terminal_size() - get the terminal size and set the editor size accordingly
 *
 * The terminal dimensions returned from the ioctl header are passed back to the
 * editor's rows and columns that are given as pointers.
 *
 * Return: 0 if success else -1
 */
ssize_t get_terminal_size(size_t *rows, size_t *columns) {
    struct winsize terminal_size;

    if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &terminal_size) == -1 || terminal_size.ws_col == 0) {
        return -1;
    } else {
        *rows = terminal_size.ws_row;
        *columns = terminal_size.ws_col;
        return 0;
    }
}


/**
 * convert_row_to_render() - convert a characters index into a render index
 *
 * @row: the editor row to render
 * @current_x_position: the current x position of the cursor
 *
 * In order to convert the characters index into a render index, we need
 * to subtract the number of columns past the last tab stop from the tab
 * stop minus one. This will tell us how many columns are left of the
 * next tab stop so that we can calculate where the tab stop needs to be.
 */
size_t convert_row_to_render(editor_row *row, size_t current_x_position) {
    size_t row_x_position = 0;

    for (size_t i = 0; i < current_x_position; i++) {
        if (row->characters[i] == '\t') {
            row_x_position += (MPAD_TAB_STOP - 1) - (row_x_position % MPAD_TAB_STOP);
        }
        row_x_position += 1;
    }

    return row_x_position;
}


/**
 * update_row() - fill the contents of the render string
 *
 * The contents of the characters string is copied into the render string
 * so that we are able to render tabs properly.
 *
 */
void update_row(editor_row *row) {
    size_t tabs = 0;
    for (size_t i = 0; i < row->size; i++) {
        if (row->characters[i] == '\t') {
            tabs += 1;
        }
    }

    free(row->render);
    row->render = malloc(row->size + tabs * MPAD_TAB_STOP + 1);

    size_t index = 0;
    for (size_t j = 0; j < row->size; j++) {
        if (row->characters[j] == '\t') {
            row->render[index++] = ' ';
            while (index % MPAD_TAB_STOP != 0) {
                row->render[index++] = ' ';
            }
        } else {
            row->render[index++] = row->characters[j];
        }
    }

    row->render[index] = '\0';
    row->render_size = index;
}


/**
 * insert_row() - copy the given string to the end of the editor's rows
 *
 * @string: the string to copy into the editor
 * @length: the length of the string
 *
 */
void insert_row(size_t index, char *string, size_t length) {
    if (index <= editor.number_rows) {

        editor.rows = realloc(editor.rows, sizeof(editor_row) * (editor.number_rows + 1));
        memmove(&editor.rows[index + 1], &editor.rows[index],
                sizeof(editor_row) * (editor.number_rows - index));

        editor.rows[index].size = length;
        editor.rows[index].characters = malloc(length + 1);
        memcpy(editor.rows[index].characters, string, length);
        editor.rows[index].characters[length] = '\0';

        editor.rows[index].render = NULL;
        editor.rows[index].render_size = 0;

        update_row(&editor.rows[index]);

        editor.number_rows += 1;
        editor.dirty = 1;
    }
}


/**
 * free_row() - free the given row from memory
 *
 * @row: the row to free from memory
 *
 */
void free_row(editor_row *row) {
    free(row->render);
    free(row->characters);
}


/**
 * delete_row() - delete the row at the given index from the buffer
 *
 * @index: the index of the row to delete
 *
 */
void delete_row(size_t index) {
    if (index < editor.number_rows) {
        free_row(&editor.rows[index]);
        memmove(&editor.rows[index], &editor.rows[index + 1],
                sizeof(editor_row) * (editor.number_rows - index - 1));
        editor.number_rows -= 1;
        editor.dirty = 1;
    }
}


/**
 * insert_row_character() - insert the given character into the given position in the given row
 *
 * @row: the row in which to insert the new character
 * @index: the index at which to insert the new character
 * @character: the character to insert
 *
 * We first check to make sure the position is at an index at which we can insert
 * a character. Next, the row of characters is reallocated to be able to add the
 * new character. Then, we make room for the character by using memmove on the row.
 * After the character is inserted into the row, we update the row size accordingly.
 * Finally, update_row is called so that the render and render_size fields are updated
 * with the new row content.
 *
 */
void insert_row_character(editor_row *row, size_t index, size_t character) {
    if (index > row->size) {
        index = row->size;
    }

    // add 2 so that we have space for an additional character and the null byte
    row->characters = realloc(row->characters, row->size + 2);
    memmove(&row->characters[index + 1], &row->characters[index], row->size - index + 1);
    row->characters[index] = character;
    row->size += 1;
    update_row(row);
    editor.dirty = 1;
}


/**
 * insert_character() - insert a character into the editor at the current cursor position
 *
 * @character: the character to insert
 *
 * If the cursor is at the end of the file, a new row is inserted. Once the character
 * is inserted into the row, the cursor moves to the left by one.
 *
 */
void insert_character(size_t character) {
    if (editor.y_position == editor.number_rows) {
        insert_row(editor.number_rows, "", 0);
    }

    insert_row_character(&editor.rows[editor.y_position], editor.x_position, character);
    editor.x_position += 1;
}


/**
 * insert_newline() - insert a new row when the enter key is pressed
 *
 */
void insert_newline(void) {
    if (editor.x_position == 0) {
        insert_row(editor.y_position, "", 0);
    } else {
        editor_row *row = &editor.rows[editor.y_position];
        insert_row(editor.y_position + 1,
                   &row->characters[editor.x_position],
                   row->size - editor.x_position);
        row = &editor.rows[editor.y_position];
        row->size = editor.x_position;
        row->characters[row->size] = '\0';
        update_row(row);
    }
    editor.y_position += 1;
    editor.x_position = 0;
}


/**
 * append_row_string() - append a string to the end of a row
 *
 * @row: the row in which to append the string
 * @string: the string to append
 * @length: the length of the string
 *
 */
void append_row_string(editor_row *row, char *string, size_t length) {
    row->characters = realloc(row->characters, row->size + length + 1);
    memcpy(&row->characters[row->size], string, length);
    row->size += length;
    row->characters[row->size] = '\0';
    update_row(row);
    editor.dirty = 1;
}


/**
 * delete_row_character() - delete the character in the given row at the given index
 *
 * @row: the row in which the character to delete resides
 * @index: the index of the character
 */
void delete_row_character(editor_row *row, size_t index) {
    if (index < row->size) {
        memmove(&row->characters[index], &row->characters[index + 1], row->size - index);
        row->size -= 1;
        update_row(row);
        editor.dirty = 1;
    }
}


/**
 * delete_character() - delete a character from the editor at the current cursor position
 *
 */
void delete_character(void) {
    if ((editor.y_position != editor.number_rows) ||
        (editor.x_position != 0 || editor.y_position != 0)) {

        editor_row *row = &editor.rows[editor.y_position];
        if (editor.x_position > 0) {
            delete_row_character(row, editor.x_position - 1);
            editor.x_position -= 1;
        } else {
            editor.x_position = editor.rows[editor.y_position - 1].size;
            append_row_string(&editor.rows[editor.y_position - 1], row->characters, row->size);
            delete_row(editor.y_position);
            editor.y_position -= 1;
        }
    }
}


/**
 * row_to_string() - convert the editor rows into a single string
 *
 * @buffer_length:
 *
 * The total length of all of the rows of text is added to the
 * total_length variable which is returned to the caller.
 * The required memory for the total length is allocated
 * and then the contents of each row is added to the new
 * string. Since the buffer is returned, the caller is responsible
 * for freeing the allocated memory.
 *
 * Return: the string to write to the file
 *
 */
char *rows_to_string(size_t *buffer_length) {
    size_t total_length = 0;

    for (size_t i = 0; i < editor.number_rows; i++) {
        total_length += editor.rows[i].size + 1;
    }

    *buffer_length = total_length;

    char *buffer = malloc(total_length);
    char *string = buffer;

    for (size_t j = 0; j < editor.number_rows; j++) {
        memcpy(string, editor.rows[j].characters, editor.rows[j].size);
        string += editor.rows[j].size;
        *string = '\n';
        string += 1;
    }

    return buffer;
}


/**
 * save_file() - write the string buffer to disk
 *
 */
void save_file(void) {
    if (editor.filename == NULL) {
        editor.filename = show_prompt("Save as: %s (ESC to cancel)");
        if (editor.filename == NULL) {
            set_status_message("Save aborted.");
        }
    }

    if (editor.filename != NULL) {
        size_t length;
        char *buffer = rows_to_string(&length);

        int destination_file = open(editor.filename, O_RDWR | O_CREAT, 0644);

        if (destination_file != -1) {
            if (ftruncate(destination_file, length) != -1) {
                if (write(destination_file, buffer, length) == (int) length) {
                    close(destination_file);
                    free(buffer);
                    editor.dirty = 0;
                    set_status_message("%zu bytes written to disk", length);
                }
            }
        } else {
            close(destination_file);
            free(buffer);
            set_status_message("Error writing to disk: %s", strerror(errno));
        }
    }
}


/**
 * open_file() - open a file and read its contents into line buffers
 *
 */
void open_file(char *filename) {
    free(editor.filename);
    editor.filename = strdup(filename);

    FILE *file = fopen(filename, "r");

    if (!file) {
        quit("Unable to open given filename.");
    }

    char *line = NULL;
    size_t line_capacity = 0;
    ssize_t line_length = 0;
    while ((line_length = getline(&line, &line_capacity, file)) != -1) {
        while (line_length > 0 && (line[line_length - 1] == '\n' ||
                                   line[line_length - 1] == '\r')) {
            line_length -= 1;
        }
        insert_row(editor.number_rows, line, line_length);
    }

    free(line);
    fclose(file);
    editor.dirty = 0;
}


/**
 * append_to_buffer() - append the string's contents to the buffer before writing
 *
 * @buffer: to buffer that the string will be written to
 * @string: the source string to copy into the buffer
 * @length: the length of the string that will be copied
 *
 * Space is allocated for the current buffer plus the string that will
 * be added to the buffer. The string is copied into this space and then
 * transferred to the buffer.
 *
 */
void append_to_buffer(editor_buffer *buffer, const char *string, ssize_t length)  {
    char *new_data = realloc(buffer->data, buffer->length + length);

    if (new_data != NULL) {
        memcpy(&new_data[buffer->length], string, length);
        buffer->data = new_data;
        buffer->length += length;
    }
}


/**
 * free_buffer() - free the memory held by the buffer's data
 *
 */
void free_buffer(editor_buffer *buffer) {
    if (buffer->data != NULL) {
        free(buffer->data);
        buffer->data = NULL;
    }
}


/**
 * draw_editor_rows() - draw each row of the editor to the terminal
 *
 * @buffer: the editor buffer in which to create rows
 *
 */
void draw_editor_rows(editor_buffer *buffer) {
    for (size_t row = 0; row < editor.height; row++) {
        size_t filerow = row + editor.row_offset;

        if (filerow >= editor.number_rows) {

            if (editor.number_rows == 0 && row == editor.height / 3) {
                char welcome_message[80];
                size_t welcome_length = snprintf(welcome_message, sizeof(welcome_message),
                                                 "MandeepPAD -- version %s", MPAD_VERSION);

                if (welcome_length > editor.width) {
                    welcome_length = editor.width;
                }

                // add padding so that the welcome message appears in the middle of the editor
                size_t padding = (editor.width - welcome_length) / 2;

                if (padding) {
                    append_to_buffer(buffer, "~", 1);
                    padding -= 1;
                }

                while (padding--) {
                    append_to_buffer(buffer, " ", 1);
                 }

                append_to_buffer(buffer, welcome_message, welcome_length);
            } else {
                append_to_buffer(buffer, "~", 1);
            }
        } else {
            ssize_t length = editor.rows[filerow].render_size - editor.column_offset;

            if (length < 0) {
                length = 0;
            }

            if ((size_t )length > editor.width) {
                length = editor.width;
            }

            append_to_buffer(buffer, &editor.rows[filerow].render[editor.column_offset], length);
        }

        // clear each line as we redraw the rows
        append_to_buffer(buffer, "\x1b[K", 3);
        append_to_buffer(buffer, "\r\n", 2);
    }
}


/**
 * draw_editor_status_bar() - draw a status bar at the bottom of the editor
 *
 */
void draw_editor_status_bar(editor_buffer *buffer) {
    // invert the colors of the row by using the \x1b[7m] escape sequence
    append_to_buffer(buffer, "\x1b[7m", 4);

    char status[80];
    size_t length = snprintf(status, sizeof(status), "%s %s",
                             editor.filename ? editor.filename : "[No Filename]",
                             editor.dirty ? "(modified)" : "");

    char line_number[80];
    size_t line_number_length = snprintf(line_number, sizeof(line_number), "%zu/%zu",
                                         editor.y_position + 1, editor.number_rows);

    if (length > editor.width) {
        length = editor.width;
    }

    append_to_buffer(buffer, status, length);

    while (length < editor.width) {
        if (editor.width - length == line_number_length) {
            append_to_buffer(buffer, line_number, line_number_length);
            break;
        } else {
            append_to_buffer(buffer, " ", 1);
            length += 1;
        }
    }

    // switch back to normal formatting with the \x1b[m escape sequence]
    append_to_buffer(buffer, "\x1b[m", 3);

    // add a blank line for that status message bar
    append_to_buffer(buffer, "\r\n", 2);
}


/**
 * draw_editor_status_message() - draw a status message bar beneath the message bar
 *
 * @buffer: the buffer in which to draw the bar
 */
void draw_editor_status_message(editor_buffer *buffer) {
    // clear the message bar
    append_to_buffer(buffer, "\x1b[K", 3);

    size_t message_length = strlen(editor.status_message);
    if (message_length > editor.width) {
        message_length = editor.width;
    }

    // set the message to disappear after a key is pressed but only if
    // five seconds have passed
    if (message_length && time(NULL) - editor.status_message_time < 5) {
        append_to_buffer(buffer, editor.status_message, message_length);
    }
}

/**
 * scroll_editor() - scroll the editor when the cursor has moved outside the window
 *
 * Allow the user to scroll horizontally and vertically. If the cursor comes to the end
 * of the line. The cursor moves to the next line. Likewise, if the cursor moves to the
 * beginning of a line, it will continue to move to the previous lines.
 *
 */
void scroll_editor(void) {
    editor.render_x_position = 0;

    if (editor.y_position < editor.number_rows) {
        editor.render_x_position = convert_row_to_render(&editor.rows[editor.y_position],
                                                         editor.x_position);
    }

    if (editor.y_position < editor.row_offset) {
        editor.row_offset = editor.y_position;
    }

    if (editor.y_position >= editor.row_offset + editor.height) {
        editor.row_offset = editor.y_position - editor.height + 1;
    }

    if (editor.render_x_position < editor.column_offset) {
        editor.column_offset = editor.render_x_position;
    }

    if (editor.render_x_position >= editor.column_offset + editor.width) {
        editor.column_offset = editor.render_x_position - editor.width + 1;
    }
}


/**
 * refresh_screen() - move the cursor to the beginning position and draw the editor rows
 *
 */
void refresh_screen(void) {
    editor_buffer buffer = {NULL, 0};

    scroll_editor();
    // hide the cursor prior to refreshing the screen so that the screen doesn't flicker
    append_to_buffer(&buffer, "\x1b[?25l", 6);
    append_to_buffer(&buffer, "\x1b[H", 3);

    draw_editor_rows(&buffer);
    draw_editor_status_bar(&buffer);
    draw_editor_status_message(&buffer);

    // move the cursor to the position stored in x_position and y_positon
    char buff[32];
    snprintf(buff,
            sizeof(buff),
            "\x1b[%zu;%zuH",
            editor.y_position - editor.row_offset + 1,
            editor.render_x_position - editor.column_offset + 1);
    append_to_buffer(&buffer, buff, strlen(buff));

    // show the cursor now that the writing is finished
    append_to_buffer(&buffer, "\x1b[?25h", 6);

    write(STDOUT_FILENO, buffer.data, buffer.length);
    free_buffer(&buffer);
}


/**
 * set_status_message() - set the status message of the status message bar
 *
 * @format: the format that needs to be passed to va_start and vsnprintf
 */
void set_status_message(const char *format, ...) {
    va_list ap;
    va_start(ap, format);
    vsnprintf(editor.status_message, sizeof(editor.status_message), format, ap);
    va_end(ap);
    editor.status_message_time = time(NULL);
}


/**
 * show_prompt() - show a prompt to the user when input is needed
 *
 * @prompt: the format string of the user's input
 */
char *show_prompt(char *prompt) {
    size_t prompt_size = 128;
    char *prompt_buffer = malloc(prompt_size);
    size_t prompt_length = 0;

    prompt_buffer[0] = '\0';

    while (1) {
        set_status_message(prompt, prompt_buffer);
        refresh_screen();

        size_t character = read_key();
        if (character == DELETE_KEY || character == CTRL_KEY('h') || character == BACKSPACE) {
            if (prompt_length != 0) {
                prompt_buffer[--prompt_length] = '\0';
            }
        } else if (character == '\x1b') {
            set_status_message("");
            free(prompt_buffer);
            return NULL;
        } else if (character == '\r') {
            if (prompt_length != 0) {
                set_status_message("");
                return prompt_buffer;
            }
        } else if (!iscntrl(character) && character < 128) {
            if (prompt_length == prompt_size - 1) {
                prompt_size *= 2;
                prompt_buffer = realloc(prompt_buffer, prompt_size);
            }
            prompt_buffer[prompt_length++] = character;
            prompt_buffer[prompt_length] = '\0';
        }
    }
}


/**
 * move_cursor() - move the cursor when given the up, down, left, or right arrow keys
 *
 * @key: the last key pressed by the user
 *
 */
void move_cursor(size_t key) {
    editor_row *row = editor.y_position > editor.number_rows ? NULL : &editor.rows[editor.y_position];

    switch (key) {
        case ARROW_LEFT:
            if (editor.x_position != 0) {
                editor.x_position -= 1;
            } else if (editor.y_position > 0) {
                editor.y_position -= 1;
                editor.x_position = editor.rows[editor.y_position].size;
            }
            break;
        case ARROW_RIGHT:
            if (row && editor.x_position < row->size) {
                editor.x_position += 1;
            } else if (row && editor.x_position == row->size) {
                editor.y_position += 1;
                editor.x_position = 0;
            }
            break;
        case ARROW_UP:
            if (editor.y_position != 0) {
                editor.y_position -= 1;
            }
            break;
        case ARROW_DOWN:
            if (editor.y_position < editor.number_rows) {
                editor.y_position += 1;
            }
            break;
    }

    row = editor.y_position >= editor.number_rows ? NULL : &editor.rows[editor.y_position];
    size_t row_length = row ? row->size : 0;
    if (editor.x_position > row_length) {
        editor.x_position = row_length;
    }
}


/**
 * process_keypress() - wait for a keypress and handle it accordingly
 *
 * The key is read in by the read_key() function and handled in the process_keypress()
 * function.
 *
 */
void process_keypress(void) {
    static size_t quit_keypresses = MPAD_QUIT_KEYPRESSES;

    size_t character = read_key();

    switch (character) {
        case '\r':
            insert_newline();
            break;

        case CTRL_KEY('q'):
            if (editor.dirty && quit_keypresses > 0) {
                set_status_message("File has unsaved changes. "
                                   "Press Ctrl+Q one more time to quit.");
                quit_keypresses -= 1;
                return;
            } else {
                write(STDOUT_FILENO, "\x1b[2J", 4);
                write(STDOUT_FILENO, "\x1b[H", 3);
                exit(0);
            }
            break;

        case CTRL_KEY('s'):
            save_file();
            break;

        case HOME_KEY:
            editor.x_position = 0;
            break;

        case END_KEY:
            if (editor.y_position < editor.number_rows) {
                editor.x_position = editor.rows[editor.y_position].size;
            }
            break;

        case BACKSPACE:
        case CTRL_KEY('h'):
        case DELETE_KEY:
            if (character == DELETE_KEY) {
                move_cursor(ARROW_RIGHT);
            }
            delete_character();
            break;

        case PAGE_UP:
        case PAGE_DOWN:
            {
                if (character == PAGE_UP) {
                    editor.y_position = editor.row_offset;
                } else if (character == PAGE_DOWN) {
                    editor.y_position = editor.row_offset + editor.height - 1;
                    if (editor.y_position > editor.number_rows) {
                        editor.y_position = editor.number_rows;
                    }
                }
                size_t times = editor.height;
                while (times--) {
                    move_cursor(character == PAGE_UP ? ARROW_UP : ARROW_DOWN);
                }
            }
            break;

        case ARROW_UP:
        case ARROW_DOWN:
        case ARROW_LEFT:
        case ARROW_RIGHT:
            move_cursor(character);
            break;

        case CTRL_KEY('l'):

        case '\x1b':
            break;

        default:
            insert_character(character);
            break;
    }
    quit_keypresses = MPAD_QUIT_KEYPRESSES;
}

/**
 * initialize_editor() - initialize the editor to its default state
 *
 */
void initialize_editor(void) {
    editor.x_position = 0;
    editor.y_position = 0;
    editor.render_x_position = 0;
    editor.row_offset = 0;
    editor.column_offset = 0;
    editor.number_rows = 0;
    editor.rows = NULL;
    editor.dirty = 0;
    editor.filename = NULL;
    editor.status_message[0] = '\0';
    editor.status_message_time = 0;

    if (get_terminal_size(&editor.height, &editor.width) == -1) {
        quit("get_terminal_size");
    }

    // decrement screen rows by 2 so that there are two extra lines
    // in which to draw the status bar and status message
    editor.height -= 2;
}


int main(int argc, char **argv) {
    enable_raw_mode();
    initialize_editor();

    if (argc >= 2) {
        open_file(argv[1]);
    }

    set_status_message("HELP: Ctrl+S to save | Ctrl+Q to quit");

    while (1) {
        refresh_screen();
        process_keypress();
    }
}
