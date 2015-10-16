# Scrapy settings for cnpq project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cnpq'

SPIDER_MODULES = ['cnpq.spiders']
NEWSPIDER_MODULE = 'cnpq.spiders'

ITEM_PIPELINES = {
    'cnpq.pipelines.DuplicatesPipeline': 300
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cnpq (+http://www.yourdomain.com)'
