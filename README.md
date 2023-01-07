Dependencies:
The crawler needs to run with Python 3.6 and later.
You need to install all the dependencies, such as bs4/beautifulsoup4, which is used for HTTP parsing.
requests_mock is used to mock the HTTP requests in unittest. 
Coverage is used for unit testing and to get the test coverage.

To install all the dependencies, you can run:
pip install -r requirements.txt

To crawl any website, you can run:
python main.py url

To run the tests and coverage:
python -m unittest discover
coverage run -m unittest discover
coverage report -m

The design of this app:
This web crawler is a mini app. When you provide a small entry URL, the crawler will print all the URLs on the same domain, 
as well as all the links found on the pages.

This crawler will have two main storage components.
-One is called "urls_queue," where we will put the entry URL and all the validated URLs. Every time we take a URL from the queue, 
we fetch the HTML content, parse it, extract the URLs from the content, validate them, and put the validated URLs into the urls_queue.
