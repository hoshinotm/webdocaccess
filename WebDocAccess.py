####
# Prints out each line of a given document on the web.
# Name of the host  and name of the document may be
# specified as unnamed arguments on the command line.
#

import sys
from enum import Enum
import socket

DEFAULT_HOST_NAME = 'data.pr4e.org'
DEFAULT_DOC_NAME = 'intro-short.txt'

#################
# Enum Args
# Defines optional command line argument positions
#
class Args(Enum):
    SCRIPT_NAME_POS = 0
    HOST_NAME_POS = 1
    DOC_NAME_POS = 2

#################
# get_host_name()
# Returns a host name from command line arguments, or
# a default host name if none is specified in the command line
#
def get_host_name():
    if len(sys.argv) < 2:
        return DEFAULT_HOST_NAME
    else:
        return sys.argv[Args.HOST_NAME_POS]

#################
# get_doc_name()
# Returns a document name from command line arguments, or
# a default doc. name if none is specified in the command line
#
def get_doc_name() :
    if len(sys.argv) < 3 :
        return DEFAULT_DOC_NAME
    else :
        return sys.argv[Args.DOC_NAME_POS]


##################
# format_get_cmd()
# Returns a standard GET command string, using given host name
# and document name.
#
def format_get_cmd( host_name, doc_name ):
    GET_CMD_TEMPLATE = 'GET http://{}/{} HTTP/1.0\r\n\r\n'
    return GET_CMD_TEMPLATE.format(host_name, doc_name).encode()

##################
# send_get()
# Creates a socket; connects to a given host through a given port;
# sends out an initial GET request; and returns the socket
#
def send_get( host_name, doc_name ):
    mysock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    mysock.connect( (host_name, 80) )  # parameter is a tuple of domain name and port#
    mysock.send( format_get_cmd(host_name,doc_name))
    return mysock

###################
#
#  Main
#
mysock = send_get( get_host_name(), get_doc_name() )
while True:
    data = mysock.recv(512)     # Receive up to 512 chars
    if (len(data) < 1):         # If EOF, quit
        break
    print(data.decode())
mysock.close()
