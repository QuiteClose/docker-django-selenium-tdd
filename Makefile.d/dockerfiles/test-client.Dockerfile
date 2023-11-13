FROM python:3.9
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
        unzip
# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
# Install Chrome Driver
RUN apt-get install -yqq unzip
COPY Makefile.d/chromedriver_downloader.py ./
RUN python chromedriver_downloader.py /tmp/chromedriver.zip
# set display port to avoid crash
ENV DISPLAY=:99
WORKDIR /usr/src/app
COPY tests/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
