# pter

Your console UI to manage your todo.txt file(s).


## Installation

To install pytodotxt, you can follow these steps to clone the repository,
and install the program.

    pip install pter

Now you can run pter to access your todo.txt file(s):

    pter ~/todo.txt

See below for more details.


## Features

pter has a bunch of features that should help you managing your todo.txt file:

 - Fully compatible to the todo.txt standard
 - Support for `due:`, `h:`, `t:`
 - Search functionality
 - Configurable colors and shortcuts (and more, see [configuration](doc/pter.md))
 - Time tracking
 - Save search queries for quick access (see [named searches](doc/named-searches.md))


## Using pter

To launch pter you have to tell it where your todo.txt file is:

    pter ~/todo.txt

This will give you a listing of all your tasks order by how soon they will be
due and what priority you have given them.

You can navigate the tasks with your cursor keys and edit selected tasks by
pressing `e`.

More default shortcuts are:

 - `e`, edit the selected task
 - `n`, create a new task
 - `d`, mark the selected task as done (or toggle back to not done)
 - `q`, quit the program

There is a complex search available (have a look at the [help
document](docs/searching.md) for details), but the short version is:

 - press `/` to enter your search terms
 - search for `done:n` to only show incomplete tasks
 - search for a context with `@context`
 - search for a project with `+project`
 - search for tasks that do not belong to a context with `-@context` or `not:@context`
 - press `Return` to return the focus to the task list

