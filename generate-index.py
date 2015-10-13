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

Edit the script, set the 2 path variables at the beginning, save it, and run it.

The script create an index which associate the OF keywords to the html files in the documentation.
You only need to run this script once. Then open-documentation.py can read the index.

The copy of the openFrameworks site contains a directory where are the sources of the OF documentation.
To parse them, the script first convert them to html using Pandoc. This create hmtl files in
indexPath\html. You can delete this folder after usage, or leave it to speed up the next update (only
the .markdown files more recents than the .html files will be reconverted by Pandoc).

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
# Example:
# docSourcesRootPath = 'C:\Users\username\Documents\of\ofSite\_documentation'
docSourcesRootPath = os.path.expanduser('~/Documents/of/ofSite/_documentation')

# Path to the Pandoc executable. If Pandoc is in your path you can do pandocExe = 'pandoc'
# Example:
# pandocExe = 'C:\Users\username\AppData\Local\Pandoc\pandoc.exe'
pandocExe = os.path.expanduser('~/AppData/Local/Pandoc/pandoc.exe')

# If these 2 paths are set, no need to read further, you can run the script




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
        print 'Convert "' + fileRelPath + '" to HTML'
        command = '"' + pandocExe + '" "' + filePath + '" -s --toc -o "' + htmlPath
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

def parseFunctionLink( a, fileRelPath ):
    
    """Extract the function name, the function signature, and the anchor from a link HTML tag <a>.
    Return ( success, name, signature, anchor ) where success is True or False."""
    
    content = a.string
    if content is None :
        m = re.search( '.*?>([^\(]+(\w+)\(.*)<', str(a) )
        if m is None:
            print colorama.Fore.RED
            print 'Unable to read function name in file ' + fileRelPath
            print 'Tag:'
            print a
            print colorama.Style.RESET_ALL
            return ( False, '', '' ) 
        else:
            functionSignature = m.group(1)
            functionName = m.group(2)

            print colorama.Fore.BLUE + 'Verify this function name from ' + fileRelPath
            print functionName + '()' + colorama.Style.RESET_ALL
            return ( True, functionName, functionSignature )
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

    # print 'Parsing ' + fileRelPath
    soup = BeautifulSoup( open( htmlPath ), "html5lib" )
        
    # Find table of content
    toc = soup.find(id='TOC')
    
    # Find all the functions
    functionsList = toc.ul.li.ul.li.ul
    if functionsList is None:
        print colorama.Fore.YELLOW + 'No function list found in ' + fileRelPath + colorama.Style.RESET_ALL
        return
        
    functions = functionsList.find_all('li')
    
    for function in functions:
    
        # Find function name
        ( success, functionName, functionSignature ) = parseFunctionLink( function.a, fileRelPath )
        if not success:
            continue
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
    tocLi = toc.ul.li
    if toc is None or tocLi is None:
        print colorama.Fore.RED + 'No TOC found in ' + fileRelPath + colorama.Style.RESET_ALL
        return
    
    # Find class name
    title = tocLi.a.string
    m = re.search( '^class\s+(\w+)_?', title )
    if m is None:
        return
        
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
        print 'Method found: ' + className + '::' + functionName + '()'
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
