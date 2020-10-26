try :
    import httplib
except:
    import http.client as httplib
from socket import timeout
import urllib.request
import urllib.error
import os
import os.path
import ssl
import time
import socket

ssl._create_default_https_context = ssl._create_unverified_context

numFolder = 0
linkCount = 0
linkData = []
dirData = []
tempData = []

extData = ["jpeg", "jpg", "png", "bmp", "gif"]

def checkConnection():
    dummyUrl = "www.google.com"
    dummyTimeOut = 3
    conn = httplib.HTTPConnection(dummyUrl, timeout=dummyTimeOut)

    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except Exception as e:
        return False

def getExtImage(url):
    """
    Result :
    [0] = Status
    [1] = Extention
    [2] = URL
    [3] = Minimized URL
    """
    res = []
    tempRes = ""
    subRes = url.split('.')
    splitItem = ""
    extTemp = ""
    extNow = ""
    foundCode = -1
    status = ""
    
    for iUrl in range(len(subRes) - 1, 0, -1):
        splitItem = subRes[iUrl]
        for iExt in extData:
            if(len(iExt) <= len(splitItem)):
                extTemp = splitItem[:len(iExt)]
                if(extTemp.lower() == iExt.lower()):
                    foundCode = iUrl
                    extNow = iExt.lower()
                    break
        if(foundCode > -1):
            break
        
    if(foundCode > -1):
        for iLinkItem in range(0, foundCode + 1):
            if(iLinkItem < foundCode):
                tempRes += subRes[iLinkItem] + '.'
            else:
                tempRes += extNow
        status = "Succes"
    else :
        tempRes = url
        status = "Failed"
    splitItem = subRes[len(subRes) - 1]
    
    res = [status, extNow, url, tempRes]
    
    return res;

def filenameCombine(filename, ext):
    if(ext[0] == '.'):
        return filename + ext
    else:
        return filename + '.' + ext

def pathCombine(path, filename):
    res = ""
    if(path[len(path)-1] == '\\' or path[len(path)-1] == '/'):
        res = path + filename
    else:
        res = path + '\\' + filename

    return res

def createNewFolder(path, folderName):
    res = []
    
    if(os.path.exists(path + '\\' + str(folderName)) == False):
        os.chdir(path)
        os.mkdir(str(folderName))
        res = ["success", str(path) + '\\' + str(folderName)]
    else :
        res = ["Failed", str(path)]

    return res
        

def statusDownload(reqCode):
    res = ""
    tempReqCode = 0
    try :
        tempReqCode = int(reqCode)
    except:
        res = "StatusDownload function Error"
    
    if(tempReqCode >= 200 and tempReqCode <= 299):
        res = "Success (" + str(reqCode) + ")"
    else:
        res = "Failed (" + str(reqCode) + ") "

    return res

def downloadImage(url, path, filename):
    """
    Result :
    [0] = Status
    [1] = Filename
    [2] = URL
    [3] = Full path
    [4] = Start time (time)
    [5] = Finish time (time)
    """
    startTime = time.time()
    res = []
    reqCode = 0
    fileNameTemp = ""
    
    fullpath = pathCombine(path, filename)
    if(checkConnection() == True):
        try:
            request = urllib.request.urlopen(url, timeout=30)
            reqCode = request.getcode()
        except (timeout, socket.error,urllib.error.URLError, urllib.error.HTTPError): 
            reqCode = 408
            fileNameTemp = "-"
        if(reqCode > 199 and reqCode < 300):
            if(os.getcwd() != path):
                os.chdir(path)
            try:
                downloading, downloadHeader = urllib.request.urlretrieve(url,fullpath)
                fileNameTemp = filename
            except (urllib.error.URLError) as e1:
                reqCode = 901
                fileNameTemp = "-"
            except (urllib.error.HTTPError) as e2:
                reqCode = e2.code
                fileNameTemp = "-"
            except (urllib.error.ContentTooShortError) as e:
                reqCode = 902
                fileNameTemp = "-"
            else:
                if(reqCode == 0):
                    reqCode = -1
                
        finishTime = time.time()
        res = [statusDownload(reqCode), fileNameTemp, url, path, startTime, finishTime] 
        
        return res
    else:
        print("Connection is lost")
    

##- Check connection -##
if(checkConnection() == True) :
    print("========================")
    print("| Your connection good |")
    print("========================")

else :
    print("=====================================")
    print("| Connection lost, please try again |")
    print("=====================================")
