# Searching

Both web interface and terminal GUI have a powerful search built-in. They also
provide the option to save your search query, so you can easily switch between
search results: [named searches](named-searches.md).

Unless configured otherwise, the search is case sensitive.

Here’s a detailed explanation of how to use the search.

## Search for phrases

The easiest way to search is by phrase in tasks.

For example, you could search for `read` to find any task containing the word
`read` or `bread` or `reading`.

To filter out tasks that do *not* contain a certain phrase, you can search with
`not:word` or, abbreviated, `-word`.


## Search for tasks that are completed

By default all tasks are shown, but you can show only tasks that are not
completed by searching for `done:no`.

To only show tasks that you already marked as completed, you can search for
`done:yes` instead.


## Hidden tasks

Even though not specified by the todotxt standard, some tools provide the
“hide” flag for tasks: `h:1`. pytodoweb understands this, too, and by default
hides these tasks.

To show hidden tasks, search for `hidden:yes`. Instead of searching for
`hidden:` you can also search for `h:` (it’s a synonym).


## Projects and Contexts

To search for a specific project or context, just search using the
corresponding prefix, ie. `+` or `@`.

For example, to search for all tasks for project “FindWaldo”, you could search
for `+FindWaldo`.

If you want to find all tasks that you filed to the context “email”, search
for `@email`.

Similar to the search for phrases, you can filter out contexts or projects by
search for `not:@context`, `not:+project`, or use the abbreviation `-@context`
or `-+project` respectively.


## Priority

Searching for priority is supported in two different ways: you can either
search for all tasks of a certain priority, eg. `pri:a` to find all tasks of
priority `(A)`.
Or you can search for tasks that are more important or less important than a
certain priority level.

Say you want to see all tasks that are more important than priority `(C)`, you
could search for `moreimportant:c`. The keyword for “less important” is
`lessimportant`.

`moreimportant` and `lessimportant` can be abbreviated with `mi` and `li`
respectively.


## Due date

Searching for due dates can be done in two ways: either by exact due date or
by defining “before” or “after”.

If you just want to know what tasks are due on 2018-08-03, you can search for
`due:2018-08-03`.

But if you want to see all tasks that have a due date set *after* 2018-08-03,
you search for `dueafter:2018-08-03`.

Similarly you can search with `duebefore` for tasks with a due date before a
certain date.

`dueafter` and `duebefore` can be abbreviated with `da` and `db` respectively.

If you only want to see tasks that have a due date, you can search for
`due:yes`. `due:no` also works if you don’t want to see any due dates.

Instead of absolute dates, you can also provide relative dates (see section
Relative Dates in [pytodoterm](doc/pytodoterm.md) documentation), like
`duebefore:1w` (all tasks that are due within the next week).


## Creation date

The search for task with a certain creation date is similar to the search
query for due date: `created:2017-11-01`.

You can also search for tasks created before a date with `createdbefore` (can
be abbreviated with `crb`) and for tasks created after a date with
`createdafter` (or short `cra`).

To search for tasks created in the year 2008 you could search for
`createdafter:2007-12-31 createdbefore:2009-01-01` or short `cra:2007-12-31
crb:2009-01-01`.

Instead of absolute dates, you can also provide relative dates (see section
Relative Dates in [pytodoterm](doc/pytodoterm.md) documentation), like
`createdafter:-3d` (all tasks that were created within the last two days).


## Completion date

The search for tasks with a certain completion date is pretty much identical
to the search for tasks with a certain creation date (see above), but using
the search phrases `completed`, `completedbefore` (the short version is `cob`), or
`completedafter` (short form is `coa`).

Instead of absolute dates, you can also provide relative dates (see section
Relative Dates in [pytodoterm](doc/pytodoterm.md) documentation), like
`completedafter:-8d` (all tasks that were completed within the last 7 days).


## Threshold or Tickler search

If you follow the non-standard suggestion to introduce the `t:` tag in your
tasks to indicate that a task should not be active prior to a certain date,
you are in luck! pytodoweb understands this convention and by default hides
tasks that have a threshold set in the future.

If you still want to see all tasks, even those with a threshold in the future,
you can search for `threshold:no`.

You can also pretend it’s a certain date in the future (eg. 2042-02-14) and
see what tasks become available then by searching for `threshold:2042-02-14`.

`threshold` can be abbreviated with `t`. `tickler` is a synonym for
`threshold`.


