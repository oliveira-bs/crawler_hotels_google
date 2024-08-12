from .items import GoogleHotelPrices, GoogleHotels, GoogleHotelsReviews


def crawl_settings(bot_name: str, today: str, basepath: str):

    rawpath = basepath.split(f"/{bot_name}")[0]
    my_settings = {
        'CONCURRENT_REQUESTS': 4,
        'CONCURRENT_REQUESTS_PER_IP': 2,
        'DOWNLOAD_DELAY': 30.573,
        'FEED_EXPORT_ENCODING': "utf-8",
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'REDIRECT_ENABLED': True,
        'LOG_LEVEL': 'INFO',
        'RETRY_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        'COOKIES_ENABLED': True,
        'BOT_NAME': 'check_%(name)s',
        'SPIDER_MODULES': [f'{bot_name}.spiders'],
        'NEWSPIDER_MODULE': f'{bot_name}.spiders',
        'FEEDS': {f'{rawpath}/{bot_name}/raw/hotels/{today}/\
extraction_{today}_%(batch_id)04d.jsonl': {
            'format': 'jsonlines',
            'encoding': 'utf8',
            'item_classes': [
                GoogleHotels,
                'hotel_reviews_google.spiders.utils.items.GoogleHotels'
            ],
            'overwrite': True,
            'batch_item_count': 2048,
        },
            f'{rawpath}/{bot_name}/raw/reviews/{today}/\
extraction_{today}_%(batch_id)04d.jsonl': {
            'format': 'jsonlines',
            'encoding': 'utf8',
            'item_classes': [
                GoogleHotelsReviews,
                'hotel_reviews_google.spiders.utils.items.GoogleHotelsReviews'
            ],
            'overwrite': True,
            'batch_item_count': 2048,
        },
            f'{rawpath}/{bot_name}/raw/prices/{today}/\
extraction_{today}_%(batch_id)04d.jsonl': {
            'format': 'jsonlines',
            'encoding': 'utf8',
            'item_classes': [
                GoogleHotelPrices,
                'hotel_reviews_google.spiders.utils.items.GoogleHotelPrices'
            ],
            'overwrite': True,
            'batch_item_count': 2048,
        },
        },
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 520, 522, 524, 408, 429, 403],
        'MAX_RETRY_TIMES': 8,
        'RETRY_TIMES': 3,
        # # SCRAPY-PLAYWRIGHT
        # 'PLAYWRIGHT_BROWSER_TYPE': "firefox",
        'PLAYWRIGHT_BROWSER_TYPE': "chromium",
        'DOWNLOAD_TIMEOUT': 30,
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            "headless": True,
            # "headless": False,
            "timeout": 40 * 1000,  # 40 seconds
        },
        'DOWNLOAD_HANDLERS': {
            "http":
            "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",

            "https":
            "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'TWISTED_REACTOR':
        "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

        'PLAYWRIGHT_MAX_PAGES_PER_CONTEXT': 3,
        'PLAYWRIGHT_MAX_CONTEXTS': 3,
        'EXTENSIONS': {
            "scrapy.extensions.memusage.MemoryUsage": 8*1024,
            "scrapy_playwright.memusage.ScrapyPlaywrightMemoryUsageExtension":
            8*1024,
        }
    }

    return my_settings
