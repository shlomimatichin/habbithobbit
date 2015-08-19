import elasticsearch
from elasticsearch import helpers
import simplejson
import logging
import datetime


class PutInElasticSearch:
    def __init__(self, filenames):
        self._es = elasticsearch.Elasticsearch()
        logging.info("Putting data into elastic search")
        total = self._putIn(filenames)
        logging.info("Done Putting data into elastic search")
        logging.info("Executing flush")
        self._es.indices.flush(index="events")
        logging.info("Done Executing flush")
        logging.info("Verifying flush")
        self._verify(total)
        logging.info("Done Verifying flush")

    def _putIn(self, filenames):
        total = 0
        for filename in filenames:
            indexActions = []
            with open(filename) as f:
                for line in f.readlines():
                    if line == "":
                        continue
                    for event in simplejson.loads(line):
                        event['time'] = datetime.datetime.fromtimestamp(event['time'])
                        action = {"_index": "events",
                                  "_type": "event",
                                  "_source": event}
                        indexActions.append(action)
            helpers.bulk(self._es, indexActions)
            total += len(indexActions)
        return total

    def _verify(self, total):
        count = 0
        for event in helpers.scan(self._es, index="events", doc_type="event"):
            count += 1
        if count != total:
            raise Exception("Number of document did not match. Expected %d documents, found %d" % (
                total, count))
