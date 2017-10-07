from setuptools import setup, find_packages

setup(
    name='Finance Data Scaper API',
    version='1.0.0',
    url='https://github.com/ajpotato214/Finance-Data-Scraper-API',
    packages=['finance_data_scraper', 'finance_data_scraper.scrapers'],
    description="A web-based RESTful API that scrapes various financial websites",
    license='MIT',
    install_requires=[
        'Flask>=0.11.1',
        'tornado',
        'requests',
        'lxml',
        'python-memcached',
        'flask-restful',
    ]
)
