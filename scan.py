import requests
import random
#查询ip归属地函数
def iploc(ip):
    ipsearch = 'http://ip-api.com/json/' + ip + '?lang=zh-CN'
    getipcountry = requests.get(url = ipsearch).json()['country']
    getcity = requests.get(url = ipsearch).json()['city']
    ipinfo = getipcountry + getcity
    return ipinfo

#设置用户代理
user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
headers = {'User-Agent': random.choice(user_agents)}
#设置节点API命令（形如 XXX.XXX.XXX.XXX:5001 ）
ipfsapi = 'XXX.XXX.XXX.XXX:5001'
searchcom = 'http://'+ ipfsapi + '/api/v0/swarm/peers?'
#请求节点API
print('开始扫描')
req = requests.post(url=searchcom).text
#处理返回对等连接的节点信息
req = req.split('},{')
#过滤出默认4001端口的节点
for i in req:
    if '4001' in i:
        req = i.split('","')
        for h in req:
            if '4001' in h:
                ip = h
                #过滤出ipv4的节点信息
                if 'ip4' in ip:
                    ip = ip.split('/ip4/')[-1]
                    ip = ip.split('/')[0]
                else:
                    pass
                #测试webui是否正常访问
                webuiurl = 'http://' + ip + ':5001/webui'
                try:
                    #设置请求1秒超时
                    response = requests.get(webuiurl,headers = headers, timeout = 1)
                    response.enconding = "utf-8"
                    #返回测试成功的结果
                    if str(response) == '<Response [200]>':

                        print(ip + ':5001/webui' + iploc(ip))
                except:
                    pass
                continue
print('结束扫描')
