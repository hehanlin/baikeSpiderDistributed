# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from HtmlParser import HtmlParser
from HtmlDownloader import HtmlDownloader


class SpiderWork(object):

    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        server_addr = '127.0.0.1'
        print 'connect to server %s...' % server_addr
        self.m = BaseManager(address=(server_addr, 8001), authkey='he')
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print 'init finish'

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()

                    if url == 'end':
                        print '控制节点通知爬虫节点停止工作...'
                        # 接着通知其它节点停止工作
                        self.result.put({'new_urls': 'end', 'data': 'end'})
                        return
                    print '爬虫节点正在解析:%s' % url.encode('utf-8')
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({"new_urls": new_urls, "data": data})
            except EOFError:
                print "连接工作节点失败"
                return
            except Exception as e:
                print e
                print 'Crawl  fali '

if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()