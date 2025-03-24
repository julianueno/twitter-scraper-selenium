from twitter_scraper_selenium import scrape_profile

scrape_profile(
    twitter_username="NemoAnno",
    output_format="csv",
    browser="firefox",
    tweets_count=500,
    filename="NemoAnno",
    directory="/Applications/MAMP/htdocs/twitter-scraper-selenium/scraped",
    headless=False)

