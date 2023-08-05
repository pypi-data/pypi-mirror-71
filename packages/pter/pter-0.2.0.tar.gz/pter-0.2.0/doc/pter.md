# pter

The commandline GUI for pytodotxt is called pter and you can start it by
providing your todo.txt to it:

    pter ~/todo.txt

In the GUI you can edit tasks, create new ones, and [search](searching.md)
through the tasks.

The behaviour of the GUI can be configured to some extend, please see below in
the section *Configuration* for details.


## Task creation / editing

pter supports extra features when creating tasks.

### Relative dates

Instead of providing full dates for `due:` or `t:`, you may write things like
`due:+4d`, for example, to specify a date in 4 days.

The suffix `d` stands for days, `w` for weeks, `m` for months, `y` for years.
The leading `+` is implied when left out and if you don’t specify it, `d` is
assumed.

`due` and `t` tags can be as trivial as `due:1` (short for `due:+1d`, ie.
tomorrow) or as complicated as `due:+15y-2m+1w+3d` (two months before the date
that is in 15 years, 1 week and 3 days).

`due` and `t` also support relative weekdays. If you specify `due:sun` it is
understood that you mean the next Sunday. If today is Sunday, this is
equivalent to `due:1w` or `due:+7d`.

With any of these relative days, pter will calculate the exact date for
you and put it in place to be compatible with the standard todo.txt format.


## Time tracking

pter can track the time you spend on a task, By default, type `t` to
start tracking. This will add a `tracking:` attribute with the current local
date and time to the task.

When you select that task again and type `t`, the `tracking:` tag will be
removed and the time spent will be saved in the tag `spent:` as hours and
minutes.

If you start and stop tracking multiple times, the time in `spent:` will
accumulate accordingly. The smallest amount of time tracked is one minute.

This feature is non-standard for todo.txt but compatible with every other
implementation.


## Keyboard controls

Unless configured otherwise by you, the following keyboard controls are
available:

 - `↑`, `↓` (cursor keys): select the next or previous task in the list
 - `Home`: go to the first task
 - `End`: go the last task
 - `e`: edit the currently selected task
 - `n`: create a new task
 - `/`: edit the search query
 - `q`: quit the program
 - `:`: jump to a list entry by number
 - `l`: load a named search
 - `s`: save the current search
 - `u`: open a URL listed in the selected task
 - `t`: Start/stop time tracking of the selected task

You can also just start typing digits to jump to a list entry by number.


## Configuration

You can configure the behaviour of pter by creating or editing a
configuration file either in the default location
(`~/.config/pter/pter.conf` or whatever `pter --help` is
telling you) or whatever configuration file you would like to use by
providing the `--config` parameter to `pter`.

The configuration file consists of three groups:

 - General, for general behaviour
 - Symbols, for icons used in the GUI
 - Colors, if you want to change the colorscheme
 - Keys, to change the keyboard controls
 - Editor:Keys, to change the keyboard controls for input fields

### General

 - `use-colors`, whether or not to use colors
 - `show-numbers`, whether or not to show numbers in the task and search list
 - `scroll-margin`, how many lines to show at the lower and upper margin of lists
 - `safe-save`, whether or not to use the safe save feature (defaults to yes)
 - `search-case-sensitive`, whether or not to search case-sensitive (defaults to yes)

### Symbols

 - `selection`, what symbol or string to use to indicate the selected item of a list
 - `not-done`, what symbol or string to use for tasks that are not done
 - `done`, what symbol or string to use for tasks that are done
 - `overflow-left`, what symbol or string to use to indicate that there is more text to the left
 - `overflow-right`, what symbol or string to use to indicate that there is more text to the right
 - `overdue`, the symbol or string for tasks with a due date in the past
 - `due-today`, the symbol or string for tasks with a due date today
 - `due-tomorrow`, the symbol or string for tasks with a due date tomorrow
 - `tracking`, the symbol or string to show that this task is currently being tracked

### Colors

Colors are defined in pairs: foreground and background color. Some items come
with a `sel-` prefix so you can define the color when it is a selected list
item.

You may decide to only define one value, which will then be used as the text
color. The background color will then be taken from `normal` or `selected`
respectively.

If you do not define the `sel-` version of a color, pter will use the
normal version and put the `selected` background to it.

If you specify a special background for the normal version, but none for the
selected version, the special background of the normal version will be used
for the selected version, too!

 - `normal`, any normal text and borders
 - `selected`, selected items in a list
 - `error`, error messages
 - `sel-overflow`, `overflow`, color for the scrolling indicators when editing tasks (and when selected)
 - `sel-overdue`, `overdue`, color for a task when it’s due date is in the past (and when selected)
 - `sel-due-today`, `due-today`, color for a task that’s due today (and when selected)
 - `sel-due-tomorrow`, `due-tomorrow`, color for a task that’s due tomorrow (and when selected)
 - `inactive`, color for indication of inactive texts
 - `help`, help text at the bottom of the screen
 - `help-key`, color highlighting for the keys in the help
 - `pri-a`, `sel-pri-a`, color for priority A (and when selected)
 - `pri-b`, `sel-pri-b`, color for priority B (and when selected)
 - `pri-c`, `sel-pri-c`, color for priority C (and when selected)
 - `context`, `sel-context`, color for contexts (and when selected)
 - `project`, `sel-project`, color for projects (and when selected)
 - `tracking`, `sel-tracking`, color for tasks that are being tracked right now (and when selected)

### Keyboard controls

In the configuration you can define keys to launch a function in the program.
The following functions exist in lists:

 - `quit`: quit the program
 - `next-item`: select the next item in a list
 - `prev-item`: select the previous item in a list
 - `half-page-up`: scroll up by half a page
 - `half-page-down`: scroll down by half a page
 - `first-item`: jump to the first item in a list
 - `last-item`: jump to the last item in a list
 - `search`: enter a new search query
 - `load-search`: show the saved searches to load one
 - `save-search`: save the current search
 - `jump-to`: enter a number to jump to that item in the list
 - `toggle-done`: toggle the "done" state of a task
 - `toggle-hidden`: toggle the "hidden" state of a task
 - `refresh-screen`: rebuild the GUI
 - `reload-tasks`: enforce reloading of all tasks from all sources
 - `toggle-tracking`: start or stop time tracking for the selected task
 - `open-url`: open a URL of the selected task
 - `nop`: nothing (in case you want to unbind keys)

And these functions exist in input fields:

 - `go-left`, move the cursor one character to the left
 - `go-right`, move the cursor one charackter to the right
 - `go-bol`, move the cursor to the beginning of the line
 - `go-eol`, move the cursor to the end of the line
 - `submit-input`, accept the changes, leave the editor (applies the changes)
 - `cancel`, cancel editing, leave the editor (reverts any changes)
 - `del-right`, delete the character right of the cursor
 - `del-left`, delete the character left of the cursor
 - `del-to-bol`, delete all characters from the cursor to the beginning of the line

Keys are just given by the character, eg. `d`, with a `^` to indicate that
`Ctrl` has to be pressed at the same time (eg. `^C` for `Ctrl+C`).

There are also some special keys understood and surrounded by `<` and `>`:

 - `<backspace>`
 - `<del>`
 - `<left>` left cursor key
 - `<right>` right cursor key
 - `<up>` cursor key up
 - `<down>` cursor key down
 - `<pgup>` page up
 - `<pgdn>` page down
 - `<home>`
 - `<end>`
 - `<escape>`
 - `<return>`
 - `<tab>`
 - `<f1>` through `<f12>`

### Example

Here's an example configuration

    [General]
    scroll-margin = 8
    show-numbers = no

    [Symbols]
    selection = →
    done = ✔
    not-done = ☐

    [Colors]
    normal = 7, 0
    error = 1, 0
    selected = 2, 0

    [Keys]
    g = first-item
    G = last-item
    j = jump-to
    <f3> = search

    [Editor:Keys]
    ^A = go-bol
    ^E = go-eol

