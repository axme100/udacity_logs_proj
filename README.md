# Create the following views for the first problem

## Create top_articles view
`CREATE VIEW top_articles AS
	SELECT articles.title, count(*) as num
	FROM articles, log
	WHERE log.path = concat('/article/',articles.slug)
	AND log.status = '200 OK'
	GROUP BY articles.title
	ORDER BY num DESC;`

###Views created for the second problem

##Create view tite_author
CREATE VIEW title_author AS
	SELECT articles.title, authors.name
	FROM articles, authors
	WHERE articles.author = authors.id;


##
CREATE VIEW name_title_num AS
	SELECT title_author.name, top_articles.title, top_articles.num
	FROM top_articles, title_author
	WHERE title_author.title = top_articles.title;

###Views created for the third problem

##SQL CODE: to get a table with two columns, day and number_of_time_not_200ok
CREATE VIEW day_not_200 AS
	SELECT date_trunc('day', log.time) AS day, count(*) AS not_200_ok_count FROM log WHERE log.status != '200 OK'
	GROUP BY DAY
	ORDER BY DAY DESC;

##SQL CODE: to get a table with two columns, date and total number of HTTP requests
CREATE VIEW day_total_requests AS
	SELECT date_trunc('day', log.time) AS day, count(*) AS not_200_ok_count
	FROM log
	GROUP BY DAY
	ORDER BY DAY DESC;

##SQL CODE: Combine the above two tables
CREATE VIEW day_not_200_total_requests AS
	SELECT day_not_200.day, day_not_200.not_200_ok_count, day_total_requests.total_requests
	FROM day_not_200, day_total_requests
	WHERE day_not_200.day = day_total_requests.day;

##SQL CODE: get the results in decimal format
CREATE VIEW decimal_results AS
	SELECT day_not_200_total_requests.day,(cast(day_not_200_total_requests.not_200_ok_count as decimal) / day_not_200_total_requests.total_requests) AS percent_not_200
	FROM day_not_200_total_requests;

SQL CODE THAT WILL TURN IT INTO PERCENTS
CREATE VIEW decimal_results_truncated AS
	SELECT day, trunc(percent_not_200*100, 2) AS percent_not_200
	FROM decimal_results;