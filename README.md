# Work Organizer

The project was created from the frustration of managing a bunch of text files and pdf documents. The goal was to create a centralized place to manage the knowledge base. And since I'm a fan of command interfaces, everything works on commands.

These are two-part console applications: the first for creating and organizing notes and artifacts, the second for keeping track of time spent on work tasks.

What Organizer can do:


Input "-new" and write a new note.
Write your "tag" after it if needed.

Input "-cls" to clear the console.

Input "-sh" to search the notes by key word
Search notes by key-words in body of a note.

Input "-tag" to search the notes by tag word.

Input "-copy" to use clipboard.
Write your tag after flag if needed.

Input "-today" to read today notes.

Input "-all" to read all created notes.

Input "-order" to open today note by number.

Input "-date" to open notes by certain day.

Input "-display tags" to view available tags.

Input "-conn" to view list of connected files
Then you will be prompted to input index of file you need
Text files will be printed directly in console
Others will be opened by default application.

Input "-conn edit" to open text file for editing.

Similar to "-conn" except it can open Notepad.exe for text file to edit them.

Input "-import" to copy files to app directory
Then input full path to new file.

Input "-edit" to modify desired note(beta)
First you need to know exact date and position of the note
In this exact manner dd/mm/yyyy %note number%
You will be prompted to input date and index of your note
Then after "Input replace note: " press ctrl+v and paste note to modify
The note must have the same fields as before in order for the system to understand it.

Input "-del" to invoke delete sequence
The you will be prompted with input date of the note
and index numbers. You can delete more than one note in one go.

To quit from any of this prompts type "quit"
