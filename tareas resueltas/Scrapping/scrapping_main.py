from turtle import title
from lxml.html import parse
from lxml.html import tostring
import urllib.request
import numpy as np
import sqlite3
from sqlite3 import Error

#cambio de user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

#descarga y parseo de la pagina.
url_str = 'https://www.readwn.com'

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_NOVEL(conn, project):
    sql = ''' INSERT INTO novels(url,title,author,genres,synopsis,chapters)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

database = r"novelas.db"
conn = create_connection(database)

for i in range(17):
    response = urllib.request.urlopen(url_str + '/list/all/all-onclick-' + str(i) + '.html')
    doc = parse(response)
    cur = conn.cursor()
    cur.execute("SELECT url FROM novels")
    urls_processed = [x[0] for x in cur.fetchall()]
    for novel in doc.xpath("//*[@class='novel-item']/a"):
        if (i == 16 and doc.xpath("//*[@class='novel-item']/a").index(novel) == 10):
            break
        info = []
        ## URL
        novel_url = url_str + novel.attrib['href']
        if novel_url in urls_processed:
            continue
        info.append(novel_url)
        ## TITLE
        info.append(novel.attrib['title'])
        ## AUTHOR
        novel_page = urllib.request.urlopen(novel_url)
        novel_doc = parse(novel_page)
        info.append(novel_doc.xpath("//*[@itemprop='author']")[0].text)
        ## GENRES
        genres = []
        for genre in novel_doc.xpath("//*[@title='Sci-fi Category']"):
            genres.append(genre.text)
        if None in genres:
            info.append("")
        else:
            info.append('|'.join(genres))
        ## SYNOPSIS
        synopsis = []
        for summary_line in novel_doc.xpath("//*[@class='summary']/*[@class='content']/p"):
            if summary_line.text != None:
                synopsis.append(summary_line.text)
        info.append('\n'.join(synopsis))
        chapter_text = []
        ## TEXT
        for chapter in novel_doc.xpath("//*[@class='chapter-list']/li/a")[0:10]:
            chapter_page = urllib.request.urlopen(url_str + chapter.attrib['href'])
            chapter_doc = parse(chapter_page)
            chapter_lines = []
            for line in chapter_doc.xpath("//*[@class='chapter-content']/p"):
                if line.text != None:
                    chapter_lines.append(line.text)
            chapter_text.append("\n".join(chapter_lines))
        info.append('\n'.join(chapter_text))
        create_NOVEL(conn, tuple(info))
