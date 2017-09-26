#Views created in Database

##Create view top_articles
CREATE VIEW top_articles as 
	SELECT articles.title, count(*) as num 
	FROM articles, log 
	WHERE log.path = concat('/article/',articles.slug) 
	AND log.status = '200 OK' 
	GROUP BY articles.title 
	ORDER BY num DESC;

