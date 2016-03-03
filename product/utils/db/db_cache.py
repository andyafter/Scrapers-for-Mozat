from product.utils.db.simple_db_util import get_db

def escape_quotes(my_str):
    return my_str.replace('"', '\\"')

class DB_Cache(object):
    '''
    must call the flush manually.
    '''    
    def __init__(self, cache_size, conn_config, table_name, columns=[], verbose=False):
        assert(type(cache_size) == int)
        self.enable = False
        self.cache = []
        self.cache_size = cache_size
        self.conn_config = conn_config
        self.conn = get_db(self.conn_config)

        self.table_name = table_name
        self.columns = columns

        self.verbose = verbose
        
    def enable_cache(self):
        self.enable = True
        self.flush()
    
    def disable_cache(self):
        self.enable = False
        self.flush()

    def add(self, row):
        for column in self.columns:
            assert(column in row)
        self.cache.append(row)
        if self.enable == False or len(self.cache) >= self.cache_size:
            self.flush()
            
    def flush(self):
        'insert all rows in self.cache into db' 
        raise NotImplementedError()


class InsertProductTagSource(DB_Cache):
    def __init__(self, cache_size, conn_config, verbose=False):
        DB_Cache.__init__(self, cache_size, conn_config, 'deja_fashion.product_tag_source', ['product_id', 'tag_source'], verbose)

    def flush(self):
        if self.cache:
            insert_sql = '''
            insert into  deja_fashion.product_tag_source(`product_id`, `tag_source`) values
            '''
            values = []
            try:
                for row in self.cache:
                    values.append('(\''+ str(row['product_id']) + '\',\'' + str(row['tag_source']).replace('\\"', '\\\\"')+'\')')
                sql = insert_sql + ',\n'.join(values)
                if self.verbose:
                    print sql
                self.conn.execute(sql)

            except Exception as e:
                print e
            self.cache = []


class InsertProduct(DB_Cache):
    def __init__(self, cache_size, conn_config, verbose=False):
        DB_Cache.__init__(self, cache_size, conn_config, 'algorithm.product', ['pid', 'tag_source', 'update_time', 'merchant', 'suitable_images', 'white_suitable', 'detail_images', 'shop_url', 'merchant_en', 'brand_en', 'price', 'discount_price',
                                                                               'discount_percent'], verbose)

    def flush(self):
        if self.cache:
            INSERT_SQL = '''
                insert into algorithm.product(`pid`, `tag_source`, `update_time`, `brand`, `merchant`, `suitable_images`, `white_suitable`
                `detail_images`, `shop_url`, `brand_en`, `merchant_en`, `price`, `discount_price`, `discount_percent`) values
            '''
            values = []
            try:
                for row in self.cache:
                    values.append('(\'' + str(row['pid']) + '\',\'' + str(row['tag_source']) + '\',\'' + str(row['update_time']) + '\',' + str(row['merchant']) + ',\'' + str(row['suitable_images']) +
                                  '\',\'' + str(row['detail_images']) + '\',\'' + str(row['shop_url']) + '\', \'' + str(row['merchant_en']) + '\', \'' +
                                  str(row['brand_en']) +  '\',' + str(row['price']) + ',' + str(row['discount_price']) + ',' + str(row['discount_percent']) + ')')
                sql = INSERT_SQL + ',\n'.join(values)
                if self.verbose:
                    print sql
                self.conn.execute(sql)
            except Exception as e:
                print e
            self.cache = []