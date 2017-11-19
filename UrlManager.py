# -*- coding: utf-8 -*-

import cPickle
import hashlib


class UrlManager(object):

    def __init__(self):
        self.new_urls = self.load_process('new_urls.txt')
        self.old_urls = self.load_process('old_urls.txt')

    def load_process(self, path):
        """
        从本地文件加载进度
        :return: 
        """
        print '[+] 从文件恢复爬取进度: %s' % path
        try:
            with open(path, 'rb') as fp:
                tmp = cPickle.load(fp)
                return tmp
        except:
            print '[!] 无进度文件，创建: %s' % path
        return set()

    def save_process(self, path, data):
        """
        保存爬取进度
        :param path: 
        :param data: 
        :return: 
        """
        with open(path, 'wb') as fp:
            cPickle.dump(data, fp)

    def new_urls_size(self):
        return len(self.new_urls)

    def old_urls_size(self):
        return len(self.old_urls)

    def has_new_url(self):
        """
        判断是否有未爬取的url
        :return: 
        """
        return self.new_urls_size() != 0

    def get_new_url(self):
        """
        获取一个未爬取的url
        :return: 
        """
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url)
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def add_new_url(self, url):
        """
        将新的url添加到未爬取的url集合中
        :param url: 
        :return: 
        """
        if url is None:
            return
        m = hashlib.md5()
        m.update(url)
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
