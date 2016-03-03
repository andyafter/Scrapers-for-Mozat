# -*- coding: utf-8 -*-
__author__ = 'mozat-pc'

from product.utils.config import DEJA_FASHION_MYSQL_CONFIG , BATCH_SIZE
from product.utils.db.simple_db_util import get_db
import copy


class DbHelper():
    CONFIG = copy.deepcopy(DEJA_FASHION_MYSQL_CONFIG)
    FETCH_ROWS_BY_BATCH_SQL = '''
                    SELECT  pid, shop_url
                    FROM deja_fashion.products
                    where merchant = {merchat_id}
                    order by id
                    limit {start_pos}, {batch}'''

    def get_urlPid(self, merchat_id, start_position, batch_size):
        '''
        :param : The start position of query
        :param batch_size: The nmber of rows return 
        :return: dic{pid:*, shop_url:*}
        '''
        conn_mysql = get_db(DbHelper.CONFIG)
        sql = DbHelper.FETCH_ROWS_BY_BATCH_SQL.format(merchat_id=str(merchat_id), start_pos=str(start_position), batch=str(batch_size))
        rows = conn_mysql.fetch_rows(sql)
        return rows



if __name__ == '__main__':
    dbHelper = DbHelper()
    print dbHelper.get_urlPid(10, 0, 2)





