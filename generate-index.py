# coding=utf-8

"""This script generate the index required by open-documentation.py to work.

Requirements
============

Python 2.7
Pandoc
    Used to convert the markdown documentation files to more parsable html files
    http://pandoc.org/
BeautifulSoup
    Module for python
    Used to parse html files produced by Pandoc
    Installation: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
html5lib
    html parser module for python
    Used by BeautifulSoup
    Installation: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
colorama
    Module for python
    Used to colorize output messages
    Installation: pip install colorama
A copy of the openFrameworks site
    Or at least its documentation directory
    Installation:
        git -clone https://github.com/openframeworks/ofSite.git
        Or go to https://github.com/openframeworks/ofSite and download ZIP
        
Usage
=====

Edit the script, set the path variables at the beginning, save it, and run it.

The script create an index which associate the OF keywords to the html files in the documentation.
You only need to run this script once. Then open-documentation.py can read the index.

The copy of the openFrameworks site contains a directory where are the sources of the OF documentation.
To parse them, the script first convert them to html using Pandoc. This create hmtl files in
indexPath\html. You can delete this folder after usage, or leave it to speed up the next update (only
the .markdown files more recents than the .html files will be reconverted by Pandoc).

TODO
====

Classes are recognized, and global functions.
But classes methods are not.
Idea: Index classes methods and when a class method if search with open-documentation.py, open
a window which display all the matches for this method name (because many classes have
common methods names).

"""

import sys
import os
import subprocess
import os.path
import html5lib
from bs4 import BeautifulSoup
import re
import colorama
colorama.init()

# Path to the documentation directory in the local OF site copy :
docSourcesRootPath = 'C:\Users\username\Documents\of\ofSite\_documentation'

# Path to the directory which will receive the index files.
# You can define it or leave it to create an 'index' directory within the current working directory.
# Custom directory example for Windows: indexPath = 'C:\Users\username\Documents\of\documentation\shortcut-script\index'
indexPath = os.path.join( os.getcwd(), 'index' );

# Path to the Pandoc executable. If Pandoc is in your path you can do pandocExe = 'pandoc'
pandocExe = '"C:\Users\username\AppData\Local\Pandoc\pandoc.exe"'

# If this 3 paths are set, no need to read further, you can run the script


###################################################################################################

def convertMarkDownToHTML( filePath, fileRelPath, dirRelPath ):
    
    """Convert a MarkDown file to an HTML file, for further processing with BeautifulSoup. This use the pandoc program."""
    
    htmlPath = os.path.join( htmlRootDirPath, dirRelPath ) + '.html'
        
    convert = True
    if( os.path.exists( htmlPath ) ):
        fileTime = os.path.getmtime( filePath )
        htmlTime = os.path.getmtime( htmlPath )
        if( fileTime <= htmlTime ):
            convert = False
    
    if( convert ):
        ( htmlDir, _ ) = os.path.split( htmlPath )
        if( not os.path.exists( htmlDir ) ):
            os.makedirs( htmlDir )
        print 'Convert "' + fileRelPath + '" to HTML'
        command = pandocExe + ' "' + filePath + '" -s --toc -o "' + htmlPath
        sys.stdout.flush()
        subprocess.call( command, shell=True )
        
    return htmlPath

###################################################################################################

def splitDirPath( path ):
    
    """Cut the path to a directory into its components"""
    
    folders = []
    
    while 1:
        ( path, folder ) = os.path.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
    
            break
    
    folders.reverse()
    return folders


###################################################################################################

def createFunctionsIndex( htmlPath, fileRelPath ) :
    
    """Add index entries for a set of of functions""" 

    # print 'Parsing ' + fileRelPath
    soup = BeautifulSoup( open( htmlPath ), "html5lib" )
        
    # Find table of content
    toc = soup.find(id='TOC')
    
    # Find all the functions
    functionsList = toc.ul.li.ul.li.ul
    if functionsList is None:
        print colorama.Fore.RED + 'No function list found in ' + fileRelPath + colorama.Style.RESET_ALL
        return
        
    functions = functionsList.find_all('li')
    
    for function in functions:
    
        # Find function name
        functionName = ''
        line = function.a.string
        if line is None :
            # print 'File:' + fileRelPath
            # print str(function.a)
            m = re.search( '.*?>[^\(]+\s(\w+)\(', str(function.a) )
            if m is None:
                print colorama.Fore.RED
                print 'Unable to read function name in file ' + fileRelPath
                print 'Tag:'
                print function
                print colorama.Style.RESET_ALL
                continue
            else:
                functionName = m.group(1)
                if functionName in ofFunctionsList:
                    continue
                print colorama.Fore.BLUE + 'Verify this function name from ' + fileRelPath
                print functionName + '()' + colorama.Style.RESET_ALL
        else:
            m = re.search( '^.*\s(\w+)\(.*\)$', line )
            if m is None:
                continue
            else:
                functionName = m.group(1)
                if functionName in ofFunctionsList:
                    continue
                print "Function found: " + functionName
            
        ofFunctionsList.append( functionName )
        
        # Create path to this function.
        # This path will allow to open the right html page for this class in the documentation.
        ( fileRelPathWithoutExt, _ ) = os.path.splitext( fileRelPath )
        # We must remove the addons/ part at the beginning ot the path, if any
        parts = splitDirPath( fileRelPathWithoutExt )
        if parts[0] == 'addons' :
            fileRelPathWithoutExt = '/'.join( parts[ 1: ] )
        else:
            fileRelPathWithoutExt = '/'.join( parts )
        
        # Remove trailing _functions
        fileRelPathWithoutExt = fileRelPathWithoutExt[ 0 : -10 ]
        
        # Ready to write this entry to the index
        indexFile.write( functionName + ' ' + fileRelPathWithoutExt + ' show_' + functionName + '\n' )
        

###################################################################################################

def createClassIndex( htmlPath, fileRelPath ) :
    
    """Add index entry for a class""" 

    soup = BeautifulSoup( open( htmlPath ), "html5lib" )
        
    # Find table of content
    toc = soup.find(id='TOC')
    
    # Find title
    li = toc.ul.li
    title = li.a.string
    
    # Find class name
    m = re.search( '^class\s+(\w+)_?', title )
    if not m is None:
        className = m.group(1)
        print "Class found: " + className
        
        # Create path to this class.
        # This path will allow to open the right html page for this class in the documentation.
        ( fileRelPathWithoutExt, _ ) = os.path.splitext( fileRelPath )
        # We must remove the addons/ part at the beginning ot the path, if any
        parts = splitDirPath( fileRelPathWithoutExt )
        if parts[0] == 'addons' :
            fileRelPathWithoutExt = '/'.join( parts[ 1: ] )
        else:
            fileRelPathWithoutExt = '/'.join( parts )
        
        # Trailing underscores must be ignored
        if fileRelPathWithoutExt.endswith( '_' ) :
            fileRelPathWithoutExt = fileRelPathWithoutExt[ 0 : -1 ]
        
        # Ready to write this entry to the index
        indexFile.write( className + ' ' + fileRelPathWithoutExt + '\n' )


###################################################################################################

# Create the directory for the index
if( not os.path.exists( indexPath )):
    os.makedirs( indexPath )
indexFile = open( os.path.join( indexPath, 'classesAndGlobalFunctions.txt' ), 'w' )

# Create the directory for the files created by Pandoc
htmlRootDirPath = os.path.join( indexPath, 'html' )
if( not os.path.exists( htmlRootDirPath )):
    os.makedirs( htmlRootDirPath )

ofFunctionsList = []

# Traverse the documentation to find OF keywords
for dirPath, dirNames, fileNames in os.walk( docSourcesRootPath ):
    for fileName in fileNames:
        
        # keep only markdown files
        ( name, ext ) = os.path.splitext( fileName )
        if( ext != '.markdown' ) : continue
        
        # Create paths relatives to the documentation directory 
        filePath = os.path.join( dirPath, fileName )
        fileRelPath = os.path.relpath( filePath, docSourcesRootPath )
        ( dirRelPath, _ ) = os.path.splitext( fileRelPath )
        
        # Convert markdown file to HTML file, with a TOC, to make it parsable with BeautifulSoup
        htmlPath = convertMarkDownToHTML( filePath, fileRelPath, dirRelPath )
        
        sys.stdout.flush()
        
        # Generate the index for a class or a set of functions, according to the file name
        if name.endswith( '_functions' ):
            createFunctionsIndex( htmlPath, fileRelPath )
        else:
            createClassIndex( htmlPath, fileRelPath )
            
indexFile.close()
