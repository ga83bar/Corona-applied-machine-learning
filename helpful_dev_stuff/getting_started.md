# Getting Started
## GROUP : ml_boyz


## Doxygen :
- doxygen is a code documentation tool !! Use it!!
- For using it you just have to make this kind of comments - '''Simple Python doxy comment'' - in your function.
- You just have to download doxygen (LINUX: sudo apt-get install doxygen)
- the system is ready to use (LINUX: in the current working directory --> CWD doxygen aml_doxy_conf.dxy
- Then go to documentation/latex and make the .pdf file (LINUX : make)

## Filepaths :
- as we probably will/must work with different operating systems use the command -os.path.join() - to create paths!!!

## Python : virtual enviroment
- 

## Interfaces :
- Informations of how to implement this Interfaces :
  https://www.python-course.eu/python3_abstract_classes.php
- The extrem short version would be 
   * inherit interface to your class (ideally with the same name only without i) e.g. class Data(iData): .....
   * copy the methods and overwrite them =)


## PEP8 :
- we want PEP8 compliant code
- please have a look at this 5 minutes tutorial (see : https://pybit.es/pep8.html)
- who takes it exactly can also read the long version (see : https://pep8.org/)

## VSCODE 
- we recommend that you use vscode

### Setup launch.json
- this file is a powerful tool to manage different debug settings (see : https://code.visualstudio.com/docs/editor/debugging)
- example :
```python
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        {
            "preLaunchTask": "prelaunch",
            "postDebugTask": "postlaunch",
            "name": "debug main",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "stopOnEntry": true
        }
    ]
}
```
    
### Setup task.json
- This file defines different tasks that can be executed before and after the code
- example :
```python
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "prelaunch",
            "type": "shell",
            
            "linux":{
                "command": "${workspaceFolder}/scripts/activate_venv.sh",
            },
            "windows": {
                "command": "${workspaceFolder}\\scripts\\activate_venv.cmd"
            }
        },
        {
            "label": "postlaunch",
            "type": "shell",

            "linux":{
                "command": "${workspaceFolder}/scripts/disable_venv.sh",
            },
            "windows": {
                "command": "${workspaceFolder}\\scripts\\disable_venv.cmd"
            }
        }
    ]
}
```

## Logging
- Please do not use print() instead use logging.info('message') or logging.error('mes') (see : https://docs.python.org/3/library/logging.html)