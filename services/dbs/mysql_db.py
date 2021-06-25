import logging as logger

logger.basicConfig(level=logger.INFO)

import pymysql
from common.config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DB,
    MYSQL_TABLE,
)

connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    port=MYSQL_PORT,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    cursorclass=pymysql.cursors.DictCursor,
)

cursor = connection.cursor()


def create_table_mysql():
    logger.info(f"MYSQL creating table : {MYSQL_TABLE}")

    sql = (
        "create table if not exists "
        + MYSQL_TABLE
        + "(vector_id bigint, embedding_id text, idea_id text, index ix_vector_id (vector_id));"
    )

    try:
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        logger.error("MYSQL ERROR:", sql, e)


create_table_mysql()


def delete_table():
    logger.info(f"MYSQL deleting table : {MYSQL_TABLE}")

    sql = "drop table if exists " + MYSQL_TABLE + ";"

    try:
        cursor.execute(sql)
        connection.commit()

    except Exception as e:
        logger.error("MYSQL ERROR:", sql, e)


def fetch_vector_id(embedding_id):
    sql = f"select vector_id from {MYSQL_TABLE} where embedding_id = '{embedding_id}'"

    try:
        cursor.execute(sql)
        res = cursor.fetchone()

        if res:
            return res["vector_id"]
    except Exception as e:
        logger.error("MYSQL ERROR:", sql, e)


def fetch_embedding_ids(vector_ids):
    if not vector_ids:
        return {}

    # vector_ids_tuple = tuple(vector_ids)
    sql = f"select vector_id, embedding_id from {MYSQL_TABLE} where vector_id in ({','.join(str(v) for v in vector_ids)})"

    print("sql")
    print(sql)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        embedding_docs_dict = {}

        for res in results:
            embedding_docs_dict[res["vector_id"]] = res["embedding_id"]

        return embedding_docs_dict
    except Exception as e:
        logger.error("MYSQL ERROR:", sql, e)


# data_list = [(idea_id, vector_ids, embedding_ids)]
def insert_embeddings(values):

    sql = (
        f"insert into {MYSQL_TABLE}(idea_id,vector_id,embedding_id) values (%s, %s, %s)"
    )

    try:
        cursor.executemany(sql, values)
        connection.commit()
    except Exception as e:
        logger.error("MYSQL ERROR:", sql, e)


def delete_embeddings(doc_id):
    sql = f"delete from {MYSQL_TABLE} where idea_id='{doc_id}'"

    try:
        cursor.execute(sql)
        connection.commit()

    except Exception as e:
        logger.error("MYSQL ERROR:", sql, e)


def get_vector_ids(doc_id):
    sql = f"select vector_id from {MYSQL_TABLE} where idea_id = '{doc_id}'"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        vector_ids = [res["vector_id"] for res in results]

        return vector_ids
    except Exception as e:
        logger.error("MYSQL ERROR:", sql, e)
