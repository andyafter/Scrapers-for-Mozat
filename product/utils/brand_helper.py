from product.utils.db.simple_db_util import  get_db
from product.utils.config import DEJA_FASHION_MYSQL_CONFIG
from product.utils.text_helper import lower_case_data
from copy import deepcopy
LOAD_BRAND_SQL = '''
        select `id`, `name` from deja_fashion.brand
'''
_merchant_dic = {}
def load_merchant_dictionary():
    global _merchant_dic
    if _merchant_dic:
        return _merchant_dic
    db_conn = get_db(deepcopy(DEJA_FASHION_MYSQL_CONFIG))
    records = db_conn.fetch_rows(LOAD_BRAND_SQL)
    for record in records:
        name  = lower_case_data(str(record['name']))
        _merchant_dic[name] = record['id']
    return _merchant_dic

if __name__ == '__main__':
    print load_merchant_dictionary()