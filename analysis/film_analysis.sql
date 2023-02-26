/*
IMDb Top Rated Movies Data Exploration
Skills used: CASE Statement, Joins, Subqueries, CTEs, Temp Tables, Windows Functions, Aggregate Functions
*/

select * from imdb_top_movies;

-- Directors that appear on the list more than once
select distinct director, count(director) as director_count
from imdb_top_movies
group by director
having director_count > 1
order by director_count desc;

-- Most popular film periods
with film_time (movie_name, release_year, film_periods) as (
	select movie_name, release_year, 
    case -- Categorize films into various periods based on their year of release
		when release_year >= 1927 and release_year <= 1940 then '1927 - 1940: Talkies and the Rise of the Hollywood Studios'
		when release_year >= 1941 and release_year <= 1954 then '1941 - 1954: Golden Era of Film and Restructuring of Hollywood'
		when release_year >= 1955 and release_year <= 1976 then '1955 - 1976: Industry Changes due to Rise of Television'
		when release_year >= 1977 and release_year <= 1995 then '1977 - 1995: Dawn of Modern Film Industry and Appearance of Blockbusters'
		else '1996 - Present: Modern Film Industry'
    end as film_periods
	from imdb_top_movies)
select film_periods, count(film_periods) as periods_count
from film_time
group by film_periods
order by film_periods;

-- Movies that were released in the same year, ranked
select distinct a.release_year, dense_rank() over (partition by a.release_year order by a.imdb_rank) as movie_rank, a.movie_name
from imdb_top_movies a
inner join imdb_top_movies b
	on a.release_year = b.release_year
	and a.movie_name != b.movie_name
order by 1, 2;

-- Most Popular Genres
drop table if exists genre_rank;
create temporary table genre_rank(
	movie_name varchar(100),
    imdb_rank int,
    genre varchar(50)
);
insert into genre_rank(
	select movie_name, imdb_rank, trim(substring_index(substring_index(m.genre, ',', n.n), ',', -1)) as movie_genre
	from imdb_top_movies m cross join(
		select a.N + b.N * 10 + 1 n
		from
			(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) a,
			(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) b
		order by n
	) n
	where n.n <= 1 + (length(m.genre) - length(replace(m.genre, ',', '')))
	order by imdb_rank, movie_genre
);
select rank() over (order by count(genre) desc) as ranking, genre, count(genre) as genre_count
from genre_rank
group by genre
order by genre_count desc;


