try :
    import httplib
except:
    import http.client as httplib
    
import urllib.request
import urllib.error
import os
import ImageDownloaderLib as imgLib
import datetime
import time
import sys

## DECLARATION ##
pathDest = ""
dataCount = 0
numFolder = 0
linkCount = 0
linkData = []
dirData = []
tempData = []
extData = ["jpeg", "jpg", "png", "bmp", "gif"]
rowNumbering = 1
_fileLogExists = -1
_logFileName = ""
_firstFolderName = ""
pathFileSource = ""

## SUMMARY DECLARATION ##
_summary = []
_successEachItem = 0
_failedEachItem = 0
_successAllItem = 0
_failedAllItem = 0
_currentTime = ""



## SUPPORT FUNCTION ##
def splitterDirectory(Items):
    resData = Items.split('|')
    return resData

def splitterLink(linkData):
    resData = linkData.split(',')
    return resData

def validationUrl(listUrl):
    joinCode = -1
    res = []

    if(len(listUrl) < 2):
        return listUrl
    
    for iUrl in range(len(listUrl)):
        if(len(listUrl[iUrl]) >= 4):
            if(listUrl[iUrl][:4].lower() != "http"):
                res[len(res)-1] += ',' + listUrl[iUrl]
            else :
                res.append(listUrl[iUrl])
        else:
            res[len(res)-1] += ',' + listUrl[iUrl]
    return res

def createLogFile(path, filename, writeLine):
    fullpath = path + '\\' + str(filename)
    global _fileLogExists
    if((os.path.exists(fullpath) == False) or ((os.path.exists(fullpath) == True) and (_fileLogExists != -1))):
        f= open(fullpath,"a+")
        f.write(writeLine+'\n')
        f.close()
        
    elif((os.path.exists(fullpath) == True) and (_fileLogExists == -1)) :
        f= open(fullpath,"w+")
        f.write(writeLine+'\n')
        f.close()

def renameLogFile(path, oldName, newName):
    fullPathOld = path + '\\' + str(oldName)
    fullPathNew = path + '\\' + str(newName)
    if(os.path.exists(fullPathOld) == True) :
        os.rename(fullPathOld, fullPathNew)

def printAllItemSummary(summaryData, successCount, failedCount):
    successText = "Success"
    failedText = "Failed"
    itemIdText = "Item ID"
    _startTime = ""
    _finishTime = ""
    
    _resText = ""
    _resText += '\n'
    _resText += ('=' * 28) + '\n'
    _resText += (f'{f"|  {successText}":<12}{f"|":<3}{f"{failedText}":<12}{f"|":<1}') + '\n'
    _resText += ('=' * 28) + '\n'
    _resText += (f'{f"|  {str(successCount)}":<12}{f"|":<3}{f"{str(failedCount)}":<12}{f"|":<1}') + '\n'
    _resText += ('=' * 28) + '\n'

    _resText += ('\n') + '\n'
    _resText += ('=' * 165) + '\n'
    _resText += (f'{f"|":<3}{f"Item ID":<17}{f"|":<3}{f"Directory":<50}{f"|":<3}{f"Success":<10}{f"|":<3}{f"Failed":<9}{f"|":<3}{f"Start time":<30}{f"|":<3}{f"Finish time":<30}{f"|":<1}') + '\n'
    _resText += ('|' + ('-' * 163) + '|')

    print(_resText)
    createLogFile(pathDest, _logFileName, _resText)
    
    for iSummary in summaryData:
        _startTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(iSummary[3]))
        _finishTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(iSummary[4]))
        _resText = (f'{f"|":<3}{f"{str(iSummary[0])}":<17}{f"|":<3}{f"{str(iSummary[5])}":<50}{f"|":<3}{f"{str(iSummary[1])}":<10}{f"|":<3}{f"{str(iSummary[2])}":<9}{f"|":<3}{f"{str(_startTime)}":<30}{f"|":<3}{f"{str(_finishTime)}":<30}{f"|":<1}')
        print(_resText)
        createLogFile(pathDest, _logFileName, _resText)
    _resText = ('=' * 165)
    print(_resText)
    createLogFile(pathDest, _logFileName, _resText)

def printItemDownloadSummary(successCount, failedCount, startTime, finishTime):
    successText = "Success : " + str(successCount)
    failedText = "Failed : " + str(failedCount)
    startTimeText = "Finish time : "
    _resText = ""
    
    _startTime = "Start time : " + (time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(startTime)))
    _finishTime = "Finish time : " + (time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(finishTime)))

    _resText += (f'{f"|  Downloading summary":<28}{f"|":<3}{f"{successText}":<22}{f"|":<3}{f"{failedText} ":<22}{f"|":<62}{f"{_startTime}":<43}{f"|":<3}{f"{_finishTime}":<43}{f"|":<1}') + '\n'
    _resText += ('=' * 230)

    print(_resText)
    createLogFile(pathDest, _logFileName, _resText)
    

def printItemDownloadResult(downloadResultData, lenDataResult, dataNumber, startTime = 0, finishTime = 0):
  
    numData = "{0:0=3d}".format(dataNumber)
    downloadStatus = downloadResultData[0]
    fileName = downloadResultData[1]
    urlDownload = downloadResultData[2]

    _resText = ""
    
    _resText = (f'{f"| {numData}":<6}| {f"{downloadStatus}":<12} | {f"{fileName}":<14} | {f"{urlDownload}":<188}{f"|":<1}')
    print(_resText)
    createLogFile(pathDest, _logFileName, _resText)
    
    if((dataNumber >= lenDataResult) and (startTime != 0 and finishTime != 0)) :
        dataNumber = 1
        _resText = ('=' * 230)
        print('=' * 230)
        createLogFile(pathDest, _logFileName, _resText)
        
        printItemDownloadSummary(_successEachItem, _failedEachItem, startTime, finishTime)
        

def printTaskHeader(linkData, proccesLine, itemId, path, totalData):
    proccesText = " Procces line - "
    itemIdTex = " Item ID : "
    dirText = "Directory : "
    totalText = "Total : " + str(totalData)
    _resText = ""
    
    _resText += ('\n')
    x = 1
    _resText += ('=' * 230) + '\n'
    _resText += (f'{f"| {proccesText}":<1}{f"{str(proccesLine)}":<10}| {f"{itemIdTex}":<10}{f"{str(itemId)}":<25}{f"|":<3}{f"{str(dirText)}":<3}{f"{str(path)}":<128}{f"|":<3}{f"{totalText}":<17}{f"|":<1}') + '\n'
    _resText += ('=' * 230)

    print(_resText)
    createLogFile(pathDest, _logFileName, _resText)

def clear():
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

def getLenFile(fullpath):
    lenFile = 0
    iTest = 0
    if(os.path.exists(fullpath) != True):
        return "File nothing"
    else :
        fileInput = open(fullpath, "r")

        for iLine in fileInput:
            if(iTest == 0):
                iTest = 1
            elif(iTest != 0):
                lenFile += 1

        fileInput.close()

        
    return lenFile

def getDirectoryFromFile(fullpath):
    res = ""

    if(os.path.exists(fullpath) != True):
        return "File nothing"
    else :
        fileInput = open(fullpath, "r")

        res = fileInput.readline().replace('\n', '')

        fileInput.close()

        return res

def getListTaskFromFile(fullpath):
    res = []
    iTest = 0
    _res = ""

    if(os.path.exists(fullpath) != True):
        return "File nothing"
    else :
        fileInput = open(fullpath, "r")

        for iLine in fileInput:
            if(iTest == 0):
                iTest = 1
            elif(iTest != 0):
                _res = iLine
                res.append(_res.replace('\n', ''))

        fileInput.close()

    return res

## MAIN FUNCTION ##

## INPUT SELECTION ##
_wrongInputCounter = 0
inputSelection = -1
while((inputSelection < 1 or inputSelection > 2) and _wrongInputCounter < 3):
    try:
        print("Select your input type :")
        print("1. Manual\n2. Text file")
        inputSelection = int(input("Input type : "))

        if(inputSelection < 1 or inputSelection > 2):
            raise Exception()
    except:
        print("Sorry, your input invalid. Please try again.\n")
        inputSelection = -1
        _wrongInputCounter += 1

if(inputSelection == -1):
    print("Sorry, your chance was null. You can try running again")
    time.sleep(2)
    sys.exit()
elif(inputSelection == 1) :
    ## INPUT PATH AND COUNT ITEM ##
    pathDest = input("Destination Folder : ")
    dataCount = int(input("Process Count : "))
    print("Plese input your data : ")
    
elif(inputSelection == 2) :
    pathFileSource = input("Full path your file (.txt) : ")
    fileSourceName = ""
    fileSourceExt = ""
    taskListFile = []
    try : 
        if(os.path.exists(pathFileSource) and os.path.isfile(pathFileSource)):
           
            fileSourceName, fileSourceExt = os.path.splitext(pathFileSource)
            if(fileSourceExt == ".txt"):
                pathDest = getDirectoryFromFile(pathFileSource)
                dataCount = int(getLenFile(pathFileSource))
                taskListFile = getListTaskFromFile(pathFileSource)
            else:
                raise Exception("You file is not text (.txt) file")
        else : 
            raise Exception("You input invalid. Please check again!")
    except:
        print("You input invalid. Please check again!")
        sys.exit()
        

## LOOPING PROGRESS ##
for i in range(0, dataCount):
    # Clear last data #
    nameFolder = ""
    linkCount = 0
    linkData = []
    dirData = []
    tempData = []
    extData = ""
    subResData = []
    iLink = 0
    tempLink = ""
    pathNow = ""
    resDataDownload = []
    _tempLog = ""
    _startTime = 0
    _finishTime = 0
    _pathNowTemp = []
    _nameFolder = ""
    
    # Processing #
    if(inputSelection == 1):
        dataItem = input()
    elif(inputSelection == 2):
        dataItem = taskListFile[i]
    nameFolder = int(splitterDirectory(dataItem)[0])
    linkData = validationUrl(splitterLink(splitterDirectory(dataItem)[1]))
    linkCount = len(linkData)

    #Create folder at item #
    _nameFolder = nameFolder
    _existsFolderNameCounter = 1
    _pathNowTemp = imgLib.createNewFolder(pathDest, _nameFolder)
    pathNow = _pathNowTemp[1]
    while(_pathNowTemp[0] == "Failed"):
        _nameFolder = splitterDirectory(dataItem)[0] + '_' + str(_existsFolderNameCounter)
        _pathNowTemp = imgLib.createNewFolder(pathDest, _nameFolder)
        pathNow = _pathNowTemp[1]
        _existsFolderNameCounter += 1
    
    ## GENERATE LOG FILE##
    if(i == 0):
        _firstFolderName = str(nameFolder)
        _logFileName = _firstFolderName + "_" + str(dataCount) + "_"  + "Writing_LOG_LOG.txt"
        _tempLog = "Destination Folder : " + pathDest + "\nProcess Count : " + str(dataCount) + "\nData download process : \n"
        createLogFile(pathDest, _logFileName, _tempLog)
        _fileLogExists = 1

        

    #Downloading #
    printTaskHeader(linkData, i+1, splitterDirectory(dataItem)[0], pathNow, linkCount)
    for itemLink in linkData:
        iLink += 1
        extData = imgLib.getExtImage(itemLink)
        if(extData[0] != "Failed"):
            filename = imgLib.filenameCombine(str(nameFolder) + '_' + "{0:0=3d}".format(iLink), extData[1])
        else:
            filename = "-"
        tempLink = extData[3]
            
        tempData = imgLib.downloadImage(tempLink, pathNow, filename)
        
        # Summary process #
        if(tempData[0][:1] == 'S'):
            _successEachItem += 1
        else:
            _failedEachItem += 1
        

        if(linkCount == 1) and (iLink == 1):
            _startTime = tempData[4]
            _finishTime = tempData[5]
            printItemDownloadResult(tempData, linkCount, iLink, startTime = _startTime, finishTime = _finishTime)
        elif(iLink == 1 and linkCount > 1):
            _startTime = tempData[4]
            printItemDownloadResult(tempData, linkCount, iLink)
        elif(iLink < linkCount):
            printItemDownloadResult(tempData, linkCount, iLink)
        elif(iLink == linkCount):
            _finishTime = tempData[5]
            printItemDownloadResult(tempData, linkCount, iLink, startTime = _startTime, finishTime = _finishTime)
    
        

    # Summary all data #
    _successAllItem += _successEachItem
    _failedAllItem += _failedEachItem

    resDataDownload = [nameFolder, _successEachItem, _failedEachItem, _startTime, _finishTime, pathNow]
    _summary.append(resDataDownload)
    
    # Reset summary each item #
    _successEachItem = 0
    _failedEachItem = 0
    resDataDownload = []

printAllItemSummary(_summary, _successAllItem, _failedAllItem)

_currentTime = time.strftime("%d-%m-%Y_%H.%M.%S", time.localtime())
_newLogFile = _firstFolderName + "_" + str(dataCount) + "_"  + _currentTime + "_LOG.txt"

renameLogFile(pathDest, _logFileName, _newLogFile)

os.chdir(os.getcwd())

