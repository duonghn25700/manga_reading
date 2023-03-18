import requests
import json
import mysql.connector

def tuple_2_list(tups):
    for i in range(len(tups)):
        tups[i] = list(tups[i])
        tups[i] = tups[i][0]
    return tups
class beetoon_insert:
    def __init__(self,host='localhost',user='root',password="S@1989", db='crawl_beetoon'):
        self.mydatabase = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        self.mycursor = self.mydatabase.cursor()
        self.insert_query = None
        self.select_query = None
        self.update_query = None
    def insert_2_authors(self,author_id, name, manga_by_author, created_at, updated_at, deleted_at=None, table_name='authors'):
        '''
        `id`         bigint UNSIGNED NOT NULL,
        `author_id`  varchar(255),
        `name`       varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `created_at` int NOT NULL,
        `updated_at` int NOT NULL,
        `deleted_at` int DEFAULT NULL
        Example:
        (1, 'Sengae', 1675607871, 1675607871, NULL),
        (2, 'Fukui Takumi', 1675607874, 1675607874, NULL)
        '''
        self.insert_query = f"""INSERT INTO `{table_name}`(`author_id`, `name`,`manga_by_author`, `created_at`, `updated_at`) VALUES ("{author_id}","{name}","{manga_by_author}","{created_at}","{updated_at}")"""

    def insert_2_categories(self, domain_id,category_id,title,slug,total_manga,description,created_at,updated_at,deleted_at=None,table_name='categories'):
        '''
        `id` bigint UNSIGNED NOT NULL,
        `domain_id` bigint UNSIGNED NOT NULL,
        `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `is_active` tinyint NOT NULL DEFAULT '1',
        `total_manga` int DEFAULT '0',
        `image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `created_at` int NOT NULL,
        `updated_at` int NOT NULL,
        `deleted_at` int DEFAULT NULL

        example:
        (1, 1, 'Genre(s):\n4-Koma\nComedy\nSlice Of Life\nWebtoon\n', 'genres-4-koma-comedy-slice-of-life-webtoon', 1, 0, 
        NULL, NULL, 1675607871, 1675607871, NULL),
        (2, 1, 'Genre(s):\nAction\nShounen\nSupernatural\n', 'genres-action-shounen-supernatural', 1, 0, 
        NULL, NULL, 1675607874, 1675607874, NULL),category_id
        '''

        self.insert_query = f"""INSERT INTO `{table_name}`(`domain_id`,`category_id`,`title`,`slug`,`total_manga`,`description`,`created_at`,`updated_at`) VALUES ("{domain_id}","{category_id}","{title}","{slug}","{total_manga}","{description}","{created_at}","{updated_at}")"""
        # self.mycursor.execute(insert_query)
        # self.mydatabase.commit()
    
    def insert_2_chapters(self,manga_id,manga_name,chapter_id,chapter_name,thumbnail_count,created_at,updated_at,deleted_at=None,table_name='chapters'):

        '''
        `id` bigint UNSIGNED NOT NULL,
        `manga_id` bigint UNSIGNED NOT NULL,
        `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `is_active` tinyint NOT NULL DEFAULT '1',
        `thumbnail_count` int DEFAULT '0',
        `created_at` int NOT NULL,
        `updated_at` int NOT NULL,
        `deleted_at` int DEFAULT NULL

        Example:
        (1, 1, 'At Each Other\'s Throats Ch.176', 1, 1, 1675607871, 1675607871, NULL),
        (2, 1, 'At Each Other\'s Throats Ch.175', 1, 1, 1675607871, 1675607871, NULL),
        '''
        self.insert_query = f"""INSERT INTO `{table_name}`(`manga_id`,`manga_name`,`chapter_id`,`chapter_name`,`thumbnail_count`,`created_at`,`updated_at`) VALUES ("{manga_id}","{manga_name}","{chapter_id}","{chapter_name}","{thumbnail_count}","{created_at}","{updated_at}")"""
        # self.mycursor.execute(insert_query)
        # self.mydatabase.commit()

    def insert_2_chapter_thumbnails(self, manga_id,chapter_id,chapter_name,thumbnail_url,created_at,updated_at,deleted_at=None,table_name='chapter_thumbnails'):
        
        '''
        
        `id` bigint UNSIGNED NOT NULL,
        `chapter_id` bigint UNSIGNED NOT NULL,
        `thumbnail_url` text COLLATE utf8mb4_unicode_ci NOT NULL,
        `is_active` tinyint NOT NULL DEFAULT '1',
        `created_at` int NOT NULL,
        `updated_at` int NOT NULL,
        `deleted_at` int DEFAULT NULL
        
        Example:
        (1, 1, 'https://pic9.yx247.com/comics/pic9/50/45170/881693/335656f07e73e44e19221e6649796c54.jpg', 1, 1675607871, 1675607871, NULL),
        (2, 2, 'https://pic9.yx247.com/comics/pic9/50/45170/881692/e79cbf3b27c582d5f0c51e81a2b82562.jpg', 1, 1675607871, 1675607871, NULL),
        '''
        self.insert_query = f"""INSERT INTO `{table_name}`(`manga_id`,`chapter_id`,`chapter_name`, `thumbnail_url`,`created_at`,`updated_at`) VALUES ("{manga_id}","{chapter_id}","{chapter_name}","{thumbnail_url}","{created_at}","{updated_at}")"""
        # self.mycursor.execute(insert_query)
        # self.mydatabase.commit()

    def insert_2_domain_crawlers(self,domain_name,display_name,description,created_at,updated_at,deleted_at=None,table_name='domain_crawlers'):
        '''
        `id` bigint UNSIGNED NOT NULL,
        `domain_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `display_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `is_active` tinyint NOT NULL DEFAULT '1',
        `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `created_at` int NOT NULL,
        `updated_at` int NOT NULL,
        `deleted_at` int DEFAULT NULL

        Example:
        (1, 'www.ninemanga.com', 'ninemanga.com', 1, 'www.ninemanga.com', 1675607871, 1675607871, NULL)
        '''
        self.insert_query = f"""INSERT INTO `{table_name}`(`domain_name`,`display_name`,`description`,`created_at`,`updated_at`) VALUES ("{domain_name}","{display_name}","{description}","{created_at}", "{updated_at}")"""
        # self.mycursor.execute(insert_query)
        # self.mydatabase.commit()
    
    def insert_2_manga(self,domain_id,manga_id,manga_name,authors,categories,slug,image,chapter_count,rank,view,description,release_at,created_at,updated_at,manga_type="manga",status="pending",deleted_at=None,table_name='manga'):

        '''
        `id` bigint UNSIGNED NOT NULL,
        `domain_id` bigint UNSIGNED NOT NULL,
        `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'manga',
        `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
        `is_active` tinyint NOT NULL DEFAULT '1',
        `image` text COLLATE utf8mb4_unicode_ci,
        `chapter_count` int DEFAULT '0',
        `rank` int DEFAULT '5',
        `description` text COLLATE utf8mb4_unicode_ci,
        `release_at` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `created_at` int NOT NULL,
        `updated_at` int NOT NULL,
        `deleted_at` int DEFAULT NULL
        '''
        self.insert_query = f"""INSERT INTO `{table_name}`(`domain_id`,`manga_id`,`manga_type`,`manga_name`,`authors`,`categories`,`slug`,`status`,`image`,`chapter_count`,`rank`,`view`,`description`,`release_at`,`updated_at`,`created_at`) VALUES ("{domain_id}","{manga_id}","{manga_type}","{manga_name}","{authors}","{categories}","{slug}","{status}","{image}","{chapter_count}" ,"{rank}","{view}","{description}", "{release_at}","{updated_at}", "{created_at}")"""
        # self.mycursor.execute(insert_query)
        # self.mydatabase.commit()

    def update_new_val(self,col_find,old_val,col_update,new_val, table_name):
        self.update_query = f"""UPDATE `{table_name}` SET `{col_update}`='{new_val}' WHERE `{col_find}` = '{old_val}'"""
        self.mycursor.execute(self.update_query)
        self.mydatabase.commit()
    
    def update_categories(self,variable, value,category_id,title,slug,total_manga,description,created_at=1,updated_at=1,deleted_at=1,is_active=1,domain_id=1,table_name="categories"):
        self.update_query = f"""UPDATE `{table_name}` SET `category_id`='{category_id}',`title`='{title}',`slug`='{slug}',`total_manga`='{total_manga}',`description`='{description}',
        `created_at`='{created_at}',`updated_at`='{updated_at}',`deleted_at`='{deleted_at}' WHERE `{variable}` = {value}"""
        self.mycursor.execute(self.update_query)
        self.mydatabase.commit()

    def update_chapters(self,variable, value,manga_id,chapter_id,name,thumbnail_count,created_at=1,updated_at=1,deleted_at=1,is_active=1,table_name="chapters"):
        self.update_query = f"""UPDATE `{table_name}` SET `manga_id`='{manga_id}',`chapter_id`='{chapter_id}',`name`='{name}',`thumbnail_count`='{thumbnail_count}',`created_at`='{created_at}',`updated_at`='{updated_at}',`deleted_at`='{deleted_at}' WHERE `{variable}` = {value}"""
        self.mycursor.execute(self.update_query)
        self.mydatabase.commit()
    
    def update_chapter_thumbnails(self,variable,value,chapter_id,thumbnail_url,is_active=1,created_at=1,updated_at=1,deleted_at=1,table_name="chapter_thumbnails"):
        self.update_query = f"""UPDATE `{table_name}` SET `chapter_id`='{chapter_id}',`thumbnail_url`='{thumbnail_url}',`is_active`='{is_active}',`created_at`='{created_at}',`updated_at`='{updated_at}',`deleted_at`='{deleted_at}' WHERE `{variable}` = {value}"""
        self.mycursor.execute(self.update_query)
        self.mydatabase.commit()
        
    def update_manga(self,variable,value,manga_name,slug,image,chapter_count,rank,view,description,release_at,created_at,updated_at,manga_type="manga",status="pending",is_active=1,deleted_at=1,table_name='manga'):
        self.update_query = f"""UPDATE `{table_name}` SET `manga_name`='{manga_name}',`slug`='{slug}',`image`='{image}',`chapter_count`='{chapter_count}',`rank`='{rank}',`view`='{view}',`description`='{description}',`release_at`='{release_at}',`manga_type`='{manga_type}',`is_active`='{is_active}',`created_at`='{created_at}',`updated_at`='{updated_at}',`deleted_at`='{deleted_at}' WHERE `{variable}` = {value}"""
        self.mycursor.execute(self.update_query)
        self.mydatabase.commit()

    def get_all_rows_in_table(self,column, col_find, val, table_name):
        self.select_query = f"SELECT `{column}` FROM `{table_name}` WHERE `{col_find}`='{val}'"
        self.mycursor.execute(self.select_query)
        tmp = self.mycursor.fetchall()
        return tuple_2_list(tmp)

    def get_value_by_column(self, column, table_name):
        self.select_query = f"SELECT `{column}` FROM `{table_name}`"
        self.mycursor.execute(self.select_query)
        tmp = self.mycursor.fetchall()
        return tuple_2_list(tmp)

    def get_1_value_by_column(self, col_find, val, col_get, table_name):
        self.select_query = f"""SELECT `{col_get}` FROM `{table_name}` WHERE `{col_find}`='{val}'"""
        self.mycursor.execute(self.select_query)
        tmp = self.mycursor.fetchall()
        # return tmp
        return tuple_2_list(tmp)[0]
    
    def data_commit(self):
        self.mycursor.execute(self.insert_query)
        self.mydatabase.commit()