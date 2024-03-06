import os
import sys

try:
    import maya.mel
    import maya.cmds
    isMaya = True
except ImportError:
    isMaya = False

def onMayaDroppedPythonFile(*args, **kwargs):
    pass

def _onMayaDropped():

    srcPath = os.path.join(os.path.dirname(__file__))
    iconPath = os.path.join(srcPath,  'icon', 'blocKeys.png')

    srcPath = os.path.normpath(srcPath)
    iconPath = os.path.normpath(iconPath)

    if not os.path.exists(iconPath):
        raise IOError('Cannot find ' + iconPath)


    command = '''
import os

script_dir = cmds.internalVar(userScriptDir=True)
script_path = os.path.join(script_dir, "blocKeys", "script", "blocKeys.py")

with open(script_path, "r") as script_file:
    exec(script_file.read())
'''.format(path=srcPath)

    shelf = maya.mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = maya.cmds.tabLayout(shelf, query=True, selectTab=True)
    maya.cmds.shelfButton(
        command=command,
        annotation='Blockeys',
        sourceType='Python',
        image=iconPath,
        image1=iconPath,
        parent=parent
    )


if isMaya:
    _onMayaDropped()
