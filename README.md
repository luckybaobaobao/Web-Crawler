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