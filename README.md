# OpenFrameworks Documentation shortcut

## Synopsis

This python 2.7 script can help you to jump directly from your text editor to the OF documentation.

<br />
<br />
<br />

## Usage example ( Qt Creator / Windows 7 )

- Select an OF keyword (a global function name, a class name, or a method of a class)

![Qt Creator Example Image 1](doc/Qt-Creator-Usage-1.png)

- Call the script, with the menu or a keyboard shortcut ( Ctrl-Alt-O in this case )

![Qt Creator Example Image 2](doc/Qt-Creator-Usage-2.png)

This lead you to the right documentation entry in your web browser:

![Documentation view Image](doc/result.png)

- If the keyword is a method of a class, and if many classes have a method with this name, a
window popup to choose the class:

![Qt Creator Example Image 3](doc/Qt-Creator-Usage-3.png)

![Selection Popup Image](doc/selection-popup.png)

Choose the class, and press Enter (or Escape to cancel). This will display the documentation for
the method of this class.

<br />
<br />
<br />

## Requirement
You need to have Python 2.7 installed.

<br />
<br />
<br />

## Installation
Copy these files somewhere, for example *C:\Users\username\Documents\of\Doc shortcut\0.9.3*
- of.ico
- of.xbm
- generate-index.py
- open-documentation.py
- and the index folder

![Files installation Image](doc/files-installation.png)

You should be able to use the tool with a command line to find an OF keyword in the online documentation:

![Command line Usage Image](doc/command-line.png)

This should open your web browser pointed to the right place, the ofSetColor documentation.

![Documentation view Image](doc/result.png)

- If this doesn't work, read the documentation at the beginning of *open-documentation.py*
- If the command output is *"Item not found in the documentation"*, perhaps you need to generate the index for your current OF version. In this case read the beginning of *generate-index.py*, and use it to generate the index.

You can manually change the base URL for the documentation, for example to use a local copy of the documentation rather
than the online documentation. Just edit *open-documentation.py* to set the OF documentation URL:

![Paths setup Image](doc/path-setup.png)  
  
<br />
<br />
<br />

## Editor configuration

You can now configure your code editor to use the script and be able to show you the documentation for a selected keyword.

Here's an example for Qt Creator 3.6.1, but this should work with any editor which allow to run shell commands.

First, add the script in the Tools menu:

![Qt Creator Setup 1 Image](doc/Qt-Creator-Setup-1.png)

![Qt Creator Setup 2 Image](doc/Qt-Creator-Setup-2.png)

![Qt Creator Setup 3 Image](doc/Qt-Creator-Setup-3.png)

You can if you want assign a keyboard shortcut to this new tool:

![Qt Creator Setup 4 Image](doc/Qt-Creator-Setup-4.png)

![Qt Creator Setup 5 Image](doc/Qt-Creator-Setup-5.png)

You can now select an OF keyword (a global function or a class name), and see its documentation with this tool.

![Qt Creator Example Image 1](doc/Qt-Creator-Usage-1.png)

Invoque the tool either by the menu or its keyboard shortcut:

![Qt Creator Example Image 2](doc/Qt-Creator-Usage-2.png)

This lead you to the right documentation entry in your web browser:

![Documentation view Image](doc/result.png)
