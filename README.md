# To use this tool:
Download the python file query.py into the same folder as your database(the same folder as newsdata.sql). I assume you already have acsess to this database and are familiar with this udacity.com project. Run the python file from the command line `python3 query.py`



# The reporting tool depends on the following views that must be created in the databse

# Create the following views for the first problem

### SQL CODE: get a list of the articles sorted by the number of views (views in problem 2 also depend on top_articles)
`CREATE VIEW top_articles AS
	SELECT articles.title, count(*) as num
	FROM articles, log
	WHERE log.path = concat('/article/',articles.slug)
	AND log.status = '200 OK'
	GROUP BY articles.title
	ORDER BY num DESC;`

# Create the following views for the second problem:

### Create view tite_author
`CREATE VIEW title_author AS
	SELECT articles.title, authors.name
	FROM articles, authors
	WHERE articles.author = authors.id;`


### Create view name_title
`CREATE VIEW name_title_num AS
	SELECT title_author.name, top_articles.title, top_articles.num
	FROM top_articles, title_author
	WHERE title_author.title = top_articles.title;`

# Create the following views for the third problem:

### SQL CODE: to get a table with two columns, day and number_of_time_not_200ok
`CREATE VIEW day_not_200 AS
	SELECT date_trunc('day', log.time) AS day, count(*) AS not_200_ok_count FROM log WHERE log.status != '200 OK'
	GROUP BY DAY
	ORDER BY DAY DESC;`

### SQL CODE: to get a table with two columns, date and total number of HTTP requests
`CREATE VIEW day_total_requests AS
	SELECT date_trunc('day', log.time) AS day, count(*) AS not_200_ok_count
	FROM log
	GROUP BY DAY
	ORDER BY DAY DESC;`

### SQL CODE: Combine the above two tables
`CREATE VIEW day_not_200_total_requests AS
	SELECT day_not_200.day, day_not_200.not_200_ok_count, day_total_requests.total_requests
	FROM day_not_200, day_total_requests
	WHERE day_not_200.day = day_total_requests.day;`

### SQL CODE: get the results in decimal format
`CREATE VIEW decimal_results AS
	SELECT day_not_200_total_requests.day,(cast(day_not_200_total_requests.not_200_ok_count as decimal) / day_not_200_total_requests.total_requests) AS percent_not_200
	FROM day_not_200_total_requests;`

### SQL CODE: turn those results into percents
`CREATE VIEW decimal_results_truncated AS
	SELECT day, trunc(percent_not_200*100, 2) AS percent_not_200
	FROM decimal_results;`