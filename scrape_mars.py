# Add Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time 
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)
  
def scrape():
    browser = init_browser()
    # Create empty dictionary to insert into mongodb
    mars_data = {}
    # NASA MARS NEWS
    # Create variable to hold url
    nasa_url = "https://mars.nasa.gov/news/"
    # Use splinter to open nasa_url
    browser.visit(nasa_url)
    time.sleep(3)
    # Create HTML object
    nasa_html = browser.html
    # Parse HTML with BeautifulSoup
    nasa_soup = BeautifulSoup(nasa_html, "html.parser")
    # Find News Title
    news_title = nasa_soup.find("div", class_ = "content_title").text.strip()
    #news_title
    # Find Paragraph Text
    news_p = nasa_soup.find("div", class_ = "rollover_description_inner").text.strip()
    #news_p
    # Add news_title and news_p to mars_data dictionary
    mars_data["news_title"] = news_title
    mars_data["news_subtitle"] = news_p

    # JPL MARS SPACE IMAGES - FEATURED IMAGE
    # Create variable to hold url
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Use splinter to open jpl_url
    browser.visit(jpl_url)
    time.sleep(3)
    # Have splinter click full image button
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    # Have splinter click more info button
    browser.click_link_by_partial_text("more info")
    # Create HTML object
    featured_pg = browser.html
    # Create BeautifulSoup object and parse with HTML parser
    jpl_soup = BeautifulSoup(featured_pg, "html.parser")
    # Get featured image url
    featured_img = jpl_soup.find("figure", class_ = "lede")
    featured_img_url =featured_img.a["href"]
    featured_img_url = ("https://www.jpl.nasa.gov" + featured_img_url)
    #featured_img_url
    # Add featured_img_url to mars_data dictionary
    mars_data["featured_img"] = featured_img_url

    # MARS WEATHER
    # Create variable to hold url
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    # Retrieve page with the requests module
    browser.visit(tweet_url)
    time.sleep(3)
    # Create HTML object
    tweet_mars_html = browser.html
    # Create BeautifulSoup object and parse with HTML parser
    tweet_mars_soup = BeautifulSoup(tweet_mars_html, "html.parser")
    time.sleep(3)
    # Retrieve weather tweet
    tweets = tweet_mars_soup.find_all("p")
    for tweet in tweets:
        # if the tweet contains "Sol" we know it is a tweet about weather
        if 'Sol' in tweet.text:
            mars_weather = tweet.text
            break
    #mars_weather
    # Add mars_weather to mars_data dictionary
    mars_data["weather"] = mars_weather

    # MARS FACTS
    # Create variable to hold url
    mars_facts_url = "http://space-facts.com/mars/"
    # Use panda to scrape tabular data
    tables = pd.read_html(mars_facts_url)
    #tables
    # Turn scraped table into dataframe and column headers
    facts_df = tables[0]
    facts_df.columns = ["Description", "Values"]
    facts_df.set_index("Description", inplace = True)
    #facts_df
    # Clean html table
    facts_table = facts_df.to_html()
    mars_facts_table = facts_table.replace("\n", "")
    #mars_facts_table
    # Add mars_facts_table to mars_data dictionary
    mars_data["facts_table"] = mars_facts_table
    # Turn dataframe into html table
    # facts_df.to_html("facts_table.html")

    # MARS HEMISPHERES
    # Create empty dictionaries and list
    hemisphere_img_urls = []
    hemisphere_dicts = {"title": [] , "img_url": []}
    # Create variable to hold url
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Use splinter to open usgs_url
    browser.visit(usgs_url)
    time.sleep(3)
   # Create HTML object
    usgs_html = browser.html
    # Create BeautifulSoup object and parse with HTML parser
    usgs_html_soup = BeautifulSoup(usgs_html, "html.parser")
    results = usgs_html_soup.find_all("h3")
    # Use loop and splinter to open hemisphere links in order to get parse title and image urls
    for result in results:
         # Get text info from result
        title = result.text
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        img_url = browser.find_link_by_partial_href("download")["href"]
        hemisphere_dicts = {"title": title, "img_url": img_url}
        hemisphere_img_urls.append(hemisphere_dicts)
        time.sleep(1)
        browser.visit(usgs_url)
    print(hemisphere_img_urls)
    # Add hemisphere_img_urls to mars_data dictionary
    mars_data['hemisphere_data']= hemisphere_img_urls

    browser.quit()

    return mars_data
