# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyTutorialPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        price_keys = ['price', 'price_inc_tax', 'price_ex_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        availability_string = adapter.get('avability')
        split_availability_string = availability_string.split('(')
        if len(split_availability_string) < 2:
            adapter['avability'] = 0
        else:
            avability_array = split_availability_string[1].split(' ')
            adapter['avability'] = int(avability_array[0])

        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == 'zero':
            adapter['stars'] = 0
        elif stars_text_value == 'one':
            adapter['stars'] = 1
        elif stars_text_value == 'two':
            adapter['stars'] = 2
        elif stars_text_value == 'three':
            adapter['stars'] = 3
        elif stars_text_value == 'four':
            adapter['stars'] = 4
        elif stars_text_value == 'five':
            adapter['stars'] = 5

        return item
    
import mysql.connector
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'ZAQ!2wsx',
            database = 'books'
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS books(
                         id int NOT NULL auto_increment,
                         name text,
                         url VARCHAR(255),
                         product_type VARCHAR(255),
                         price_ex_tax DECIMAL,
                         price_inc_tax DECIMAL,
                         tax DECIMAl,
                         avability INTEGER,
                         num_reviews INTEGER,
                         stars INTEGER,
                         category VARCHAR(255),
                         description text,
                         price DECIMAL,
                         PRIMARY KEY (id)
                         )""")
    
    def process_item(self, item, spider):
        self.cur.execute("""insert into books (
                         name,
                         url,
                         product_type,
                         price_ex_tax,
                         price_inc_tax,
                         tax,
                         avability,
                         num_reviews,
                         stars,
                         category,
                         description,
                         price) VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s);""",
                            (
                                item["name"],
                                item["url"],
                                item["product_type"],
                                item["price_ex_tax"],
                                item["price_inc_tax"],
                                item["tax"],
                                item["avability"],
                                item["num_reviews"],
                                item["stars"],
                                item["category"],
                                str(item["description"][0]),
                                item["price"]

                            )
        )

        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()