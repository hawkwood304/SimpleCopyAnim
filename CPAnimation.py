import maya.cmds as cm
import json
import os

ScriptVar = cm.internalVar(userScriptDir=True)
DIRECTORY = os.path.join(ScriptVar , 'TemporaryAnim')

Author = {
    "Thi": "Junior technical artist" ,
}


def createDirectory():
    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)


def CopyAnimation():
    createDirectory()
    selection = cm.ls(sl=True , type='transform')
    infoFile = os.path.join(DIRECTORY , 'temporaryAnim.json')
    with open(infoFile , 'w') as f:
        json.dump(Author , f , indent=4)

    for obj in selection:
        try:
            nameCtr = obj.split(':')[-1]
        except:
            nameCtr = obj

        listAttr = cm.listAttr(obj , keyable=True) or []

        if len(listAttr) != 0:

            for attr in listAttr:

                listKeyframes = cm.keyframe('{}.{}'.format(obj , attr) , query=True) or []

                if len(listKeyframes) != 0:
                    for i in listKeyframes:
                        animDic = {
                            "{0}.{1}/{2}".format(nameCtr , attr , i): cm.getAttr('{}.{}'.format(obj , attr) , time=i)
                        }

                        with open(infoFile) as f:
                            data = json.load(f)
                        data.update(animDic)

                        with open(infoFile , 'w') as f:
                            json.dump(data , f , indent=4 , sort_keys=True)


def PasteAnimation():
    selection = cm.ls(sl=True , type='transform')
    infoFile = os.path.join(DIRECTORY , 'temporaryAnim.json')
    with open(infoFile , 'r') as f:
        data = json.load(f)

    for obj in selection:
        try:
            nameCtr = obj.split(':')[-1]
        except:
            nameCtr = obj

        for eachLine in data:
            time = eachLine.split('/')[-1]
            name = eachLine.split('/')[0]
            if str(nameCtr) in str(name):
                newName = name.replace(nameCtr, obj)
                value = data.get(eachLine)
                cm.setKeyframe(newName, v=value, t=time)