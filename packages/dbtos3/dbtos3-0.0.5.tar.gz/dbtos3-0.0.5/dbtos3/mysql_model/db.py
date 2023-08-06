import logging
import os
from datetime import datetime

import mysql.connector
import pandas as pd

from dbtos3.s3_model import service
from dbtos3.sqlite_model import catalogue

try:
    os.mkdir('Logs')
except FileExistsError:
    pass

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename='Logs/logs-{}.log'.format(datetime.now().strftime('%d%m%y%H%M')),
                    filemode='w', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class ReplicationMethodsMySQL:
    """
    mySQL_Model replication methods
    """

    def __init__(self, host, database, user, password, region_name, aws_access_key_id, aws_secret_access_key, s3bucket,
                 main_key, port):
        """
        :param host: host name for db
        :param database: db name
        :param user: user name
        :param password: user password
        :param port: host port
        :param region_name: aws region
        :param aws_access_key_id: aws user key
        :param aws_secret_access_key: aws user password
        :param s3bucket: bucket to write to
        :param main_key: folder to write to
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

        self.s3bucket = s3bucket
        self.s3main_key = main_key

        self.s3_service = service.S3ServiceMethod(
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            s3bucket=s3bucket,
            main_key=main_key
        )

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database,
            port=self.port
        )

        self.cursor = self.connection.cursor()

        # ensures the catalogue exists
        catalogue.CatalogueMethods().set_up_catalogue()

    @staticmethod
    def update_catalogue(column_name, column_time, table_name, app_run_time, data_source):
        update_catalogue = catalogue.CatalogueMethods()
        update_catalogue.update_catalogue(column_name=column_name, column_time=column_time, table_name=table_name,
                                          app_run_time=app_run_time, data_source=data_source)

    def day_level_full_load(self, days, table, column):
        try:
            logging.info(
                '[mysql.db] loading data from {} at {} days based on column {} [{}]'.format(table, days, column,
                                                                                            datetime.now()))

            table_columns = []
            # construct query to get nth days of data from table & all column names of that table
            data_query = "select * from {} where {} > now() - interval {} day".format(table, column, days)
            column_query = "show columns from {}".format(table)

            # execute queries and allocate them to objects

            # gather all column names for data frame
            self.cursor.execute(column_query)
            for c in self.cursor.fetchall():
                table_columns.append(c[0])

            # substitute for real dictionary cursor to preserve the column names of the table
            # querying from the database and simply parsing to json loses vital data, so the
            # steps below gather the data, and generates a dict that zips column names to relevant data
            # this is as efficient as I can develop, so will need to look for something better in future
            self.cursor.execute(data_query)
            columns = [desc[0] for desc in self.cursor.description]
            data = [dict(zip(columns, row)) for row in self.cursor.fetchall()]

            # create data frame to easily gather values using pandas
            data_frame = pd.DataFrame(data, columns=table_columns)

            # updates catalogue
            self.update_catalogue(column_name=column, column_time=data_frame[column].max(),
                                  table_name=table, app_run_time=datetime.now(), data_source='mysql-{}'.format(table))

            # use write to s3 method to send data frame directly to s3
            self.s3_service.write_to_s3(data=data, local=table)

        except Exception as error:
            logging.info('[mysql.db] error while loading table from MySQL: {} [{}]'.format(error, datetime.now()))

        finally:
            logging.info(
                '[mysql.db] loading data from {} at {} days based on column {} done! [{}]'.format(table, days, column,
                                                                                                  datetime.now()))

    def replicate_table(self, table, column):
        """
        gathers information from s3 .csv object and determines what data needs replication from the database
        :param table: string. the table that will be updated and replicated from
        :param column: string. the column that satisfies the date parameter for replication
        :return: writes directly to s3
        """
        try:
            logging.info(
                '[mysql.db] replicating table {} based on timestamp {} [{}]'.format(table, column, datetime.now()))

            # get max update time first from catalogue
            max_update_time = catalogue.CatalogueMethods().get_max_time_from_catalogue(table=table,
                                                                                       data_source='mysql-{}'.format(
                                                                                           table))

            # construct query to get nth days of data from table & all column names of that table
            if max_update_time is None:
                logging.info('[mysql.db] no need to update {}! [{}]'.format(table, datetime.now()))
            else:
                data_query = "select * from {} where {} > '{}'".format(table, column, max_update_time)

                # if method will pass the data if there is no updates needed
                self.cursor.execute(data_query)

                # substitute for real dictionary cursor to preserve the column names of the table
                # querying from the database and simply parsing to json loses vital data, so the
                # steps below gather the data, and generates a dict that zips column names to relevant data
                # this is as efficient as I can develop, so will need to look for something better in future
                columns = [desc[0] for desc in self.cursor.description]
                data = [dict(zip(columns, row)) for row in self.cursor.fetchall()]

                catalogue.CatalogueMethods().update_catalogue(column_name=column,
                                                              column_time=self.get_max_time_from_db(table=table,
                                                                                                    column=column),
                                                              table_name=table,
                                                              app_run_time=datetime.now(),
                                                              data_source='mysql-{}'.format(table))

                self.s3_service.write_to_s3(data=data, local=table)

        except Exception as error:
            logging.info('[mysql.db] error while loading table from MySQL: {} [{}]'.format(error, datetime.now()))

        finally:
            logging.info(
                '[mysql.db] loading data from {} based on column {} done! [{}]'.format(table, column, datetime.now()))

    def get_max_time_from_db(self, table, column):
        try:
            logging.info(
                '[mysql.db] getting max time from {} to update catalogue based on {} [{}]'.format(table, column,
                                                                                                  datetime.now()))

            data_query = "select max({}) from {}".format(column, table)
            self.cursor.execute(data_query)
            return self.cursor.fetchall()[0][0]

        except Exception as error:
            logging.info('[mysql.db] error while loading table from MySQL: {} [{}]'.format(error, datetime.now()))

        finally:
            logging.info('[mysql.db] getting max time from {} complete! [{}]'.format(table, datetime.now()))

    def close_connection(self):
        """
        closes connection to database
        :return: none
        """
        logging.info('[mysql.db] closing all connections [{}]'.format(datetime.now()))
        self.connection.close()
        catalogue.CatalogueMethods().close_connection()
