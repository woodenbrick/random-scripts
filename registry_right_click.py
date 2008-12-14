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