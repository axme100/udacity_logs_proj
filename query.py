#!/usr/bin/env python3

# Import psycopg2, used to interact with PostgreSQL databases
import psycopg2

# Set up the DB forum name
DBNAME = "news"


def most_popular_articles():

    # Create a connection object
    db = psycopg2.connect(database=DBNAME)

    # Open a cursor into the database
    cursor = db.cursor()

    # Execute an SQL command
    cursor.execute("SELECT * FROM top_articles LIMIT 3;")

    # Retreieve the data
    results = cursor.fetchall()

    # Close the database
    db.close()

    print("")
    print("The top 3 most popular articles: ")
    print("")
    print("1) Title: " + results[0][0] + "--Views: " + str(results[0][1]))
    print("2) Title: " + results[1][0] + "--Views: " + str(results[1][1]))
    print("3) Title: " + results[2][0] + "--Views: " + str(results[2][1]))
    print("")


def most_popular_article_authors():

    # Create a connection object
    db = psycopg2.connect(database=DBNAME)

    # Open a cursor into the database
    cursor = db.cursor()

    # Execute an SQL command
    cursor.execute("""
                  SELECT name, SUM(num) AS total_views
                  FROM name_title_num GROUP BY name_title_num.name
                  ORDER BY total_views DESC;""")

    # Retreieve the data
    results = cursor.fetchall()

    # Close the database
    db.close()

    print("")
    print("The Top Authors:")
    print("")
    print("1) Author: " + results[0][0] +
          "--Total Views: " + str(results[0][1]))
    print("2) Author: " + results[1][0] +
          "--Total Views: " + str(results[1][1]))
    print("3) Author: " + results[2][0] +
          "--Total Views: " + str(results[2][1]))
    print("4) Author: " + results[3][0] +
          "--Total Views: " + str(results[3][1]))
    print("")


def more_than_one_percent():

    # Create a connection object
    db = psycopg2.connect(database=DBNAME)

    # Open a cursor into the database
    cursor = db.cursor()

    # Execute an SQL command
    cursor.execute("""
                  SELECT day, percent_not_200
                  FROM decimal_results_truncated
                  WHERE percent_not_200 > 1;""")

    # Retreieve the data
    results = cursor.fetchall()

    # Close the database
    db.close()

    # Return the results, note that fetchall()
    # returns a list with a tuple inside of it
    # thus the complicated indexing

    print("")
    print("Days in which more than 1% of requests failed: ")
    print("")
    print("On " + str(results[0][0].date()) +
          " " + str(results[0][1]) + "% of requesets led to errors")
    print("")

most_popular_articles()
most_popular_article_authors()
more_than_one_percent()
