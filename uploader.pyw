import sys, os
from _winreg import *


from ftplib import FTP
import webbrowser

website_url = "http://gear.64digits.com/"
server = ''
username = ''
password = ''


def upload(fname):
    remote_folder = "temporary" #this if the folder I want to put my files on the server

    name = os.path.basename(fname) #fetch the filename alone for the remote name
    name = name.replace(" ","-") #take out spaces from the name to make it nice for the web

    #Connect to server
    ftp = FTP(server)
    ftp.login(username, password)
    ftp.cwd('public_html/'+remote_folder) #hop to remote_folder
    ftp.retrlines('LIST') #print out a dir listing for good measure
    
    #Upload the file to the server
    print "Uploading...",
    ftp.storbinary("STOR "+name, open(fname,"rb"))
    ftp.close()
    print "Done!"

    #Show the file in the default browser
    webbrowser.open(website_url+remote_folder+"/"+name)



def register(command_name,association=sys.argv[0],runner="runner.exe"):
    #The params are:
    #name to register as, this shows in in the right click menu for all files
    #the script to associate it with (defaults to this script)
    #the location of the runner (defaults to runner.exe in same place as script)
    
    association = os.path.realpath(association)
    runner = os.path.realpath(runner)

    if not os.path.isfile(runner):
        print "Runder does not exist at "+runner
        return 0
    
    try:
        reg = CreateKey(HKEY_CLASSES_ROOT,"*\\Shell\\"+command_name+"\\Command")
        runner_path = runner.replace("\\","\\\\")
        association_path = association.replace("\\","\\\\")

        key = runner_path + " " +association_path + " %1"
        print command_name+" :: "+key
        SetValue(reg, "", REG_SZ, key)
        CloseKey(reg)
    except:
        print "Failed to set registry"

def unregister(command_name):
    #the param is the name of the command
    try:
        if command_name=="":
            return 0 #don't allow everything under shell to be deleted
        DeleteKey(HKEY_CLASSES_ROOT,"*\\Shell\\"+command_name+"\\Command")
        DeleteKey(HKEY_CLASSES_ROOT,"*\\Shell\\"+command_name)
        print ("Deleted HKEY_CLASSES_ROOT\\"+"*\\Shell\\"+command_name)
    except:
        print "Command "+command_name+" was not registered"


command_name = "Upload"

#If no arguments are given, register ourselves
if len(sys.argv)==1:
    register(command_name)

#Otherwise unregister if the command is -unreg, or otherwise do whatever we want
if len(sys.argv)==2:
    if sys.argv[1] == "-unreg":
        unregister(command_name)
        raw_input("")
        sys.exit()

    #At this point we can call functions to operate on the param given
    #which is the name of the file that was right clicked
    upload(sys.argv[1])





