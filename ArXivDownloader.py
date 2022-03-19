
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from pathlib import Path
import requests
import os


class ArXivDowloader():
    def __init__(self, url, keywords):
        '''INPUT: url: string, to web page, e.g. 'www.google.de'
                  keywords: list of strings, with keywords to be searched in title and abstract.
                  Can also be author name'''
        self.page_text=self.url2text(url)
        self.abstracts=self.getAbstracts(self.page_text)
        self.url=url
        self.keywords=keywords
        self.ids=self.searchforkeys()
    
    def download(self):
        '''downloads all articles that match the keywords to a new Desktop folder'''
        print('check for Desktop folder...')
        Desktop_path = os.path.expanduser("~/Desktop")
        file_path=Desktop_path+'/New_on_arXiv'
        if not os.path.exists(file_path):
            print('creating desktop folder...')
            os.makedirs(file_path)
        print('starting download...')
        total=len(self.ids)
        for index, cid in enumerate(self.ids):
            print('    downloading file '+str(index+1)+'/'+str(total))
            article_url='https://arxiv.org/pdf/' + cid  + '.pdf'    
            self.download_pdf(article_url , file_path +'/arXiv'+cid)
        print('--> done')
   
    def url2text(self,url):
        '''Download all text shown on a web page.
        INPUT: url: string, url to web page, e.g. 'www.google.de'
        OUTPUT: string, containing the text from web page'''
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()
    
    def getAbstracts(self,page_text):
        '''Get all abstracts from full page_text and the corresponding article IDs.
        INPUT: page_text, string text on web page
        OUTPUT: list containing tuples in format (article ID, article_text)'''
        page_text=page_text.split('New submissions for')[1] # only look into text after 'new submissions'
        page_text=page_text.split('Replacements for')[0] # only look into text before 'replacements'
        articles=page_text.split('arXiv:') # seperator: 'arXiv:' by which each new article starts
        return [(article[:10],article[27:]) for article in articles] # create tuples (article ID, article_text)
    
    def searchforkeys(self):
        '''Checks all abstracts, titles, authors if contain one of the keywords
           OUTPUT: lsit of article Ids that contain at least one keyword in abstract, author, title'''
        ids=[]
        for article_id, abstract in self.abstracts:
            for keyword in self.keywords:
                if keyword.lower() in abstract.lower():
                    ids.append(article_id)
                    break
        return ids
    

    def download_pdf(self,url,path):
        '''Dowload pdf file from an url that is directed to apdf file
        INPUT: url: string, containing the url to a pdf file
           filename: string, containing path and filename where pdf is saved, format without
           .pdf file ending'''
        filename = Path(path+'.pdf')
        response = requests.get(url)
        filename.write_bytes(response.content)


