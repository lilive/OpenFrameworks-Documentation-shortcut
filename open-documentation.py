# coding=utf-8

"""This script load the documentation page of the OF keyword passed as command line argument in your web browser.

Index
=====

This script use the index generated by generate-index.py to find the right html page.
If you haven't downloaded an index with this script, you have to run generate-index.py only once (see
generate-index.py documentation)

Usage
=====

Once you've got an index, just set the two paths below: indexPath and documentationURL.
The script use these paths to find the index and the OpenFrameworks documentation root page.
The script load the documentation page of an OpenFrameworks keyword within your browser, just invoque this
script with the keyword as argument.
If the script can't find the keyword in the index, it will load the home page of the documentation.

Requirement
===========

Python 2.7

"""

import sys
import os.path
import re
import webbrowser
import Tkinter
import tkFont
import platform

# Path to the index directory (downloaded with this script, or generated by generate-index.py)
# Example:
# indexPath = 'C:\Users\username\Documents\python\OF doc\index'
indexPath = os.path.expanduser('~\Documents\python\OF doc\index')

# Base URL of the OpenFrameworks documentation
documentationURL = 'http://www.openframeworks.cc/documentation/'

# For users, no need to read further, you just have to set these paths


# Get the searched keyword
if len( sys.argv ) < 2 :
    print 'Error: This script must be call with an item name to search in the documentation as parameter.'
    sys.exit(1)
keyword = sys.argv[1]

# Open the index file
classesAndGlobalFunctionsIndexPath = os.path.join( indexPath, 'classesAndGlobalFunctions.txt' )
if not os.path.isfile( classesAndGlobalFunctionsIndexPath ):
    print 'Error: No index found.'
    sys.exit(1)
classesIndex = open( classesAndGlobalFunctionsIndexPath, 'r' )

# Search the keyword in the index for classes and global functions

regex1 = re.compile( '(\w+)\s+(.+)' )
regex2 = re.compile( '(\S+)\s+(.+)' )
for entry in classesIndex:
    
    # Split the index text line to isolate the keyword 
    m1 = regex1.match( entry )
    if m1 is None:
        print 'Error: Malformed index file!!!'
        continue
    
    # Check if the index line is composed with 2 strings (class entry) or 3 strings (function entry)
    m2 = regex2.match( m1.group(2) )
    
    if m2 is None:
        # If the index entry is about a class, this entry match the keyword in two cases:
        # 1- idemName is strictly identical to the class name of this entry
        # 2- idemName, followed by an underscore, is identical to the class name of this entry
        if keyword == m1.group(1) or keyword + '_' == m1.group(1) :
            # Open the right URL in the web browser
            relPath = m1.group(2)
            url = documentationURL + relPath + '.html'
            print 'Opening ' + url
            webbrowser.open( url )
            sys.exit(0)
    else:
        # If the index entry is about a function, this entry match the keyword only
        # if it is strictly identical to the function name.
        if keyword == m1.group(1) :
            # Open the right URL in the web browser
            relPath = m2.group(1)
            anchor = m2.group(2)
            url = documentationURL + relPath + '.html#' + anchor
            print 'Opening ' + url
            webbrowser.open( url )
            sys.exit(0)
            
            
# If the keyword is not a class or a global function name, it may be a method name for a class.
# Does an index file exists for this keyword ?
indexPath = os.path.join( indexPath, keyword + '.txt' )
if os.path.isfile( indexPath ):
    
    index = open( indexPath, 'r' )
    
    # Create a list of tuples ( className, relURL ) from the index
    entries = []
    regex = re.compile( '(\w+)\s+(.+)' )
    for entry in index:
        # Split the index text line to get the class name and the URL 
        m = regex.match( entry )
        if m is None:
            print 'Error: Malformed index file!!! File is ' + indexPath 
            continue
        className = m.group(1)
        relURL = m.group(2)
        entries.append( ( className, relURL ) )
    entries.sort()
    
    # If there is only one entry, open it in the web browser 
    if len( entries ) == 1:
        url = documentationURL + entries[0][1]
        print 'Opening ' + url
        webbrowser.open( url )
        sys.exit(0)
    
    # If there is many classes with a method called like keyword, built a selection window
    
    window = Tkinter.Tk()
    window.title(' Select Class for method ' + keyword )
    # Change the window icon, if possible
    dirPath = os.path.dirname(os.path.realpath(__file__))
    icoPath = os.path.join( dirPath, 'of' )
    if platform.system() == 'Windows':
        window.iconbitmap( icoPath + '.ico' )
    elif platform.system() == 'Linux':
        window.iconbitmap( icoPath + '.xbm' )
    
    # The scrollbar to scroll the list
    scrollBar = Tkinter.Scrollbar( window )
    scrollBar.pack( side=Tkinter.RIGHT, fill=Tkinter.Y )
    
    # The list of the classes
    height = max( 5, len(entries) )
    height = min( 30, height )
    font = tkFont.Font(family='Helvetica', size=10)
    listBox = Tkinter.Listbox(window, font=font, width=40, height=height, exportselection=0 )
    listBox.pack( side=Tkinter.RIGHT, fill=Tkinter.Y )
    for entry in entries:
        listBox.insert( Tkinter.END, entry[0] )
    listBox.activate( 0 )
    listBox.selection_set( 0 )
    listBox.focus_set()
    
    # Attach the scrollbar to the list
    scrollBar.config( command=listBox.yview )
    listBox.config( yscrollcommand = scrollBar.set )
    
    # Center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    # Open the class method documentation in the browser when <Return> is pressed
    def returnPressed(event):
        selection = listBox.curselection()
        if selection:
            idx = selection[0]
            relURL = entries[ idx ][1]
            url = documentationURL + relURL
            print 'Opening ' + url
            webbrowser.open( url )
        window.destroy()
    window.bind("<Return>", returnPressed )
    
    # Close the selection window and do nothing when <Escape> is pressed
    def escapePressed(event):
        window.destroy()
    window.bind("<Escape>", escapePressed )
    
    # Ask the user to select the class
    window.mainloop()
    sys.exit(0)
    

print 'Item not found in the documentation'
webbrowser.open( documentationURL )