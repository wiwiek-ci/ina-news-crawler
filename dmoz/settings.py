# Scrapy settings for dmoz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'dmoz'
BOT_VERSION = '1.0'

SPIDER_MANAGER_CLASS = 'dmoz.spidermanager.MySpiderManager'
SPIDER_MODULES = ['dmoz.spiders']
NEWSPIDER_MODULE = 'dmoz.spiders'
DEFAULT_ITEM_CLASS = 'dmoz.items.ArticleItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    'dmoz.pipelines.FilterAndFlagPipeline',
    'dmoz.pipelines.DuplicatePipeline',
    'dmoz.pipelines.NormalizeCategoryPipelines',
    'dmoz.pipelines.MySQLStorePipeline']