#Import psycopg2, used to interact with PostgreSQL databases
import psycopg2	

#Set up the DB forum name
DBNAME = "news"


def most_popular_articles():

    #Create a connection object
    db = psycopg2.connect(database=DBNAME) 

    #Open a cursor into the database
    cursor = db.cursor()

    #Execute an SQL command
    cursor.execute("SELECT * FROM top_articles LIMIT 3;")

    #Retreieve the data
    results = cursor.fetchall()

    #Close the database
    db.close()

    print("The three most popular artilces are: ") 
    print(results[0])
    print(results[1]) 
    print(results[2])

def most_popular_article_authors():

    #Create a connection object
    db = psycopg2.connect(database=DBNAME) 

    #Open a cursor into the database
    cursor = db.cursor()

    #Execute an SQL command
    cursor.execute("")

    #Retreieve the data
    results = cursor.fetchall()

    #Close the database
    db.close()

    print("The three most popular artilces are: ") 
    print(results[0])
    print(results[1]) 
    print(results[2])


most_popular_articles()




'''
# Database code for the DB Forum, full solution!

import psycopg2, bleach

DBNAME = "forum"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select content, time from posts order by time desc")
  posts = c.fetchall()
  db.close()
  return posts

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("insert into posts values (%s)", (bleach.clean(content),))  # good
  db.commit()
  db.close()
'''






# Code fro the first SQL problem
'''
SELECT articles.title, count(*) as num 
	FROM articles, log 
	WHERE log.path = concat('/article/',articles.slug) 
	AND log.status = '200 OK' GROUP BY articles.title 
	ORDER BY num 
	DESC LIMIT 3;

Create top articles table


Create title_author table
create view title_author as SELECT articles.title, authors.name FROM articles, authors WHERE articles.author = authors.id;



CREATE VIEW name_title_num as SELECT title_author.name, top_articles.title, top_articles.num FROM top_articles, title_author WHERE title_author.title = top_articles.title;


#SQL Code for the second problem

SELECT name, SUM(num) AS total_views 
FROM name_title_num 
GROUP BY name_title_num.name 
ORDER BY total_views DESC;



Start the 3rd problem



SQL CODE: to get a table with two columns, day and number_of_time_not_200ok
CREATE VIEW day_not_200 AS SELECT date_trunc('day', log.time) AS day, count(*) AS not_200_ok_count FROM log WHERE log.status != '200 OK' GROUP BY DAY ORDER BY DAY DESC; 

SQL CODE: to get a table with two columns, date and total number of HTTP requests
CREATE VIEW day_total_requests AS SELECT date_trunc('day', log.time) AS day, count(*) AS not_200_ok_count FROM log GROUP BY DAY ORDER BY DAY DESC;

SQL CODE: Combine the above two tables
CREATE VIEW day_not_200_total_requests AS SELECT day_not_200.day, day_not_200.not_200_ok_count, day_total_requests.total_requests FROM day_not_200, day_total_requests WHERE day_not_200.day = day_total_requests.day;

SQL CODE: get the results in decimal format
CREATE VIEW decimal_results AS select day_not_200_total_requests.day,(cast(day_not_200_total_requests.not_200_ok_count as decimal) / day_not_200_total_requests.total_requests) AS percent_not_200 FROM day_not_200_total_requests;

SQL CODE THAT WILL ACTUALLY GO INTO SYNTAX ###The only thing that is missing from here is only returning the ones that are greater than 1%
CREATE VIEW decimal_results_truncated AS select day, trunc(percent_not_200*100, 2) AS percent_not_200 FROM decimal_results;

#Actual Syntax to put into tables
SELECT day, percent_not_200 FROM decimal_results_truncated WHERE percent_not_200 > 1;




'''