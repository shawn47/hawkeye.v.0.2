#coding=utf-8
import logging
import os

format_dict = {
   1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}

class Logger():
    def __init__(self, logname, loglevel, logger):
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)
        
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # 定义handler的输出格式
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
    
    def getlog(self):
        return self.logger

# /Users/xiaoyongbo/Documents/projects/hawkeye.v.0.2
logger = Logger(logname="/Users/xiaoyongbo/Documents/projects/hawkeye.v.0.2/logs/app-log.log", loglevel=1, logger="hawkeye").getlog()
