# IMSCC Unpacker

Resources from LMS platforms (such as PowerSchool, Blackboard, and others) are exported as an .imscc file, a special type of zip file using the Common Cartridge specification to allow for cross-platform portability. Theoretically, this means that one should be be able export course materials from one LMS and import them into another without any issues.

For whatever reason, this does not always work, and users are forced choose between two bad options: (1) manually download and organize all the files one at a time and (2) parse the IMSCC file's XML manifest and manually reorganize and relabel everything.

With course materials of any appreciable volume, this takes hours, if not days. In many cases, this is an unfeasible amount of work and results in perfectly useful course materials being rendered useless.

The **IMSCC Unpacker** is Python script that parses the XML manifest included in an IMSCC file and reorganizes and renames the files within to reflect the way they were originally presented in the LMS. It does have limitations (see below), but the output format is usable by non-technical users.

## Usage

#### Requirements
* Python 3.10.12 (other versions may work but have not been tested)
* lxml 5.2.2

#### How To Use
1. Download the source files.
2. Install the project requirements (listed above).
3. Run the main.py file in the project's src folder.
4. You will be prompted to input the full path to a file directory in the command line.
   *NOTE: This will scan and convert **all** IMSCC files within the directory. This does **not** copy the files, so **you will lose the original file once processing begins**.*
6. It's that simple, and should take too long. The restructured file will be saved as a normal zip file in the same directory as the original one.

## Limitations (PLEASE READ BEFORE USING)

1. This tool was created specifically to solve an issue for PowerSchool's Schoology LMS. It has not been tested against IMSCC files created by other platforms, though theoretically the Common Cartridge specification should make it usable in other cases.
2. This tool has not been comprehensively tested against all Schoology modules/plugins. It has only the functionality I needed at time of creation. This includes (non-exhaustively) dealing with Exams, Assessments, Quizzes, the Turnitin LTI plugin, and handling any files uploaded by instructors--such as Excel sheets, Word docs, and PDFs.
3. This tool is functional on a Linux system (Ubuntu 22.04). In order for it to function on Windows, adjustments will need to be made to the filepath separators.
4. Text originally entered into the LMS itself posed an issue. It belongs in a web format (HTML/XML) but reconstructing that was non-essential. Anything that was entered into the LMS platform directly (rather than uploaded) is output by the Unpacker as a plain text (.txt) file. This includes Exams, Quizzes, Assignments, etc.. Because related images/graphs that were included in these elements are not compatible with plain text, the places where they belong has been noted in the files along with the name of the relevant image.
    While this is admittedly inconvenient, entering it into a new platform is as simple as copying and pasting into a new element of the same type (Assignment, Quiz, etc.).
5. Please forgive the messiness. When time is of the essence, function often triumphs over form.
