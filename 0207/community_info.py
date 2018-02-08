# encoding:utf-8
import   MySQLdb, time, urllib2, json

def __init__(self, location, city, into_db):  
    self.location = location  
    self.city = city  
    self.ziduan = ['name', 'address', 'city', 'district', 'scope', 'crawler_time', 'location']  
    self.seq = ['"''"', '"', '"''"', '"', '"''"', '', '"']  
    self.into_db = into_db  

def spider(self):  
  
    dif = [self.location[0] - self.location[2], self.location[3] - self.location[1]]  # 经纬度范围  
    b = [x / 100.0 + self.location[2] for x in xrange(int(dif[0] * 50))]  
    c = [x / 100.0 + self.location[1] for x in xrange(int(dif[1] * 50))]  
  
    d = [[x, y] for x in b for y in c]                                                # 构建小矩形框  
  
    cnxn = MySQLdb.connect(host=self.into_db[0], user=self.into_db[1],  
                           passwd=self.into_db[2], charset=self.into_db[3])           # 连接到MySQL  
  
    cursor = cnxn.cursor()                                                            # 定义一个MySQL游标  
    sql = "select name from house.community_info where  city = '{}' ".format(self.city)  
    cursor.execute(sql)                                                               # 执行SQL语句  
  
    url_database = [item[0] for item in cursor.fetchall()]         # 取出当前城市已有小区的名字  
  
    cnxn.commit()                                                  # 提交事务！不然python无法执行sql操作  
    dict_data_list = []                                            # 字典列表  
    i = 0  
  
    for x in d:                                                    # 遍历当前城市所有划分出来的小矩形  
  
        html = urllib2.urlopen(  
            r'http://api.map.baidu.com/place/v2/search?query=小区&bounds={},{},{},{}4&page_size=20&output=json&ak=byEXq8wAVGXWKqOI4sA99ErDAtqlP6Fk'  
                .format(x[0], x[1], x[0] + 0.01, x[1] + 0.01))  
        b = html.read()  
  
        c = json.loads(b)    # json  
        #print 'josn->>', c, '<<--'  
  
        if not c['results']:  
            continue  
        for x in c['results']:  
            dict_data = {}  
            dict_data['city'] = self.city  
            dict_data['name'] = x['name'].encode('utf-8', 'ignore')  
            dict_data['address'] = x['address'].encode('utf-8', 'ignore')  
  
            try:  
                lng_lat = str(x['location']['lng']) + ',' + str(x['location']['lat'])  
            except KeyError:  
                lng_lat = '0.0,0.0'  
  
            dict_data['location'] = lng_lat  
            lng_lat = ','.join(lng_lat.split(',')[::-1])  
            html = urllib2.urlopen(  
                r'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location={}&output=json&pois=1&ak=你的AK码'.format(  
                    lng_lat))  
            b = html.read()  
            b = b.split('renderReverse&&renderReverse(')[1][:-1]  
            c = json.loads(b)  # json  
            dict_data['scope'] = c['result']['business'].split(',')[0].encode('utf-8', 'ignore')  
            dict_data['crawler_time'] = str(int(time.time())).encode('utf-8', 'ignore')  
  
            if not dict_data['scope']:  
                dict_data['scope'] = '其他'  
            dict_data['district'] = c['result']['addressComponent']['district'].encode('utf-8', 'ignore')  
  
            if not dict_data['district']:  
                dict_data['district'] = '其他'  
            dict_data_list.append(dict_data)  
  
  
    cnxn = MySQLdb.connect(host=self.into_db[0], user=self.into_db[1], passwd=self.into_db[2],  
                           charset=self.into_db[3])  
    cursor = cnxn.cursor()  
  
    #print len(dict_data_list)  
  
    for x in dict_data_list :                                    # 遍历  
        if not x['name'].decode('utf-8') in url_database:        # 判断小区是否已经存在  
            # 插入数据  
            sql = "insert into test.community_info ({}) values ({})".format(  
                ",".join([item for item in self.ziduan]),  
                ",".join([j + x[i] + j for j, i in zip(self.seq, self.ziduan)]))  
              
            cursor.execute(sql)  
    cnxn.commit()                                                # 同理，提交事务  
    cnxn.close()                                                 # 断开连接  

# 主程序入口  
if __name__ == '__main__':  
    a = [('西安', [34.4438130000, 108.8006150000, 34.1830240000, 109.1546790000])]  # 设定西安市区经纬度范围  
  
    into_db=("172.23.15.19","o8Jy4QqqHk4WytL","","utf8")  
  
    for x, y in a:  
       example1 = community_info(y, x, into_db)  
    