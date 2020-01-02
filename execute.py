# coding:utf-8
# __user__ = hiicy redldw
# __time__ = 2019/12/31
# __file__ = execute
# __desc__ =

from scrapy.cmdline import execute
from scrapy.utils.project import get_project_settings
setting = get_project_settings()
execute(['scrapy', 'crawl', 'cdhome','-s',f"JOBDIR=${setting.get('JOB_DIR')}"])  # 持久化调度任务