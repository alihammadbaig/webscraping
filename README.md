This repo contains two Scrapy Spiders used to scrap joboutlook website for jobs related information.

Web scraping, web harvesting, or web data extraction is data scraping used for extracting data from websites. I am using Scrapy for this purpose. Scrapy is an open source and collaborative framework for extracting the data you need from websites.

If you are thinking of Scraping a website, this page will help you understand the how Scrapy works from a beginner to an advance level. You won't need any other source after this - promise 

Here is what we will learn

* Installing Anaconda on your local machine - Its not mandatory, but if you're afraid of configuring environment variable, then this is highly recommended. 
* Installing Scrappy
* Creating a scrappy project
* Running a scrappy project - in scrappy specific terminology we will learn how to crawl the website with Spider 
* Store the output in files (I will store it in JSON file, we can easily use the same method to store output in XML, CSV and a few other formats)
* We will scrape this website https://joboutlook.gov.au/Industry.aspx. We will not only read information from this page, but hit subsequent links on this page and read information from the other pages in the same program as well.
# Step-by-step guide
First thing first - **Download Anaconda** for windows with Python 3.* version from here https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe
**Install Anaconda**  - Just double click the .exe and follow the steps, its very simple standard installation. This guide might also be helpful https://medium.com/@GalarnykMichael/install-python-on-windows-anaconda-c63c7c3d1444. Anaconda provides Python and R along with several libraries, RStudio, Spyder IDE, Jupyter notebook and several other tools out of box.

**Install Scrapy**  - Open Anaconda prompt by going to Windows start button > All Programs > Anaconda > Anaconda Prompt and run the following command 

conda install -c conda-forge scrapy
Detailed documentation over here. 

**Scrapy Shell** - Scrappy comes with an interactive shell where you can try and debug code. Run Anaconda Prompt, type scarpy and press enter. Then type the following command 

**scrapy shell** https://scrapy.org
I would highly recommend to get used to shell before going any further. This one page document will be enough to know the workings of Scrapy shell https://doc.scrapy.org/en/latest/topics/shell.html

**Build a new project** - On the Anaconda prompt run the following command

scrapy startproject myproject

This will create a "myproject" directory with the following content

tutorial/
    scrapy.cfg            # deploy configuration file

    myproject/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py


Before going any further, I recommend to at least read the section Our first Spider of this tutorial 
Lets create a "Spider" that "Crawls" the web.
Spiders are classes that you define and that Scrapy uses to scrape information from a website (or a group of websites). They must subclass scrapy.Spider and define the initial requests to make, optionally how to follow links in the pages, and how to parse the downloaded page content to extract data.

**Summary of what the code does**
The spider lands on https://joboutlook.gov.au/Industry.aspx (start_urls object in code). This is the first request made by the Spider. Spider method parse is called automatically by Scrapy which is in charge of processing the response and returning scraped data and/or more URLs to follow. In the following code parse method reads href attribute of HTML anchor tags that are inside and h2 heading (see the image below). Each HTML element can be accessed with two functions of response object, css or xpath, I prefer css.

*You can see code behind the web page by right clicking the page and selecting Inspect in Chrome.*

![alt text](https://github.com/alihammadbaig/webscraping/blob/master/image.png)

The Code
Below is the code for our first Spider. Save it in a file named JobInfo.py under the myproject/spiders directory in your project.

The parse method loops over each heading(see image 1 above), gets the URL and creates a new request to that page. A separate method parse_industry_profiles parses the response returned from this new request. Similarly, this parse functions also loops over each section on this page(see image 2 above), gets the URL and makes a request to that page. The response of this call is handle by another parse function parse_profile_details, which returns the information mentioned in image 3 above.

```python
import scrapy


class JobinfoSpider(scrapy.Spider):

    name = 'jobdetails'
    allowed_domains = ['joboutlook.gov.au']
    start_urls = ['https://joboutlook.gov.au/Industry.aspx']

    def parse(self, response):

        industry_details_page_urls = \
            response.css('article > div.career-title > h2 > a::attr(href)'
                         ).extract()

        for url in industry_details_page_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_industry_profiles)

    def parse_industry_profiles(self, response):
        profile_details_page_urls = \
            response.css('article > div.career-title > h3 > a::attr(href)'
                         ).extract()

        # Job profile details page

        for url in profile_details_page_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_profile_details)

    def parse_profile_details(self, response):
        fast_facts = \
            response.css('ul.snapshot > li > span.snapshot-data::text')

        yield {
            'industry': response.css('div.breadcrumb-col > ul > li:nth-of-type(3) > a::text').extract_first().strip(),
            'job_profile': response.css('div.page-title-col > h1::text').extract_first().strip(),
            'anzsco_code': response.css('div.anzsco > abbr::text').extract_first().replace('ANZSCO ID ', '').strip(),
            'avg_weekly_pay': fast_facts[0].extract().strip(),
            'future_growth': fast_facts[1].extract().strip(),
            'skill_level': fast_facts[2].extract().strip(),
            'employment_size': fast_facts[3].extract().strip(),
            'unemployment': fast_facts[4].extract().strip(),
            'male_share': fast_facts[5].extract().strip(),
            'female_share': fast_facts[6].extract().strip(),
            'full_time': fast_facts[7].extract().strip(),
        }
```

The following command executes the project and stores the returned data in JSON format in a single file
```python
scrapy crawl jobdetails -o jobdetails.json
```

**More Generic Approach**
The code below does the exact same thing as the previously explained code does, the only difference is we are using Items class to store the information. This is a more generic and preferable approach. Read more about Items class here. 

Lets create an Items class in existing project file items.py

```python
import scrapy
from scrapy.item import Item, Field

class JoboutlookItem(scrapy.Item):
    main_page_url = Field()
    profile_page_url = Field()
    profile_detail_page_url = Field()
    industry = Field()
    job_profile = Field()
    anzsco_code = Field()
    avg_weekly_pay = Field()
    future_growth = Field()
    skill_level = Field()
    employment_size = Field()
    unemployment = Field()
    male_share = Field()
    female_share = Field()
    full_time = Field()
```
Lets create a Spider that uses the JoboutlookItem class to store and transfer data.

```python
import scrapy
from joboutlook.items import JoboutlookItem

class JobinfoSpider(scrapy.Spider):
    name = 'jobinfo'
    allowed_domains = ['joboutlook.gov.au']
    start_urls = ['https://joboutlook.gov.au/Industry.aspx']

    def parse(self, response):
        urls = response.css(
            'article > div.career-title > h2 > a::attr(href)').extract()
        item = JoboutlookItem()
        item['main_page_url'] = response.url

        for url in urls:
            url = response.urljoin(url)
            request = scrapy.Request(url=url,
                                     callback=self.parse_industry_profiles)
            request.meta['item'] = item
            yield request

    def parse_industry_profiles(self, response):
        self.log('__fun parse_industry_profiles__')
        item = response.meta['item']
        item['profile_page_url'] = response.url

        profile_details_page_urls = response.css(
            'article > div.career-title > h3 > a::attr(href)').extract()

        for url in profile_details_page_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_profile_details, meta={'item': item})

    def parse_profile_details(self, response):
        item = response.meta['item']
        item['profile_detail_page_url'] = response.url

        fast_facts = response.css(
            'ul.snapshot > li > span.snapshot-data::text')

        item['industry'] = response.css(
            'div.breadcrumb-col > ul > li:nth-of-type(3) > a::text').extract_first().strip(),
        item['anzsco_code'] = response.css(
            'div.anzsco > abbr::text').extract_first().replace('ANZSCO ID ', '').strip()
        item['job_profile'] = response.css(
            'div.page-title-col > h1::text').extract_first().strip()
        item['avg_weekly_pay'] = fast_facts[0].extract().strip()
        item['future_growth'] = fast_facts[1].extract().strip()
        item['skill_level'] = fast_facts[2].extract().strip()
        item['employment_size'] = fast_facts[3].extract().strip()
        item['unemployment'] = fast_facts[4].extract().strip()
        item['male_share'] = fast_facts[5].extract().strip()
        item['female_share'] = fast_facts[6].extract().strip()
        item['full_time'] = fast_facts[7].extract().strip()

        yield item
```

Execute the project

```python
scrapy crawl jobinfo -o jobinfo.json
```

