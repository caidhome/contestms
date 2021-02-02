# from pymysql import install_as_MySQLdb
#
# install_as_MySQLdb()

import pymysql

pymysql.version_info = (1, 4, 0, "final", 0)  # 指定pymysql的版本
pymysql.install_as_MySQLdb()

