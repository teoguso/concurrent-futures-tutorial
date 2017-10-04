#!/usr/bin/env python
"""
Collection of utility functions
"""
import hashlib
import json
import logging
import random
import time
from google.cloud import bigquery


logger = logging.getLogger("helpers.py")
random.seed(42)


def n_fibonacci(n=10):
    """Calculate the Nth Fibonacci number"""
    i = 0
    x = 1
    if n < 2:
        return n
    for __ in range(n - 1):
        x, i = x + i, x
    return x

def fake_io(whatevs=None):
    """Take some time as if it were writing to disk/calling a rest API"""
#     long_time = np.random.randint(1,5)
    long_time = .2 + 0.2 * random.random()
    time.sleep(long_time)
    # return "Done with {} after {} secs".format(whatevs, long_time)
    return whatevs

def calc_length(x):
    """Typically x is an int"""
    return len(str(x))


def digits_fibonacci(n):
    """Calculate the number of digits in the nth Fibonacci number"""
    return calc_length(n_fibonacci(n))


def calc_lengths(iterable_object):
    """Generate lenghts of values from generator.
    
    Works for any iterable.
    """
    for x in iterable_object:
        yield calc_length(x)

def print_stuff(generator_object):
    """Print values as they are generated"""
    for x in generator_object:
        print(x)


def stream_data(json_data, dataset_name, table_name):
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)
    data = json.loads(json_data)

    # Reload the table to get the schema.
    try:
        table.reload()
    except Exception as e:
        logger.error(e)

    rows = [data.values()]
    logger.debug('stream_data')
    try:
        logger.debug('stream_data')
        errors = table.insert_data(rows)
        if not errors:
            logger.debug('stream_data, not errors')
            logger.info('Loaded 1 row into {}:{}'.format(dataset_name, table_name))
        else:
            logger.debug('stream_data, errors')
            logger.warning('Errors: {}'.format(errors))
        return errors
    except Exception as e:
        logger.debug('stream_data, exceptions')
        logger.error(e)


def create_bigquery_client():
    """Build the bigquery client."""
    credentials = GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
            credentials = credentials.create_scoped(BQ_SCOPES)
    http = httplib2shim.Http()
    credentials.authorize(http)
    return discovery.build('bigquery', 'v2', http=http)


def bq_data_insert(records, bigquery_client, project_id, dataset, table, template_suffix=None):
    """Insert a list of records into the given BigQuery table

    Each row is expected to be a JSON-readable string.
    If template_suffix is provided, the given table is used as a template table,
    and a new table will be created, with name 'table+template_suffix'.
    """
    try:
        rowlist = []
        # Generate the data that will be sent to BigQuery
        for item in records:
            item_row = {
                "insertId": hashlib.sha256(bytes(str(item), 'utf-8')).hexdigest(),
                "json": json.loads(item),
            }
            rowlist.append(item_row)
        if not rowlist:
            return
        body = {
            "skipInvalidRows": True,
            "ignoreUnknownValues": True,
            "rows": rowlist,
        }
        if template_suffix:
            body["templateSuffix"] = template_suffix
        # Try the insertion.
        response = bigquery_client.tabledata().insertAll(
                projectId=project_id, datasetId=dataset,
                tableId=table, body=body).execute(num_retries=NUM_RETRIES)
        # logger.debug(
        #     "Request response: {} {}".format(
        #         datetime.datetime.now(), json.dumps(response)
        #     )
        # )
        return response
        # TODO: 'invalid field' errors can be detected here.
    except Exception as ex:
        logger.error("Giving up: {}".format(ex))
