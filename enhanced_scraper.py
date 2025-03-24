from twitter_scraper_selenium import scrape_profile as original_scrape
from driver_utils import Utilities

def enhanced_scrape_profile(
    twitter_username: str,
    output_format: str = "json",
    browser: str = "firefox",
    tweets_count: int = 10,
    filename: str = None,
    directory: str = None,
    headless: bool = True,
    scroll_down_attempts: int = 20,
    wait_between_scrolls: int = 3,
    proxy: str = None
):
    # Initialize driver using original package's logic
    driver = ...  # Copy initialization code from original package
    
    try:
        utils = Utilities()
        utils.close_popups(driver)
        
        if not utils.wait_until_tweets_appear(driver):
            raise Exception("Tweets failed to load")
            
        # Enhanced scrolling
        loaded = utils.smart_scroll(
            driver,
            max_scrolls=scroll_down_attempts,
            min_tweets=tweets_count,
            timeout=wait_between_scrolls*scroll_down_attempts
        )
        
        # Get and process tweets
        tweets = utils.get_visible_tweets(driver)[:tweets_count]
        
        # Use original package's saving logic
        return save_results(tweets, output_format, filename, directory)
        
    finally:
        driver.quit()