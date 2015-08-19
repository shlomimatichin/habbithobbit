import urllib2
import logging
import os


class DownloadPackages:
    _DOWNLOADED = "downloaded"
    _ELASTIC_SEARCH_URL = \
        "https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.1.tar.gz"
    _ELASTIC_SEARCH_BASENAME = _ELASTIC_SEARCH_URL.split("/")[-1]
    _ELASTIC_SEARCH_PATH = os.path.join(_DOWNLOADED, _ELASTIC_SEARCH_BASENAME)
    _KIBANA_URL = "https://download.elastic.co/kibana/kibana/kibana-4.1.1-linux-x64.tar.gz"
    _KIBANA_BASENAME = _KIBANA_URL.split("/")[-1]
    _KIBANA_PATH = os.path.join(_DOWNLOADED, _KIBANA_BASENAME)

    def downloadElasticSearch(self):
        logging.info("Downloading elastic search")
        self._download(self._ELASTIC_SEARCH_PATH, self._ELASTIC_SEARCH_URL)
        logging.info("Done Downloading elastic search")
        return self._ELASTIC_SEARCH_PATH

    def downloadKibana(self):
        logging.info("Downloading kibana")
        self._download(self._KIBANA_PATH, self._KIBANA_URL)
        logging.info("Done Downloading kibana")
        return self._KIBANA_PATH

    def _download(self, path, url):
        if os.path.exists(path):
            return
        connection = urllib2.urlopen(url)
        try:
            contents = connection.read()
        finally:
            connection.close()
        logging.info("Done Downloading elastic search")
        if not os.path.isdir(self._DOWNLOADED):
            os.mkdir(self._DOWNLOADED)
        with open(path, "wb") as f:
            f.write(contents)


if __name__ == "__main__":
    DownloadPackages().downloadElasticSearch()
    DownloadPackages().downloadKibana()
