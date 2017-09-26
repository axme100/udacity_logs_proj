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
    cursor.execute("SELECT name, SUM(num) AS total_views FROM name_title_num GROUP BY name_title_num.name ORDER BY total_views DESC;")


    #Retreieve the data
    results = cursor.fetchall()

    #Close the database
    db.close()

    print("The most popular article authors are: ") 
    print(results[0])
    print(results[1]) 
    print(results[2])
    print(results[3])

def more_than_one_percent():

    #Create a connection object
    db = psycopg2.connect(database=DBNAME) 

    #Open a cursor into the database
    cursor = db.cursor()

    #Execute an SQL command
    cursor.execute("SELECT day, percent_not_200 FROM decimal_results_truncated WHERE percent_not_200 > 1;")

    #Retreieve the data
    results = cursor.fetchall()

    #Close the database
    db.close()

    #Return the results, note that fetchall() returns a list with a tuple inside of it, thus the complicated indexing 
    print("On " + str(results[0][0].date()) + " " + str(results[0][1]) + "% of requesets led to errors")
    

print("Question 1")
print("")
most_popular_articles()
print("")
print("Question 2")
print("")
most_popular_article_authors()
print("")
print("Question 3")
print("")
more_than_one_percent()