import pymysql


# mysql操作类
class MySqlCtl:
    def __init__(self, host, username, password, database, port=3306, charset='utf8'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.charset = charset

    # 连接mysql方法
    def _connect(self):
        return pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.username,
                               passwd=self.password,
                               db=self.database,
                               charset=self.charset)

    # 插入方法
    def insert(self, sql):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        affected_rows = conn.affected_rows()
        cursor.close()
        conn.close()
        return affected_rows

    # 插入二进制数据
    def insert_binary(self, sql, params):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        affected_rows = conn.affected_rows()
        cursor.close()
        conn.close()
        return affected_rows

    # 修改方法
    def update(self, sql):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        affected_rows = conn.affected_rows()
        cursor.close()
        conn.close()
        return affected_rows

    # 删除方法
    def delete(self, sql):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        affected_rows = conn.affected_rows()
        cursor.close()
        conn.close()
        return affected_rows

    # 查询所有数据，结果以元祖方式返回
    def query_all(self, sql):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    # 查询所有数据，结果以字典方式返回
    def query_all_dict(self, sql):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    # 查询单条数据，结果以元祖方式返回
    def query_one(self, sql):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    # 查询单条数据，结果以字典方式返回
    def query_one_dict(self, sql):
        # 对sql语句进行转义, 防止sql注入
        sql = pymysql.escape_string(sql)

        conn = self._connect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    # 二进制数据
    def binary(self, data):
        return pymysql.Binary(data)
