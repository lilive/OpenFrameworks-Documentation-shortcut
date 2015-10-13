# OpenFrameworks Documentation shortcut

## Synopsis

This python 2.7 script can help you to jump directly from your text editor to the OF documentation.

## Usage example ( Code::Blocks )

- Place the insertion point on an OF keyword (a global function name, a class name, or a method of a class)
- Call the script, with the menu or a keyboard shortcut ( Alt-O in this case )

![Code::Blocks Usage Image](doc/codeblocks-usage.png)

This lead you to the right documentation entry in your web browser:

![Documentation view Image](doc/result.png)

- If the keyword is a method of a class, and if many classes have a method with this name, a
window popup to choose the class:

![Code::Blocks Usage 2 Image](doc/codeblocks-usage-2.png)

![Selection Popup Image](doc/selection-popup.png)

Choose the class, and press Enter (or Escape to cancel). This will display the documentation for
the method of this class.

## Requirement
You need to have Python 2.7 installed.

## Installation
Put the script somewhere, for example *C:\Users\username\Documents\python\OF doc*

![Files installation Image](doc/files-installation.png)

You should be able to use the tool with a command line to find an OF keyword in the online documentation:

![Command line Usage Image](doc/command-line.png)

This should open your web browser pointed to the right place, the ofSetColor documentation.
- If this doesn't work, read the documentation at the beginning of *open-documentation.py*
- If the command output is *"Item not found in the documentation"*, perhaps you need to generate the index for your current OF version. In this case read the beginning of *generate-index.py*, and use it to generate the index.

You can manually change the base URL for the documentation, for example to use a local copy of the documentation rather
than the online documentation. Just edit *open-documentation.py* to set the OF documentation URL:

![Paths setup Image](doc/path-setup.png)

## Editor configuration ( Code::Blocks )
You can now configure your code editor to use the script and be able to show you the documentation for a selected keyword.

Here's an example for Code::Blocks 12.11, but this should work with any editor which allow to run shell commands.

First, add the script in the Tools menu:

![Code::Blocks setup 1 Image](doc/codeblocks-install-step-1.png)

![Code::Blocks setup 2 Image](doc/codeblocks-install-step-2.png)

![Code::Blocks setup 3 Image](doc/codeblocks-install-step-3.png)

![Code::Blocks setup 4 Image](doc/codeblocks-install-step-4.png)

You can if you want assign a keyboard shortcut to this new tool:

![Code::Blocks setup 5 Image](doc/codeblocks-install-step-5.png)

![Code::Blocks setup 6 Image](doc/codeblocks-install-step-6.png)

You can now place the insertion point on an OF keyword (a global function or a class name), and see its documentation with this tool.

Invoque the tool either by the menu or its keyboard shortcut:

![Code::Blocks Usage Image](doc/codeblocks-usage.png)

This lead you to the right documentation entry in your web browser:

![Documentation view Image](doc/result.png)
