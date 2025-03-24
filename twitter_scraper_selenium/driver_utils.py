#!/usr/bin/env python3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
from random import randint
import logging

logger = logging.getLogger(__name__)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)


class Utilities:
    """
    Enhanced utilities for more reliable Twitter scraping
    """

    @staticmethod
    def wait_until_tweets_appear(driver, timeout=30) -> None:
        """Wait for tweets to appear with longer timeout and multiple selectors"""
        try:
            # Try multiple selectors as Twitter changes them frequently
            selectors = [
                '[data-testid="tweet"]',  # Modern Twitter
                'article[role="article"]',  # Alternative selector
                'div[data-testid="tweetText"]'  # Tweet text container
            ]
            
            for selector in selectors:
                try:
                    WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    return
                except:
                    continue
            
            raise WebDriverException("No tweets found using any selector")
            
        except WebDriverException:
            logger.exception("Tweets did not appear after %s seconds", timeout)

    @staticmethod
    def scroll_down(driver, scroll_pause_time=2, scroll_attempts=10) -> None:
        """Enhanced scrolling that actually reaches the bottom of the page"""
        last_height = driver.execute_script("return document.body.scrollHeight")
        attempts = 0
        
        while attempts < scroll_attempts:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load page
            time.sleep(scroll_pause_time)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same, try the alternate scroll method
                try:
                    body = driver.find_element(By.CSS_SELECTOR, 'body')
                    body.send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)
                except:
                    break
                    
            last_height = new_height
            attempts += 1

    @staticmethod
    def wait_until_completion(driver, max_wait=30) -> None:
        """More robust page load detection"""
        try:
            start_time = time.time()
            while True:
                state = driver.execute_script("return document.readyState")
                if state == "complete":
                    return
                if time.time() - start_time > max_wait:
                    raise TimeoutError("Page didn't load within timeout")
                time.sleep(1)
        except Exception as ex:
            logger.exception('Page load error: %s', ex)

    @staticmethod
    def close_popups(driver):
        """Close any popups that might obstruct scraping"""
        try:
            # Cookie consent popup
            driver.find_element(By.XPATH, 
                '//div[@role="dialog"]//span[contains(text(), "Accept")]').click()
            time.sleep(1)
        except:
            pass

    @staticmethod
    def get_visible_tweets(driver):
        """Returns currently visible tweet elements"""
        selectors = [
            '[data-testid="tweet"]',
            'article[role="article"]'
        ]
        for selector in selectors:
            tweets = driver.find_elements(By.CSS_SELECTOR, selector)
            if tweets:
                return tweets
        return []