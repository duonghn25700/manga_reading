from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import mysql.connector
from datetime import datetime
import time
from beetoon.beetoon2sql_v4 import beetoon_insert
import re

mydb = beetoon_insert(host='localhost',user='root',password="", db='crawl_beetoon')

session = requests.Session()
retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


beetoon_crawl = list()

def remove_non_letters(input_string):
    return re.sub(r'[^a-zA-Z\s]+', '', input_string)

def list_2_int(list1):
    list1 = [str(integer) for integer in list1]
    return int("".join(list1))
'''
genre : Chủ đề
start : Trang bắt đầu crawl
end   : Trang kết thúc crawl
'''
def crawl_beetoon_data(genre, start, end):
    cnt = start
    base = 'https://ww5.beetoon.net/'
    display_url = 'ww6.beetoon.net'
    base_url = 'https://ww6.beetoon.net/'
    url = base + genre
    manga_id = 1
    manga_id_list = mydb.get_value_by_column(column='manga_id', table_name='manga')
    if len(manga_id_list)>0:
        manga_id = max(manga_id, max(manga_id_list)) + 1
    else:
        manga_id = 1
    cate_list = []
    author_list = []
    now = datetime.now()
    # current_time = 1
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    # MySQL : INSERT TABLE 'domain_crawlers'
    mydb.insert_2_domain_crawlers(domain_name=base,
    display_name=display_url, description=base_url, 
    created_at=current_time, updated_at=current_time)
    # mydb.data_commit()
    
    # print(mydb.insert_query)

    # XỬ LÝ TỪNG TRANG TRONG MỤC ĐÃ CHỌN (LASTEST-UPDATE)
    while (cnt <= end):
        # LẤY SOURCE CODE CỦA TRANG
        pageUrl = url + '/page-' + str(cnt)
        r = session.get(pageUrl)
        soup = BeautifulSoup(r.content, 'html.parser')
        print("PageUrl: ", pageUrl)
        # TẤT CẢ CÁC BỘ MANGA TRONG PAGE
        comics = soup.find('div', class_="comics-grid")
        '''
        # DUYỆT CÁC BỘ TRUYỆN TRONG URL : https://ww6.beetoon.net/latest-update/
        #
        # CRAWL DATA TỪNG Chapter TRUYỆN --> 
        # manga_id = int, manga_name = str , thumbnail = jpg, author = str,
        # categories = list, last-update = str, chapters = dict
        # 
        '''
        for link in comics.findAll('div', class_="entry"):
            start_time = time.time()
            now = datetime.now()
            last_update = "Update soon"
            chapter_list = []
            chapterid = 1
            chapters = list()
            chapters = list()
            data_crawl = dict()
            
            manga_name = "update soon"
            author = "update soon"
            categories = []
            linkManga_base = link.a['href']
            current_time = now.strftime("%Y/%m/%d %H:%M:%S")
            rManga_base = session.get(linkManga_base)
            soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
            print("\nlink manga: ",linkManga_base)

            # MANGA NAME
            manga_name = soupManga_base.find('h1', class_='name bigger').text

            # THUMBNAIL MANGA
            thumbnail = soupManga_base.find('div', 'thumb text-center').img['src']
            
            # RATING STAR, NUMBER OF RATING, NUMBER OF VIEWS
            rate = int(float(soupManga_base.find('div', class_ = 'rating-container').text.replace('\n',"").replace(" ","")))
            rating_result = soupManga_base.find('div', class_ = 'rating-result').text
            n_of_views = soupManga_base.find('div', class_ = 'view-times').text.replace("\n", "").replace(",","").split(" ")[1]
            n_of_views = int(n_of_views)
            
            # STATUS
            manga_status = soupManga_base.find('div', class_="update").text.split("\n")[2]

            # TOTAL CHAPTERS
            manga_chapter_count = int(soupManga_base.find('div', class_="new-chap").text.split(":")[1])
            
            # AUTHORS MANGA
            author = ""
            author_id = 1
            author_id_list = mydb.get_value_by_column(column='author_id', table_name="authors")
            if len(author_id_list)>0:
                author_id = max(author_id, max(author_id_list)) + 1
            author_list = []
            authors = soupManga_base.find('div', 'author')
            for a in authors.find_all('a', title=True):
                name_author = a['title'] + ","
                author += name_author
                author_list.append(a['title'])
            author = author[:-1]
            # print("\nAuthor list : ",author_list)
            authors_name = mydb.get_value_by_column(column='name', table_name='authors')
            
            # MySQL : INSERT TABLE 'authors'
            for author_name in author.split(","):
                if author_name not in authors_name:
                    mydb.insert_2_authors(author_id=author_id,name=author_name,manga_by_author = "1" ,created_at=current_time, updated_at=current_time, deleted_at=1)
                    author_id +=1
                    mydb.data_commit()

            # MANGA DESCRIPTION
            desc = soupManga_base.find('div', {"id": "desc"}).text
            desc = desc.replace("[", "").replace("]", "").replace('"', "").replace("'","")
            
            # CATEGORIES
            cats = soupManga_base.find('div', class_="genre")
            manga_released_date="updating"
            for category in cats.find_all('a', href=True):
                categories.append(category.text)

            # LAST UPDATE
            try:
                last_update = soupManga_base.find('div', class_='chapter-date')['title']
                last_update = last_update.split(" ")[0]
            except Exception as e:
                print(f"\nNONE CHAPTER FROM : {linkManga_base}")

            category_id = 1
            category_id_list = mydb.get_value_by_column(column='category_id', table_name="categories")
            if len(category_id_list)>0:
                category_id = max(category_id, max(category_id_list)) + 1
            
            # MySQL : INSERT TABLE : 'categories'
            sql_categories_title = mydb.get_value_by_column(column='title', table_name='categories')
            for cate in categories:
                if cate not in sql_categories_title:
                    slug = 'genre/' + cate.lower().replace(" ","-") +'/'
                    mydb.insert_2_categories(domain_id=1,category_id=category_id, title=cate, slug=slug, total_manga=0,
                    description=None, created_at=current_time, updated_at=current_time)
                    category_id+=1
                    mydb.data_commit()

            print("\nmanga_id:", manga_id)
            print("\nmanga_name:", manga_name)
            print("\nthumbnail:", thumbnail)
            print("\nauthor:", author)
            print("\ncategories:",categories)
            print("\nStatus:", manga_status)
            print("\nTotal chapters:", manga_chapter_count)
            print("\nDescription:", desc)
            print("\nlast_update:", last_update)

            # DUYỆT TỪNG PAGE TRUYỆN TRONG 1 MANGA
            last_page = 1
            cnt_page = 1
            try:
                last_page = int(soupManga_base.findAll('a', class_ = 'next page-numbers')[1].get('href').split("/")[4].split("-")[1])
            except Exception as e:
                print("\nTotal_page:", 1)
            else:
                print("\nTotal_page:", last_page)

            # RELEASE DATE
            YOOOO = linkManga_base + '/page-' + str(last_page)
            rYOOOOO = session.get(YOOOO)
            soupYOOOOO = BeautifulSoup(rYOOOOO.content, 'html.parser')
            try:
                manga_released_date = soupYOOOOO.findAll('div', class_ = 'chapter-date')[-1]['title']
                print("\nReleased at:", manga_released_date)
            except:
                print("\nReleased at:", manga_released_date)

            ###########################################################################################
            # MySQL : INSERT TABLE 'manga'
            manga_name_list = mydb.get_value_by_column(column='manga_name', table_name='manga')
            if manga_name not in manga_name_list:
                manga_slug = remove_non_letters(manga_name).lower().replace(" ","-")
                manga_image = thumbnail
                
                mydb.insert_2_manga(domain_id=1,manga_id=manga_id, manga_name=manga_name,authors=author, 
                categories=", ".join(categories),
                slug=manga_slug, image=thumbnail, chapter_count=manga_chapter_count,rank=rate,view=n_of_views,status=manga_status,
                description=desc, release_at=manga_released_date,
                created_at=current_time, updated_at=current_time)
                mydb.data_commit()

            # MySQL : UPDATE TABLE 'authors'.'manga_by_author'
            sql_manga_authors = mydb.get_value_by_column(column='authors', table_name='manga')
            for name in author_list:
                id_list = []
                for sql_author in sql_manga_authors:
                    if name in sql_author:
                        tmp = mydb.get_all_rows_in_table(column="manga_id", col_find="authors", val=sql_author, table_name='manga')
                        for x in tmp:
                            if x not in id_list:
                                id_list.append(x)
                id_list=",".join([str(x) for x in id_list])
                mydb.update_new_val(col_find='name',old_val=name,col_update='manga_by_author',new_val=id_list, table_name='authors')
            
            # MySQL : UPDATE TABLE 'categories'.'total_manga'
            sql_manga_categories = mydb.get_value_by_column(column='categories', table_name='manga')
            for cate in categories:
                id_list = []
                for sql_cate in sql_manga_categories:
                    if cate in sql_cate:
                        sql_manga_id = mydb.get_1_value_by_column(col_find='categories', val=sql_cate, col_get='manga_id', table_name='manga')
                        id_list.append(sql_manga_id)
                id_list = ",".join([str(x) for x in id_list])
                # print(id_list)
                mydb.update_new_val(col_find='title',old_val=cate,col_update='total_manga',new_val=id_list, table_name='categories')
            
            # LẤY URL TỪNG CHAPTER
            while last_page>=cnt_page:
                # LẤY LINK MANGA
                linkManga = linkManga_base + '/page-' + str(last_page)
                print("\npage {}:".format(last_page), linkManga)

                # LẤY DATA TỪ MANGA
                rManga = session.get(linkManga)
                soupManga = BeautifulSoup(rManga.content, 'html.parser')
                last_page -= 1

                # LẤY TÊN CÁC CHAPTER TRONG PAGE
                for chaptername in soupManga.findAll('h2', class_="chap")[::-1]:
                    chaptername = chaptername.text.replace("  ", "-").lower()
                    chapter_list.append((chaptername[:-1].replace(".","-"), chapterid))
                    chapterid += 1
                # print(chapter_list)

            if len(chapter_list) > 0:
                for i in range(len(chapter_list)):
                    # chapter_id, chapter_name, page_list
                    chapter_id = chapter_list[i][1]
                    chaptername = None
                    chapter_name = None
                    chapter = dict()
                    page_list = []

                    # LẤY DATA TỪNG CHAPTER
                    linkChapter = linkManga_base + '-' + chapter_list[i][0] + '/'
                    # print("Link chapter : \n\n", linkChapter)
                    rChapter = session.get(linkChapter)
                    soupChapter = BeautifulSoup(rChapter.content, 'html.parser')

                    # TÊN CHAPTER
                    try:
                        chapter_name = soupChapter.find('a', class_ = 'bg-tt').text
                        chaptername = chapter_name + ' - BeeToon.net'
                        print("\nChapter Name: ", chaptername)
                    except Exception as e:
                        print("\nNo Chapter Name")

                    # CRAWL ẢNH TỪNG CHAPTER
                    for img in soupChapter.findAll('img', attrs={'alt': chaptername}):
                        src = img['src'].replace('\n', '')
                        page_list.append(src)
                    
                    # print(page_list)
                    # THÊM KEY Chapters vào DATA CHÍNH
                    chapter['chapter_id'] = chapter_id
                    chapter['chapter_name'] = chapter_name
                    chapter['page_list'] = page_list
                    chapters.append(chapter)
                    # print("\nchapters: ", chapters)

                    # MySQL : INSERT TABLE 'chapters'
                    chapters_name = mydb.get_value_by_column(column="chapter_name", table_name="chapters") # Tất cả các tên chapter trong table 'chapters'
                    # Kiểm tra nếu chưa add chapter thì add vào 'chapters'
                    if chapter_name not in chapters_name:
                        mydb.insert_2_chapters(manga_id=manga_id,manga_name=manga_name,chapter_id=chapter_id,chapter_name=chapter_name,
                        thumbnail_count=len(chapter['page_list']),
                        created_at=current_time, updated_at=current_time)
                        mydb.data_commit()

                    # MySQL : INSERT TABLE 'chapter_thumbnails'
                    thumb_manga_id= mydb.get_1_value_by_column(col_get='manga_id',col_find='manga_name',val=manga_name, table_name="manga")
                    # print("\nFROM manga_id:",thumb_manga_id)
                    if chapter_name not in mydb.get_value_by_column(column="chapter_name", table_name="chapter_thumbnails"):
                        for chapter_thumbnail_url in chapter['page_list']:
                            mydb.insert_2_chapter_thumbnails(manga_id=thumb_manga_id,
                            chapter_id=chapter['chapter_id'],chapter_name=chapter_name,
                            thumbnail_url=chapter_thumbnail_url,
                            created_at= current_time, updated_at=current_time)  
                            mydb.data_commit()

                # print("\nchapters:", chapters)
            data_crawl['manga_id'] = manga_id
            data_crawl['manga_name'] = manga_name
            data_crawl['thumbnail'] = thumbnail
            data_crawl['author'] = author
            data_crawl['last-update'] = last_update
            data_crawl['categories'] = categories
            data_crawl['chapters'] = chapters
            end_time = time.time()
            print("\nTotal time : {}".format(int(end_time - start_time)))
            
            # # MySQL : UPDATE TABLE 'manga'
            mydb.update_new_val(col_find="manga_name",old_val=manga_name,col_update="chapter_count",new_val=int(len(data_crawl['chapters'])), table_name='manga')
            
            # update
            manga_id+=1
            beetoon_crawl.append(data_crawl)
            print("---"*20)
        cnt+=1

crawl_beetoon_data('latest-update', 1, 600)

# with open('data1.json', 'w', encoding="utf-8") as f:
#     json.dump(beetoon_crawl, f, indent=4)