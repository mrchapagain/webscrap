# Scrapy settings for webscrap project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html



BOT_NAME = 'webscrap'

SPIDER_MODULES = 'webscrap.spiders'#['webscrap.spiders']
NEWSPIDER_MODULE = 'webscrap.spiders'

#FEED_EXPORT_FIELDS= ["image_urls"]

#Export as JSON Feed
FEED_FORMAT = "json"
# Name of the file where data extracted is stored
FEED_URI = "data.json"



FEEDS = {
    'data.json': {
        'format': 'json', 
        'overwrite': False,
        'indent': 4,
        'store_empty': True,
        'fields': None,
        'encoding': 'utf-8'},

    'log.jsonlines': {
        'format': 'jsonlines', 
        'overwrite': True,
        'encoding': 'utf-8'}
}

FEED_EXPORT_ENCODING = 'utf-8'



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webscrap (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'webscrap.middlewares.WebscrapSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'webscrap.middlewares.WebscrapDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'webscrap.pipelines.WebscrapPipeline': 800,
    #"webscrap.pipelines.CustomImagesPipeline": 1,
    #'webscrap.pipelines.FilesPipeline': 1,
}
ITEM_STORE = 'data'
#IMAGE_STORE = 'images'
#<IMAGES_STORE>/full/<image_id>.jpg

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'




"""IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (260, 260),
}


IMAGES_EXPIRES = 2  # 2 days of delay for image expiration (default:90 days)"""

