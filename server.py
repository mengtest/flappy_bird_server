#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import socket, select, netstream, random

user = []   #二人对战
pipeRandomHeight = []   #
battleSize = 2

if __name__ == "__main__":
    s = socket.socket()
    
    host = "127.0.0.1"
    port = 1234
    s.bind((host, port))
    
    s.listen(4)
    
    inputs = []
    inputs.append(s)
    
    while True:
        rs, ws, es = select.select(inputs, [], [])
        for r in rs:
            if r is s:
                # accept
                c, addr = s.accept()
                print 'Got connection from'+str(addr)
                inputs.append(c)
                user.append(c)
                if len(user) == battleSize:  # 游戏开始
                    # 准备pipeRandomHeight信息
                    pipeRandomHeight.append(random.randrange(0, 4))
                    pipeRandomHeight.append(random.randrange(0, 4))
                    pipeRandomHeight.append(random.randrange(0, 4))
                    # 准备sendData信息
                    sendData = {}
                    pipeData = {}
                    pipeData[0] = pipeRandomHeight[0]
                    pipeData[1] = pipeRandomHeight[1]
                    pipeData[2] = pipeRandomHeight[2]
                    sendData['pipe'] = pipeData
                    sendData['start'] = 1
                    sendData['size'] = battleSize
                    # 给user发送
                    for i in range(len(user)):
                        sendData['no'] = i
                        try:
                            netstream.send(user[i], sendData)
                            print 'send data to '+str(user[i].getpeername())+'\tdata is: '+str(sendData)
                        except Exception:
                            print 'Error: 游戏开始，给user'+i+'发送'
            else:
                # receive data
                recvData = netstream.read(r)
                print 'Read data from '+str(r.getpeername())+'\tdata is: '+str(recvData)
                # socket关闭
                if recvData == netstream.CLOSED:
                    print str(r.getpeername())+'disconnected'
                    inputs.remove(r)
                    user.remove(r)
                else:   # 根据收到的request发送response
                    # client请求pipeRandomHeight
                    if 'pipe' in recvData:
                        index = recvData['pipe']
                         # list里没有的话需要广播pipe信息，list里一旦添加就会广播，所以list里有的话说明已经广播过了
                        if index >= len(pipeRandomHeight):
                            sendData = {}
                            pipeData = {}
                            pipeRandomHeight.append(random.randrange(0, 4))
                            pipeData[index] = pipeRandomHeight[index]
                            sendData['pipe'] = pipeData
                            # 对玩家广播
                            for i in range(len(user)):
                                try:
                                    netstream.send(user[i], sendData)
                                    print 'send data to '+str(user[i].getpeername())+'\tdata is: '+str(sendData)
                                except Exception:
                                    print 'Error: 给user'+i+'广播pipe信息'
                    # client通知自己的位置
                    if 'pos' in recvData:
                        pos = recvData['pos']
                        no = recvData['no']
                        sendData = {}
                        sendData['pos'] = pos
                        sendData['no'] = no
                        # 对玩家广播
                        for i in range(len(user)):
                            if i == no:
                                continue
                            try:
                                netstream.send(user[i], sendData)
                                print 'send data to '+str(user[i].getpeername())+'\tdata is: '+str(sendData)
                            except Exception:
                                print 'Error: 给user'+i+'广播pipe信息'                            
    '''
    sock = socket.socket()
    sock.bind(('127.0.0.1', 1234))
    sock.listen(1)
    c, addr = sock.accept()
    data = {}
    dataPipe = {}
    index = 0
    data['start'] = 1
    dataPipe[0] = 0
    dataPipe[1] = 1
    dataPipe[2] = 2
    dataPipe[3] = 3
    data['pipe'] = dataPipe
    netstream.send(c, data)
    print('done')
    '''
    '''
    # test send
    data = {}
    data['login'] = 'chenchao'
    data['wife'] = 'gongyilin'
    #data['hobby'] = '看动画，听音乐，打篮球，玩游戏，哈哈哈'
    data['pipe'] = {'index':15, 'random':3}
    data['bird'] = {'1':111, '2':222, '3':333}
    print("send data: "+str(data))
    netstream.send(c, data)
    #test read
    data2 = netstream.read(c)
    print("read data: "+str(data2))
    if data2['login'] == 'chenchao':
        print("end")
    c.close()
    sock.close()
    '''
    ''' base64
    s = "woshizifuchuan我是字符串"
    a = base64.b64encode(s)
    print a
    b= base64.b64decode(a)
    print b
    '''
    ''' dict to json
    data = {}
    data['name'] = 'chen'
    data['wife'] = 'gong'
    data['pos'] = {1:154, 2:254, 3:354}
    print data['pos'][1]
    jsonData = json.dumps(data)
    #print 'json data: '+str(jsonData)
    data = json.loads(jsonData)
    print data['pos']
    '''
