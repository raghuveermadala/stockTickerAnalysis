FROM ubuntu

MAINTAINER Andy Papa

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
  python3 \
  python3-setuptools \
  python3-pip \
  python3-lxml \
  memcached \
  git \
&& rm -rf /var/lib/apt/lists/*

# Clone the project from GitHub
RUN git clone https://github.com/ajpotato214/Finance-Data-Scraper-API.git

WORKDIR /Finance-Data-Scraper-API

# Install Python3 modules via setuptools
RUN python3 setup.py install

# This is the default port Tornado runs on. If you change this then you should
# change this in Finance-Data-Scraper-API/finance_data_scraper/config.cfg as well
EXPOSE 8080

# Finally, run it
CMD ["python3", "finance_data_scraper/webserver.py"]
