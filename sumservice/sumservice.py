#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# Service configuration file for CLAM
###############################################################

#Consult the CLAM documentation at https://clam.readthedocs.io/

from clam.common.parameters import ChoiceParameter, BooleanParameter, StaticParameter
from clam.common.formats import PlainTextFormat
from clam.common.data import InputTemplate, OutputTemplate, Profile, SetMetaField, loadconfig
from clam.common.digestauth import pwhash
import clam
import sys
import os

#The minimum version of CLAM that is required by this service
REQUIRE_VERSION = 3.2

CLAMDIR = clam.__path__[0] #directory where CLAM is installed, detected automatically
WEBSERVICEDIR = os.path.dirname(os.path.abspath(__file__)) #directory where this webservice is installed, detected automatically

# ======== GENERAL INFORMATION ===========

# General metadata concerning your system.

#The System ID, a short alphanumeric identifier for internal use only (mandatory!)
SYSTEM_ID = "sumservice"
#System name, the way the system is presented to the world
SYSTEM_NAME = "Summarisation Service"

#An informative description for this system (this should be fairly short, about one paragraph, and may not contain HTML)
SYSTEM_DESCRIPTION = "An automatic summarisation service for several languages"

#A version label of the underlying tool and/or this CLAM wrapper
#(If you can derive this dynamically then that is strongly recommended! It should be the same as in your setup.py)
SYSTEM_VERSION = 0.1

#The author(s) of the underlying tool and/or this CLAM wrapper
#(If you can derive this dynamically then that is strongly recommended!)
SYSTEM_AUTHOR = "Maarten van Gompel"

#How to reach the authors?
SYSTEM_EMAIL = "proycon@anaproy.nl"

#Does this system have a homepage (or possibly a source repository otherwise)
#SYSTEM_URL = ""

#Is this webservice embedded in a larger system? Like part of an institution or particular portal site. If so, mention the URL here.
#SYSTEM_PARENT_URL = ""

#The URL of a cover image to prominently display in the header of the interface. You may also want to set INTERFACEOPTIONS="centercover" to center it horizontally.
#SYSTEM_COVER_URL = ""

#URL to a website where users can register an account for use with this webservice. This link is only for human end
#users, not an API endpoint.
#SYSTEM_REGISTER_URL = ""

#Amount of free memory required prior to starting a new process (in MB!), Free Memory + Cached (without swap!). Set to 0 to disable this check (not recommended)
REQUIREMEMORY = 100


# ======== EXTERNAL CONFIGURATION ===========

#specify these variables in an external yaml file
#called $hostname.yaml or config.yaml and use the loadconfig() mechanism.
#Such an external file will be looked for my default and is the recommended way.

#This invokes the automatic loader, do not change it;
#it will try to find a file named $system_id.$hostname.yml or just $hostname.yml, where $hostname
#is the auto-detected hostname of this system. Alternatively, it tries a static $system_id.config.yml or just config.yml .
#You can also set an environment variable CONFIGFILE to specify the exact file to load at run-time.
#It will look in several paths including the current working directory and the path this settings script is loaded from.
#Such an external configuration file simply defines variables that will be imported here. If it fails to find
#a configuration file, an exception will be raised.
loadconfig(__name__)


#Allow Asynchronous HTTP requests from **web browsers** in following domains (sets Access-Control-Allow-Origin HTTP headers), by default this is unrestricted
#ALLOW_ORIGIN = "*"

# ======== WEB-APPLICATION STYLING =============

#Choose a style (has to be defined as a CSS file in clam/style/ ). You can copy, rename and adapt it to make your own style
STYLE = 'classic'

# ======== ENABLED FORMATS ===========

#In CUSTOM_FORMATS you can specify a list of Python classes corresponding to extra formats.
#You can define the classes first, and then put them in CUSTOM_FORMATS, as shown in this example:

#class MyXMLFormat(CLAMMetaData):
#    attributes = {}
#    name = "My XML format"
#    mimetype = 'text/xml'




# CUSTOM_FORMATS = [ MyXMLFormat ]

# ======== ENABLED VIEWERS ===========

#In CUSTOM_VIEWERS you can specify a list of Python classes corresponding to extra viewers.
#You can define the classes first, and then put them in CUSTOM_VIEWERS, as shown in this example:

# CUSTOM_VIEWERS = [ MyXMLViewer ]

# ======= INTERFACE OPTIONS ===========

#Here you can specify additional interface options (space separated list), see the documentation for all allowed options
#INTERFACEOPTIONS = "inputfromweb" #allow CLAM to download its input from a user-specified url
#INTERFACEOPTIONS = "disableliveinput"

# ======== PROJECTS: PROFILE DEFINITIONS ===========

#Define your profiles here. This is required for the project paradigm, but can be set to an empty list if you only use the action paradigm.

PROFILES = [
    Profile(
        InputTemplate('InputTextfile',PlainTextFormat,"Plain text file",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('Summary',PlainTextFormat,'Plain text file',
            SetMetaField('encoding','utf-8'),
            removeextension=".txt",
            extension='.summary.txt',
            multi=True
        ),
    )
]

# ======== PROJECTS: COMMAND ===========

#The system command for the project paradigm.
#It is recommended you set this to small wrapper
#script around your actual system. Full shell syntax is supported. Using
#absolute paths is preferred. The current working directory will be
#set to the project directory.
#
#You can make use of the following special variables,
#which will be automatically set by CLAM:
#     $INPUTDIRECTORY  - The directory where input files are uploaded.
#     $OUTPUTDIRECTORY - The directory where the system should output
#                        its output files.
#     $TMPDIRECTORY    - The directory where the system should output
#                        its temporary files.
#     $STATUSFILE      - Filename of the .status file where the system
#                        should output status messages.
#     $DATAFILE        - Filename of the clam.xml file describing the
#                        system and chosen configuration.
#     $USERNAME        - The username of the currently logged in user
#                        (set to "anonymous" if there is none)
#     $PARAMETERS      - List of chosen parameters, using the specified flags
#
COMMAND = WEBSERVICEDIR + "/sumservice_wrapper.py $DATAFILE $STATUSFILE $OUTPUTDIRECTORY"

#Or if you only use the action paradigm, set COMMAND = None

# ======== PARAMETER DEFINITIONS ===========

#The global parameters (for the project paradigm) are subdivided into several
#groups. In the form of a list of (groupname, parameters) tuples. The parameters
#are a list of instances from common/parameters.py

PARAMETERS =  [
    ('Global', [
        BooleanParameter(id='gpu',name="GPU", description="Use GPU (improves performance but may not always be available)",default=True),
        ChoiceParameter(id='language',name='Language',description='The language of the input texts and output summaries', choices=[ ('nl','Dutch  / Nederlands')],default='nl'),
    ])
]
