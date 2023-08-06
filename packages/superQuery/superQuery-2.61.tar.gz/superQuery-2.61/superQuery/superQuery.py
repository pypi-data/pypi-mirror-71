import os
import sys
import json
import logging

import pymysql.cursors
import pandas as pd

# The pydrive and oauth2 context belongs to the superQuery 
# export to Jupyter flow
try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    from oauth2client.client import GoogleCredentials
except ImportError:
    print("[sQ] pyDrive or oauth2 clietn import error.")


LOG_DIR = os.getenv("SUPERQUERY_LOGDIR")
LOG_LEVEL = os.getenv("SUPERQUERY_LOGLEVEL") or logging.INFO

def setup_logging():
    loglevel = int(LOG_LEVEL)
    fmt = "%(asctime)s - [%(name)s] ...%(message)s"
    logger = logging.getLogger("sQ")
    formatter = logging.Formatter(fmt)
    logger.setLevel(loglevel)
    logname = "superPy"
    if LOG_DIR is not None:
        logfname = os.path.join(LOG_DIR, logname + ".log")
        ofstream = logging.handlers.TimedRotatingFileHandler(logfname, when="D", interval=1, encoding="utf-8")
        ofstream.setFormatter(formatter)
        logger.addHandler(ofstream)
    #Console output:
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger

LOGGER = setup_logging()


class Configuration(object):

    def __init__(self):
        self.config = None
        self.configString = ""

    def configure_parameters(self, config):
        
        for item in config:
            self.configString += item + " "
            self.configString += config[item] + " "

        return self.configString

class QueryJobConfig(object):

    def __init__(self):
        self.destination = None

class Row(object):
    def __init__(self, rowdict):
        self.__dict__ = rowdict

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return self.__dict__


class Result:
    def __init__(self, cur=None, stats=None):
        self._cur = cur
        self.stats = Row(stats)

    def __iter__(self):
        return self.result()

    def _set_job_reference(self, jobRef):
        for key, value in jobRef.items():
            setattr(self, key, jobRef[key])

    def result(self):
        while True:
            row = self._cur.fetchone()
            if row is not None:
                row = Row(row)
                yield row
            else:
                break

    def to_df(self):
        return pd.DataFrame([row.to_dict() for row in self])


class Client(object):

    def __init__(self, usernameDriveAuth=None):
        self._logger = logging.getLogger("sQ")
        self._usernameDriveAuth = usernameDriveAuth
        self._username = os.getenv("SUPERQUERY_USERNAME")
        self._password = os.getenv("SUPERQUERY_PASSWORD") 
        self._user_agent = "python"
        self._project = None
        self._destination_dataset = None
        self._destination_project = None
        self._destination_table = None
        self._write_disposition = None
        self._log_query_results = True
        self.result = None
        self.connection = None

        self._BQ_DML_list = ["INSERT", "UPDATE", "DELETE"]
    
    def get_colab_auth_from_drive(self, usernameDriveAuth):
        user_auth = None
        self._logger.debug("Trying to get auth file from Google Drive")
        try:
            from google.colab import auth
            auth.authenticate_user()
            gauth = GoogleAuth()
            gauth.credentials = GoogleCredentials.get_application_default()
            drive = GoogleDrive(gauth)

            file_list = drive.ListFile().GetList()
            user_auth = None

            for f in file_list:
                if f['title'] == "auth.json":
                    fname = f['title']
                    f_ = drive.CreateFile({'id': f['id']})

                    self._logger.debug("Got auth file!")
                    user_auth = f_.GetContentString(fname)
                    self._username = usernameDriveAuth
                    self._password = json.loads(user_auth)['value']

                    self._logger.debug("Saving auth to environment")
                    os.environ['SUPERQUERY_USERNAME'] = self._username
                    os.environ['SUPERQUERY_PASSWORD'] = self._password

                    # self._logger.debug("Removing auth file!")
                    # f_.Trash()  # Move file to trash.
                    # f_.UnTrash()  # Move file out of trash.
                    # f_.Delete()  # Permanently delete the file.
                    break;

        except Exception as e:
            print("[sQ] Error in Drive flow...")
            self._logger.exception(e)

    def project(self, project):
        self._project = project
        return self

    def dataset(self, dataset):
        self._destination_dataset = dataset
        return self

    def table(self, table):
        self._destination_table = table
        return self

    def write_disposition(self, disposition):
        self._write_disposition = disposition
        return self

    def destination_project(self, project):
        self._destination_project = project
        return self

    def get_data_by_key(self, key, username=None, password=None):
        raise NotImplementedError("Up next...")

    def set_log_query_results(self, log_query):
        self._log_query_results = log_query
        return self
    
    def get_log_query_results(self):
        return self._log_query_results

    def query(self,
              sql,
              project=None,
              dry_run=False,
              use_cache=True,
              username=None,
              password=None,
              close_connection_afterwards=True,
              job_config=None,
              hostname="bi.superquery.io"):
        
        if job_config is not None:
            raise NotImplementedError("The job_config parameter is not yet handled")

        if (self._username is None or self._password is None) and self._usernameDriveAuth:
            self.get_colab_auth_from_drive(self._usernameDriveAuth)
        
        username = username or self._username
        password = password or self._password
        if username is None or password is None:
            raise Exception("Username or password not specified")

        try:
            #Reuse or establish connection:
            if self.connection is None:
                self._logger.debug("Establishing a new connection")
                self.connection = self.authenticate_connection(username, password, hostname=hostname)
                if self.connection is None:
                    raise Exception("Unable to establish a connection")
                else:
                    self._logger.debug("Connection to superQuery successful")
            else:
                self._logger.debug("Using existing superQuery connection!")

            #We have a connection:
            self._set_destination_project()
            self._set_destination_dataset()
            self._set_destination_table()

            #BQ does not allow to set write disposition to DML with error: Cannot set write disposition in jobs with DML statements
            #https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language      
            if not any(DML_word in sql.upper() for DML_word in self._BQ_DML_list):
                self._set_write_disposition()

            self._set_dry_run(dry_run)
            self._set_caching(use_cache)
            self._set_user_agent()
            self._set_project(project)

            #We have a successful setup: 
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                with self.connection.cursor() as cursor2:
                    cursor2.execute("explain;")
                    explain = cursor2.fetchall()
                    stats = json.loads(explain[0]["statistics"])
                    stats = self.clean_stats(stats)
                    #job_reference = json.loads(explain[0]["jobReference"])
                self.result = Result(cursor, stats)
                if float(stats['bigQueryTotalBytesProcessed']) > 0:
                    savings = (float(stats['bigQueryTotalBytesProcessed']) - float(stats['superQueryTotalBytesProcessed'])) / float(stats['bigQueryTotalBytesProcessed']) * 100
                else:
                    savings = 0
                if self._log_query_results:
                    print("[sQ] Cost: ${0}, superQuery saved you: {1}%, Speedup: {2}X".format(round(stats['superQueryTotalBytesProcessed']/1024**4 * 5,4), str( round(savings , 2)), round(1/(1-((savings if savings < 100 else savings-1)/100)),2)))
                return self.result

        except Exception as e:
            self._logger.error("An error occurred (perhaps retry)")
            self._logger.exception(e)
            self.connection = None

        finally:
            if close_connection_afterwards:
                self.close_connection()

    def clean_stats(self, stats):

        if (type(stats['superQueryTotalBytesProcessed']).__name__ == 'str'):
            stats['superQueryTotalBytesProcessed'] = 0

        return stats

    def close_connection(self):
        if (self.connection):
            self._logger.debug("Closing the connection")
            self.connection.close()
            self.connection = None

    def _set_user_agent(self):
        self.connection._execute_command(3, "SET super_userAgent=" + self._user_agent)
        self.connection._read_ok_packet()

    def _set_project(self, project=None):
        project = project or self._project
        if project is not None:
            self._logger.debug("Setting the project to %s", project)
            self.connection._execute_command(3, "SET super_projectId=" + project)
            self.connection._read_ok_packet()

    def _set_destination_project(self):
        project = self._destination_project or self._project
        if project is not None:
            self._logger.debug("Setting the destination project to %s", project)
            self.connection._execute_command(3, "SET super_destinationProject=" + project)
            self.connection._read_ok_packet()

    def _set_destination_dataset(self):
        if self._destination_dataset is not None:
            self._logger.debug("Setting the destination dataset to %s", self._destination_dataset)
            self.connection._execute_command(3, "SET super_destinationDataset=" + self._destination_dataset)
            self.connection._read_ok_packet()

    def _set_destination_table(self):
        if self._destination_table is not None:
            self._logger.debug("Setting the destination table to %s", self._destination_table)
            self.connection._execute_command(3, "SET super_destinationTable=" + self._destination_table)
            self.connection._read_ok_packet()

    def _set_write_disposition(self):
        disposition = self._write_disposition or "WRITE_EMPTY"
        self._logger.debug("Setting write-disposition to %s", disposition)
        self.connection._execute_command(3, "SET super_destinationWriteDisposition=" + disposition)
        self.connection._read_ok_packet()

    def _set_dry_run(self, is_dryrun=False):
        self._logger.debug("Setting dry run to %s", str(is_dryrun))
        if is_dryrun:
            self.connection._execute_command(3, "SET super_isDryRun=true")
        else:
            self.connection._execute_command(3, "SET super_isDryRun=false")
        self.connection._read_ok_packet()

    def _set_caching(self, use_cache=True):
        self._logger.debug("Setting cache to %s", str(use_cache))
        if use_cache:
            self.connection._execute_command(3, "SET super_useCache=true")
        else:
            self.connection._execute_command(3, "SET super_useCache=false")
        self.connection._read_ok_packet()

    def authenticate_connection(self, username, password, hostname="bi.superquery.io", port=3306):
        try:
            connection = pymysql.connect(
                host=hostname,
                port=port,
                user=username,
                password=password,
                db="",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            return connection
        except Exception as e:
            self._logger.debug("Authentication problem!")
            self._logger.exception(e)
            raise

    @property
    def stats(self):
        if self.result is not None:
            return self.result.stats
