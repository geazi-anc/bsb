from datetime import datetime

import pendulum
from airflow.decorators import dag, task

from etl.extraction import get_top5_best_sellers
from etl.load import (load_to_datalake, load_to_datawarehouse,
                      read_from_datalake)
from etl.transform import (apply, convert_weeks_on_the_list_to_int,
                           format_author_name, format_best_seller_title)


@dag(
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False
)
def bsb_dag():
    """
    ETL pipeline to extract best sellers fiction books from New York Times.

    * Extract: extract best sellers from New York Times via webscraping;
    * Transform: transforme some data of best sellers, such as **author name**, **weeks on the list**;
    * Load: load transformed best sellers to data warehouse, using MongoDB;
    """

    @task
    def extract_top5_best_sellers_from_nyt():
        """
        ## Extract
        At first, extract top5 best sellers fiction books from New York Times via webscraping.
        After, load pure data to datalake to be transformed in next task.
         """

        best_sellers = get_top5_best_sellers()
        load_to_datalake(best_sellers)

    @task
    def transform_best_sellers_books():
        """
        ## Transform
        After extraction, get best sellers from datalake, without '_id' field of MongoDB.
        So, use **apply** function to apply transform function in each best sellers from datalake. After, load these best sellers again to datalake.
        """

        best_sellers = read_from_datalake()

        best_sellers = apply(
            best_sellers, *(
                format_best_seller_title,
                format_author_name,
                convert_weeks_on_the_list_to_int
            )
        )

        load_to_datalake(best_sellers)

    @task
    def load_best_sellers_to_datawarehouse():
        """
        ## Load
        After transform task, get best sellers from datalake. After, load best sellers to data warehouse.
        """

        best_sellers = read_from_datalake()
        load_to_datawarehouse(best_sellers)

    # taskflow: ETL pipeline

    # extract
    extract_top5_best_sellers_from_nyt()

    # transform
    transform_best_sellers_books()

    # load
    load_best_sellers_to_datawarehouse()


dag = bsb_dag()
