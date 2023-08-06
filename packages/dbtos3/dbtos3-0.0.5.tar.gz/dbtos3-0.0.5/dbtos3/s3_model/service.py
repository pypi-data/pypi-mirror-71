import calendar
import json
import logging
import os
import time
from datetime import datetime, date

import boto3

try:
    os.mkdir('Logs')
except FileExistsError:
    pass

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename='Logs/logs-{}.log'.format(datetime.now().strftime('%d%m%y%H%M')),
                    filemode='w', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class S3ServiceMethod:
    """
    PostgreSQL_Model replication methods
    """

    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, s3bucket,
                 main_key):

        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

        self.s3bucket = s3bucket
        self.s3main_key = main_key

        self.s3resource = boto3.resource('s3',
                                         region_name=region_name,
                                         aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key)

    def write_to_s3(self, local, data):
        """
        gathers data frame object and parses it to s3 .json object

        :param local: string. the table that is being replicated or loaded in order to name the directory accordingly
        :param data: json object. the json object to be parsed into and s3 object
        :return: writes object directly to s3
        """
        try:
            logging.info('[s3.service] writing dataframe of table {} to s3 [{}]'.format(local, datetime.now()))
            if len(data) < 1:
                logging.info('[s3.service] no data in {} needs to be sent to s3 [{}]'.format(local, datetime.now()))
            else:
                def json_serial(obj):
                    """JSON serializer for objects not serializable by default json code"""
                    if isinstance(obj, (datetime, date)):
                        return obj.isoformat()
                    raise TypeError("Type %s not serializable" % type(obj))

                s3_object = self.s3resource.Object(self.s3bucket, '{1}/{0}/{0}-{2}.json'
                                                   .format(local, self.s3main_key, calendar.timegm(time.gmtime())))
                s3_object.put(Body=(bytes(json.dumps(data, default=json_serial, allow_nan=True)
                                          .encode('UTF-8'))))

        except Exception as error:
            logging.info('[s3.service] error while trying to send {} data to s3: {} [{}]'
                         .format(local, error, datetime.now()))

        finally:
            logging.info('[s3.service] loading data from {} to s3 done! [{}]'.format(local, datetime.now()))

    def specific_write_to_s3(self, folder, file, data):
        """
        gathers data frame object and parses it to s3 .json object and writes to a SPECIFIC folder

        :param folder: the specific folder stored in the main key
        :param file: the unique name of the file stored
        :param data: json object. the json object to be parsed into and s3 object
        :return: writes object directly to s3
        """
        try:
            logging.info('[s3.service] writing dataframe of table {} to s3 [{}]'.format(file, datetime.now()))
            if len(data) < 1:
                logging.info('[s3.service] no data in {} needs to be sent to s3 [{}]'.format(file, datetime.now()))
            else:
                def json_serial(obj):
                    """JSON serializer for objects not serializable by default json code"""
                    if isinstance(obj, (datetime, date)):
                        return obj.isoformat()
                    raise TypeError("Type %s not serializable" % type(obj))

                # folder/file-date
                s3_object = self.s3resource \
                    .Object(self.s3bucket, '{0}/{1}/{2}-{3}.json'
                            .format(self.s3main_key, folder, file, calendar.timegm(time.gmtime())))
                s3_object.put(Body=(bytes(json.dumps(data, default=json_serial, allow_nan=True)
                                          .encode('UTF-8'))))

        except Exception as error:
            logging.info(
                '[s3.service] error while trying to send {} data to s3: {} [{}]'.format(file, error, datetime.now()))

        finally:
            logging.info('[s3.service] loading data from {} to s3 done! [{}]'.format(file, datetime.now()))
