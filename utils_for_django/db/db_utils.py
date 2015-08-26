#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150825
#  @date          20150825 - Build DbUtils
#  @version       0.0
"""Connection MySQL for SQLAlchemy
"""
import sys

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError


class DbConnecter(object):
    def __init__(self, conn_conf):
        """Fill out connection database information
        """
        self.conn_conf = conn_conf

    def get_db_connection(self):
        """Get db connection
        """
        # Data process: Define necessary variables before using
        tables = {}
        conn_conf = self.conn_conf
        connection_str = "%s://%s:%s@%s/%s?charset=utf8" % (conn_conf['driver'],
                                                            conn_conf['user'],
                                                            conn_conf['password'],
                                                            conn_conf['host'],
                                                            conn_conf['db'])
        conf_tables = conn_conf['tables']

        try:
            # Connection process: Start to connect database
            engine = sqlalchemy.create_engine(connection_str,
                                              strategy='threadlocal',
                                              pool_recycle=600)
            connection = engine.contextual_connect()

            # Connection process: Get table from database
            for (tag, table_name) in conf_tables.iteritems():
                metadata = sqlalchemy.MetaData()
                metadata.bind = engine
                table = sqlalchemy.Table(table_name, metadata, autoload=True)
                tables[tag] = table

            return (engine, connection, tables)
        except SQLAlchemyError:
            # Connection process: Database connection failed
            err_msg = "Error: unable to open connection to %s on %s." % (conn_conf['db'], conn_conf['host'])
            sys.stdout.flush()
            return (None, None, None)

    def close_db_connection(self, engine_map):
        """Close db connection
        """
        try:
            for engine_name in engine_map:
                engine_map[engine_name].contextual_connect().close()
                engine_map[engine_name].dispose()
                del engine_map[engine_name]
        except:
            pass
