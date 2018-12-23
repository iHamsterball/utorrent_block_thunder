import requests
import re
import json
from requests.cookies import RequestsCookieJar
import time
import os


def getTokenPage(url,cookie_jar):
    headers = {'Authorization': 'Basic MTox'}
    tokenUrl = url+"token.html"
    rsp = requests.get(tokenUrl, headers=headers,cookies =cookie_jar)
    print (rsp)
    return  rsp.content

def getToken(html):
    html = re.sub(r'<html><div id=\'token\' style=\'display:none;\'>', "", html)
    html = re.sub(r'</div></html>', "", html)
    return html

def getDownloadItem(url,token,cookie_jar):
    headers = {'Authorization': 'Basic MTox'}
    content = {'token': token ,'list' : 1}
    rsp = requests.get(url,params=content,headers=headers,cookies = cookie_jar)
    # print (rsp.url)
    # print (rsp)
    return str(rsp.content,'utf-8')

def getAlltorrents(downItem):
    allDict = json.loads(downItem)
    return  allDict['torrents']

#将正在下载和做种的种子hash返回
def getTorrentHashAndStatus(Torrent):
    hash = Torrent[0]
    status = Torrent[21]
    # for i in Torrent:
    #     #     print("序号：%s   值：%s" % (Torrent.index(i) + 1, i))
    if "Seeding" in status or "Downloading" in status:
        return hash
def queryTorrentClient(url,token,cookie_jar,hash):
    blockList = []
    headers = {'Authorization': 'Basic MTox'}
    # action = getpeers & hash = 5
    # D52 & t = 1545584374277
    content = {'token': token ,'action': "getpeers", 'hash': hash,'t' : int(time.time())}
    rsp = requests.get(url, params=content, headers=headers, cookies=cookie_jar)
    PeersInfo = json.loads(str(rsp.content, 'utf-8'))['peers']
    # print (allPeers[1])
    allPeer = PeersInfo[1]
    for peer in allPeer:
        if isNeedBlockClient(peer):
            blockList.append(peer)
    return blockList

def reloadipfilter(url,token,cookie_jar):
    blockList = []
    headers = {'Authorization': 'Basic MTox'}
    # action = getpeers & hash = 5
    # D52 & t = 1545584374277
    content = {'token': token ,'action': "setsetting", 's': 'ipfilter.enable','v' : 1}
    rsp = requests.get(url, params=content, headers=headers, cookies=cookie_jar)
    print (rsp.status_code)

def getAllFilerClient(NeedQueryList,url,token,cookie_jar):
    blockAllList = []
    for oneTorrentHash in NeedQueryList:
        blockList = queryTorrentClient(url,token,cookie_jar,oneTorrentHash)
        if blockList is not None:
            blockAllList.append(blockList)
    return(blockAllList)

def isNeedBlockClient(peer):
    if "XL0012" in peer[5] or "Xunlei" in peer[5] or "Xfplay" in peer[5] or str(peer[5]).startswith("7."):
        # print (peer[5])
        return True
    return False

def getAllFilerClientIpList(AllFilerClientInfo):
    clientIpList = []
    for peers in AllFilerClientInfo:
        for peer in peers:
            if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",str(peer[1])):
                clientIpList.append(peer[1])
    return clientIpList


def writeToFile(NewFilerClient):
    newAddList = []
    with open(fileAddress, 'r') as f1:
        exsitFilerClient = f1.readlines()
    f1.close()
    countOld = len(exsitFilerClient)
    for ip in NewFilerClient:
        if ip not in ''.join(exsitFilerClient).strip('\n') :
            newAddList.append(ip)
    countNew = len(newAddList)
    with open(fileAddress, 'a+') as f:
        for wirteIp in newAddList:
            f.write(wirteIp + '\n')
        f.close()
    with open('./log.txt', 'a+') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"   add    "+str(countNew) + "  ips"+ '\n')
        f.close()

if __name__ == "__main__":
    while True:
        time.sleep(60)
        fileAddress = r'C:\Users\11\AppData\Roaming\uTorrent\ipfilter.dat'
        Root_url = 'http://127.0.0.1:10000/gui/'
        headers = {'Authorization': 'Basic MTox'}
        response = requests.get(Root_url, headers = headers)
        cookie_jar = response.cookies
        # print(cookie_jar)



        tokenContent = getTokenPage(Root_url,cookie_jar)
        # print(tokenContent)
        content =str(tokenContent,'utf-8')
        token =getToken(content)
        # print (token)

        downItem = getDownloadItem(Root_url,token,cookie_jar)
        # print (downItem)
        torrents = getAlltorrents(downItem)

        NeedQueryList = []
        for torrent in torrents:
        # print (torrents[0])
            BThash = getTorrentHashAndStatus(torrent)
            if BThash is not None:
                NeedQueryList.append(BThash)
                # print (torrent[2])
        print (NeedQueryList)
        AllFilerClientInfo = getAllFilerClient(NeedQueryList,Root_url,token,cookie_jar)
        print (AllFilerClientInfo)
        clientIpList = getAllFilerClientIpList(AllFilerClientInfo)
        print (clientIpList)
        writeToFile(clientIpList)
        reloadipfilter(Root_url,token,cookie_jar)
