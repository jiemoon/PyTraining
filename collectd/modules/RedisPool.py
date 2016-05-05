#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
import redis


class Redis(object):
    def __init__(self, host, port=5123, max_connections=5):
        # create redis connection pool, default 5 connections
        __conn_pool = redis.ConnectionPool(host=host, port=port,
                                           max_connections=max_connections)
        self.__redis_conn = redis.Redis(connection_pool=__conn_pool)
        self.__pipeline = self.__redis_conn.pipeline()

    def redis_hset(self, redis_key, redis_fields, redis_values, key_expire=30):
        """Hset redis key-val to redis key

        :param redis_key: redis key
        :param redis_fields: redis fields in redis key
        :param redis_values: redis values for redis field
        :param key_expire: redis key expire time, default 30 seconds
        :return: None
        """
        fields_len = len(redis_fields)
        self.__pipeline.expire(redis_key, key_expire)
        for i in xrange(fields_len):
            self.__pipeline.hset(redis_key, redis_fields[i], redis_values[i])
        self.__pipeline.execute()
