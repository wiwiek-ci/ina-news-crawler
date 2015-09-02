You can create custom crawler by extending NewsBaseCrawler class and place the custom crawler class file in base\_directory/dmoz/spiders directory.

## NewsBaseCrawler ##

Extract these value from an article:
  * Title (sanitized)
  * Category (normalized)
  * Content (sanitized)
  * Subtitle (capitalized first char in each word)
  * Published at (format: "%Y-%m-%d %H:%M")
  * Place
  * Subtitle
  * Author

## CustomCrawler ##

To create custom fetcher, you have to extend NewsBaseCrawler class. The attributes you have to override:
  * name = the name of the custom  "_`sitename`_"
  * source = domain of target sites. This will constrain the allowed domain.
  * debug = whether you just only want to print the result (True) or save to database (False). The default value is False.
  * start\_urls = URLs that contain seed URLs for further crawling (fetching content)
  * rules = rule in regex to determine which links should be followed
  * xpath\_title = XPath string of the title of the article
  * xpath\_category = XPath string of the category of the article
  * xpath\_content = XPath string of the content of the article
  * xpath\_subtitle = XPath string of the subtitle of the article
  * xpath\_published\_at = XPath string of the published date of the article
  * xpath\_place = XPath string of the place of the article
  * xpath\_author = XPath string of the author of the article

The function that can be overriden:
  * parse\_date: function to parse date so it become format "%Y-%m-%d %H:%M"
  * parse\_place: function to parse place text
  * parse\_author: function to parse author text
  * get\_category: function to get raw category text
  * normalize\_category: function to make normalize category value. Assign each category by one of these variables: CATEGORY\_NATIONAL, CATEGORY\_INTERNATIONAL, CATEGORY\_ECONOMY, CATEGORY\_SPORTS, CATEGORY\_FOOTBALL, CATEGORY\_SCITECH, CATEGORY\_HUMANIORA, CATEGORY\_ENTERTAINMENT, and CATEGORY\_OTHERS.
  * parse\_category: function to parse category text