#!/usr/bin/env python
import subprocess
import optparse
import re

#Create variables out of shell commands
#Note triple quotes can embed Bash

#You could add another bash command here
#HOLDING_SPOT="""fake_command"""


TOPFIRST="{history 0}" | sed 's/^\ *//' | cut -d' ' -f3-"

TOPSECOND=""# " | sort | uniq -dc | sort -gr} "

TOPCMD="tee "
for i in range(3,23):
    TOPCMD = TOPCMD + TOPFIRST + str(i) + TOPSECOND
TOPCMD = TOPCMD + """| awk 1 RS= ORS="\n\n" | $PAGER"""

#This function takes Bash commands and returns them
def runBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read().strip()
    return out  #This is the stdout from the shell command

VERBOSE=False
def report(output,cmdtype="UNIX COMMAND:"):
   #Notice the global statement allows input from outside of function
   if VERBOSE:
       print "%s: %s" % (cmdtype, output)
   else:
       print output

#Function to control option parsing in Python
def controller():
    global VERBOSE
    #Create instance of OptionParser Module, included in Standard Library
    p = optparse.OptionParser(description='TopCMD',
                                            prog='tc',
                                            version='tc 0.1',
                                            usage= '%prog [option]')
    p.add_option('--usage', '-u', action="store_true", help='gets disk usage of homedir', default=False)

    #Option Handling passes correct parameter to runBash
    options, arguments = p.parse_args()
    if options.usage:
        value = runBash(TOPCMD)
        report(value, "TOP_CMD")
    else:
        p.print_help()

#Runs all the functions
def main():
    controller()

#This idiom means the below code only runs when executed from command line
if __name__ == '__main__':
    main()
