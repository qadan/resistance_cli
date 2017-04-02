# Base installation

system_scripts/resistance_cli.conf goes into /etc/systemd
create the folder /etc/systemd/system/getty@tty1.service.d
system_scripts/override.conf goes into /etc/systemd/system/getty@tty1.service.d

TODO: Printer driver?

# Modification

* Any .txt file placed into help_files will display a response when the user tries "help X" (minus the .txt)
* Any .txt file placed into query_responses will display a response when the user tries "query X" (minus the .txt)
* Any .pdf file placed into read_files or on the USB drive will display a response when the user tries "read X". Note that these are not real PDFs but simply PDF-like files that just contain text (i.e., you could make one in Notepad by just saving the extension as .pdf).
* Some of the text that is used for response in general cases can be modified in general_responses.json. Some of these bits of text have a '%s' in them; this will be replaced with some text in the following cases:
  * command_not_found: '%s' replaced with the command the user tried to use.
  * command_called_incorrectly: '%s' replaced with the command the user tried to use.
  * help_not_found: '%s' replaced with whatever the user tried to get help about.
  * file_not_found: '%s' replaced with the file the user tried to open.
* The welcome message that displays on login can be modified in welcome_message.txt
* The password used to login can be modified in password.txt

# Notes

* You can exit the program completely by typing in the code in secret_exit.txt at any prompt. Modifying secret_exit.txt will change that code.
* The program modifies the system in such a way that Ctrl-C and Ctrl-D no longer exit the program as one would generally expect on a unix-like system. This is to keep more tech-savvy users from just exploding the whole thing.
* As a general rule, lines of text in .txt are kept to 120 characters maximum; this was done for consistency and so there wouldn't be unexpected wrap-around issues with the monitor.
