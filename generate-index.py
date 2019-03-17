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

- Edit the script
- Set the 2 path variables at the beginning
- Set the logLevel
- Save it and run it.

The script create an index which associate the OF keywords to the html files in the documentation.
You only need to run this script once. Then open-documentation.py can read the index.

The copy of the openFrameworks site contains a directory where are the sources of the OF documentation.
To parse them, the script first convert them to html using Pandoc. This create hmtl files in
indexPath\html. You can delete this folder after usage, or leave it to speed up the next update (only
the .markdown files more recents than the .html files will be reconverted by Pandoc).

"""

import sys, os

# Path to the documentation directory in the local OF site copy :
# Example:
# docSourcesRootPath = 'C:\Users\username\Documents\of\ofSite\_documentation'
docSourcesRootPath = os.path.expanduser('~/Documents/of/ofSite/documentation')

# Path to the Pandoc executable. If Pandoc is in your path you can do pandocExe = 'pandoc'
# Example:
# pandocExe = 'C:\Users\username\AppData\Local\Pandoc\pandoc.exe'
# pandocExe = os.path.expanduser('~/AppData/Local/Pandoc/pandoc.exe')
pandocExe = 'C:\Program Files\pandoc\pandoc.exe'

NOTICE = 0
WARNING = 1
ERROR = 2
# What messages do we print ?
logLevel = WARNING

# If these 2 paths and the logLevel are set, no need to read further, you can run the script


import subprocess, shlex
import os.path
import html5lib
from bs4 import BeautifulSoup
import re
import colorama
colorama.init()

logLevelTitle = {
    NOTICE: '',
    WARNING: colorama.Fore.YELLOW + "[WARNING]",
    ERROR: colorama.Fore.RED + "[ERROR]"
}

def log( message, level = NOTICE ):
    
    """Print the message with a proper color and title, according to level"""
    
    if level >= logLevel :
        print logLevelTitle[ level ],
        print message,
        print colorama.Style.RESET_ALL

# Check for pandoc file exist
if not os.path.isfile( pandocExe ):
    log( "The path to pandoc is incorrect, there is no such file :" + pandocExe, ERROR )
    sys.exit(1)

# Path to the script directory
scriptDirPath = os.path.dirname(os.path.realpath(__file__))

# Path to the directory which will receive the index files.
indexPath = os.path.join( scriptDirPath, 'index' );


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
        log( 'Convert "' + fileRelPath + '" to HTML' )
        command = '"' + pandocExe + '" --quiet -f markdown-space_in_atx_header -t html -s --toc -o "' + htmlPath + '" "' + filePath + '"'
        args = shlex.split( command )
        process = subprocess.Popen( args, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        stdoutdata, stderrdata = process.communicate()
        if stderrdata:
            log( "pandoc failed to parse this markdown file :" + filePath, ERROR )
            log( "pandoc return this error :", ERROR )
            log( stderrdata, ERROR )
        
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

def parseFunctionLink( a, fileRelPath ):
    
    """Extract the function name, the function signature, and the anchor from a link HTML tag <a>.
    Return ( success, name, signature, anchor ) where success is True or False."""

    # Find the text of the link. a.string is not enought because sometimes the link text is
    # html formated.
    content = "".join( a.stripped_strings )
    if not content :
        log( 'Unable to read function name in file ' + fileRelPath, ERROR )
        log( 'Tag:', ERROR )
        log( a, ERROR )
        return ( False, '', '' ) 
        
    else:
        m = re.search( '^.*?\s(\w+)\(.*\)$', content )
        if m is None:
            return ( False, '', '' )
        else:
            functionName = m.group(1)
            return ( True, functionName, content )
                

###################################################################################################

def createFunctionsIndex( htmlPath, fileRelPath ) :
    
    """Add index entries for a set of of functions""" 

    log( 'Parsing ' + fileRelPath )
    soup = BeautifulSoup( open( htmlPath ), "html5lib" )
        
    # Find table of content
    toc = soup.find(id='TOC')
    
    # Find all the functions
    functionsList = toc.ul.li.ul.li.ul
    if functionsList is None:
        log( 'No function list found in ' + fileRelPath, WARNING )
        return
        
    functions = functionsList.find_all('li')
    
    for function in functions:
    
        # Find function name
        ( success, functionName, functionSignature ) = parseFunctionLink( function.a, fileRelPath )
        if not success:
            continue
        if functionName in ofFunctionsList:
            continue
        log( "Function found: " + functionName )
            
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
    tocLi = toc.ul.li
    if toc is None or tocLi is None:
        log( 'No TOC found in ' + fileRelPath, ERROR )
        return
    
    # Find class name
    title = tocLi.a.string
    m = re.search( '^class\s+(\w+)_?', title )
    if m is None:
        return
        
    className = m.group(1)
    log( "Class found: " + className )
    
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
    
    # Find methods list for this class
    
    if tocLi.ul is None:
        return
        
    methods = None
    for li in tocLi.ul.find_all('li'):
        if li.a is None:
            continue
        if li.a.string == 'Methods':
            if li.ul is None:
                continue
            methods = li.ul.find_all('li')
            
    if methods is None:
        return
    
    # Memorize the names and the links to these methods
    
    for method in methods:
        ( success, functionName, functionSignature ) = parseFunctionLink( method.a, fileRelPath )
        if not success:
            continue
        log( 'Method found: ' + className + '::' + functionName + '()' )
        entry = ( className, fileRelPathWithoutExt )
        if functionName in classesMethods:
            if not entry in classesMethods[ functionName ]:
                classesMethods[ functionName ].append( entry );
        else:
            classesMethods[ functionName ] = [ entry ];
    


###################################################################################################

# Create the directory for the index
if( not os.path.exists( indexPath )):
    os.makedirs( indexPath )
indexFile = open( os.path.join( indexPath, 'classesAndGlobalFunctions.txt' ), 'w' )

# Create the directory for the files created by Pandoc
htmlRootDirPath = os.path.join( indexPath, 'html' )
if( not os.path.exists( htmlRootDirPath )):
    os.makedirs( htmlRootDirPath )

# List of all the OF global functions. Used to memorize the OF global functions and avoid multiple
# identicals entries in the index (because these functions may be overloaded).
# createFunctionsIndex() will populate this list.
ofFunctionsList = []

# All the classes methods.
# Keys of the dictionnary are the functions names.
# The value are list. Each list contains pairs in the form ( className, fileRelPathWithoutExt ).
# createClassIndex() will populate this dictionnary.
classesMethods = dict()

# Traverse the documentation to find OF keywords,
# and write the index for all the classes and the globalMethods

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

# Create the index for each classes method found, because a same method name can be use in several different classes

for functionName, entries in classesMethods.iteritems():
    indexFile = open( os.path.join( indexPath, functionName + '.txt' ), 'w' )
    for ( className, fileRelPathWithoutExt ) in entries:
        # print functionName, className, fileRelPathWithoutExt
        indexFile.write( className + ' ' + fileRelPathWithoutExt + '.html#show_' + functionName + '\n' )
    indexFile.close()
