# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: db.py
@time: 2018/7/31 上午11:11
@desc:
"""
import pymysql
from app.utils.common import tools


class DB:

    def __init__(self, host, port, user, passwd):

        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = passwd
        self.con = self.connect()

    def connect(self):
        """
        连接数据库
        """
        try:
            con = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                  cursorclass=pymysql.cursors.DictCursor, charset='utf8')
            return con
        except Exception as e:
            tools.log().error(e)

    def db_query(self, sql, fun=None):
        """
        数据库查询sql里边的所有数据
        """
        tools.log().info('开始执行sql:   '  )
        tools.log().info(sql)

        cursors = self.con.cursor()
        try:
            cursors.execute(sql)
            if fun:
                return cursors.fetchone()
            else:
                return cursors.fetchall()
        except Exception as e:
            tools.log().error(e)
            return None

    def db_insert(self, sql):
        """
        sql插入数据库
        """

        tools.log().info('开始执行sql:   ')
        tools.log().info(sql)
        cursors = self.con.cursor()
        try:
            result = cursors.execute(sql)
            # cursors.close()
            self.con.commit()
            # self.con.close()

            return result
        except Exception as e:

            tools.log().error(e)

    def db_close(self):
        """
        关闭连接
        :return:
        """
        try:
            self.con.close()

        except Exception as e:

            tools.log().error(e)


if __name__ == '__main__':
    DB('1', '2', '2', '3').connect()
