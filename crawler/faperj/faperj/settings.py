# Scrapy settings for faperj project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'faperj'

SPIDER_MODULES = ['faperj.spiders']
NEWSPIDER_MODULE = 'faperj.spiders'

ITEM_PIPELINES = {
    'faperj.pipelines.DuplicatesPipeline': 300
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'faperj (+http://www.yourdomain.com)'
