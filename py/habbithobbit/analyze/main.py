import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("elasticsearch").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
import argparse
import time
from habbithobbit.analyze import elasticsearchdaemon
from habbithobbit.analyze import kibanadaemon
from habbithobbit.analyze import putinelasticsearch


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="cmd")
toElasticCmd = subparsers.add_parser(
    "toElastic",
    help="Setup a fresh elastic search database with all data")
toElasticCmd.add_argument("input", nargs="+")
serveCmd = subparsers.add_parser("serve")
args = parser.parse_args()

if args.cmd == "toElastic":
    elasticsearchdaemon.ElasticSearchDaemon.clear()
    daemon = elasticsearchdaemon.ElasticSearchDaemon()
    putinelasticsearch.PutInElasticSearch(args.input)
elif args.cmd == "serve":
    daemon = elasticsearchdaemon.ElasticSearchDaemon()
    daemon2 = kibanadaemon.KibanaDaemon()
    time.sleep(1000000)
else:
    raise AssertionError("Unknown command: " + args.cmd)
