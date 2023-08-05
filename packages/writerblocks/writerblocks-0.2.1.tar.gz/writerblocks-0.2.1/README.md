# writerblocks

A toolkit for writing stories in a modular way.

## Overview

writerblocks provides a way of constructing structured stories from a
collection of Markdown-formatted text files.  It's intended to be highly
flexible and customizable, and to make it easy to reorder, restructure, and
change around the story on the fly.

writerblocks works using a project directory, containing the following:

1. Some number of text files, default Markdown-formatted, representing "scenes"
   or snippets of story, which may be stored in subdirectories.
   Each text file may contain a "tags block" consisting of the word "tags:"
   followed by one or more lines containing comma-separated tags, keywords,
   or labels that categorize the contents of that file.
2. An `index` file, which is a YAML or JSON file that contains the relative
   locations of the scene files and information about the organization of
   those scenes.  It may simply be a list that tells what order the files
   should be read in, or it may group them under volumes, chapters, sections,
   or some other hierarchical structure.
3. A configuration file, `writerblocks.ini`, that contains default options
   that would otherwise be provided on the command line.
4. A `format` file, which is a YAML or JSON file that contains instructions for
   how to format the story.  This file can specify what to use to separate
   scenes, chapters, or whatever other grouping mechanisms are used in the
   index.

(The configuration and format files, as well as an empty index file, can be
automatically generated; see usage examples for how to do that.)

It's additionally possible to create a `preamble` file whose contents will be
automatically attached to the beginning of the final output file.

Once the user has created the project directory, they can call writerblocks to combine
the scenes into new files, which can then be optionally converted into a
publication format (PDF, epub, HTML, etc.) according to the ordering and
structure defined in the index file.

Additionally, the user can combine only scenes that have specific tags; for
example, if they choose to tag all scenes with the characters that appear in
that scene, they could generate a file containing the scenes that featured
specific characters, to look at what those characters' arc looks like on its
own.  It's also possible to *exclude* scenes based on their tags, so if you
want to look at the scenes involving characters A and B but not C, that can be
easily done as well.

Since the order of scenes depends only on the index file, if the user decides
that a particular scene or group of scenes needs to happen at a different point
in the story, they need only to move the filenames in the index.  Removing a
scene is easy too, and doesn't require deleting the actual file; just get rid of
any references to it in the index and consider it gone!

## Requirements

writerblocks depends on Python 3.5 or newer.  It also requires pandoc (tested with version 
1.19.2.4) for the format conversion process.

## Some usage examples

  * Create a new project with default options in directory `some/dir`:

    `writerblocks-cli --base-dir /some/dir --new-project`
  * Generate a PDF based on the contents of `my_index.json` in the current working directory:

    `writerblocks-cli --out-fmt pdf --out-file out.pdf --index-file my_index.json`
  * Generate foo.md, a compilation of all files with the tag `foo` in said index:

    `writerblocks-cli -f markdown -o foo.md -i my_index.json -t foo`
