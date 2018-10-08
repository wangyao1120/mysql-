import re
import hashlib

import pymysql

from MyModel import Model

class User(Model):
    def __init__(self,host,user,password,db,charset,port=3306):
        super().__init__(host,user,password,db,charset,port)
        self.table_name = 'user'
        self.cacheField()
        if self.cache:
            fields = ','.join(self.cache.values())
            self.options['field'] = fields

    def myMd5(self,str):
        """
        获取字符串的md5值
        :param str:
        :return: 字符串的md5值
        """
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()

    def login(self,username,password):
        """
        登陆
        :param username: 用户名
        :param password: 密码
        :return:
        """
        password = self.myMd5(password)  #获取password的md5
        result = self.table('user').field('uid,uname,password').where("uname='{}'".format(username)).select()
        # print(result)
        if not result:
            return "用户名错误"
        if password == result[0]['password']:
            return True
        else:
            return "密码错误，请重新输入"
        # return 'ok'


    def register(self,userinfo):
        """
        用户注册
        :param userinfo:用户信息，字典
        :return: 成功返回True，失败返回False
        """
        if self.checkUsername(userinfo['uname']) == -1:
            return "用户名不能少于6位"
        if self.checkUsername(userinfo['uname']) == -2:
            return "用户名重复"
        if self.checkPassword(userinfo['password']) == -1:
            return "密码不能纯数字"
        if self.checkPassword(userinfo['password']) == -2:
            return "密码不能少于6位"
        if not self.checkEmail(userinfo['email']):
            return "不是emai"
        #把密码做一次md5
        md5 = hashlib.md5()
        md5.update(userinfo['password'].encode('utf-8'))
        userinfo['password'] = md5.hexdigest()

        self.table('user').insert(userinfo)


    def checkUsername(self,username):
        username = username.strip()
        #用户名不能少于6位
        if len(username) <= 6:
            return -1

        #用户名不能重复
        result = self.table('user').where("uname='%s'"%username).select()
        if not result:
            return  1  #数据库中没有该用户名，可以使用
        else:
            return -2  #用户名重复

    def checkPassword(self,pwd):
        #密码验证失败
        #如果是纯数字，则验证失败
        if  re.match(r'\d+$',pwd):
            return -1
        #如果少于6位，验证失败
        if len(pwd) < 6:
            return -2
        return 1

    def checkEmail(self,email):
        if not re.match(r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$', email):
            return False
        return True


if __name__ == '__main__':
    user = User('localhost','root','123','test','utf8')
    # # user.checkUsername('tom1111')
    # uname = input("请输入用户名：")
    # password = input("请输入密码：")
    # email = input("请输入email:")
    # user.register({'uname':uname,'password':password,'email':email})


    #用户登陆
    uname = input("请输入用户名：")
    password = input("请输入密码：")
    print(user.login(uname,password))
