'''
Web Scraping IMDb Top 100 Movies (Sorted by IMDb Rating)
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd

def main():
    # Request page source from URL
    url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
    response = requests.get(url)
    # Get page source
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create empty lists to assign values for later
    title = []
    rank = []
    year = []
    time = []
    genre = []
    rating = []
    metascore = []
    votes = []
    gross = []
    description = []
    director = []
    stars = []

    # Scrape page and store data
    movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
    # Find movie attributes
    for data in movie_data:

        # Title
        name = data.h3.a.text
        title.append(name)

        # IMDb Rank
        num = data.h3.find('span', class_='lister-item-index unbold text-primary').text
        num = num[:-1]
        rank.append(num)

        # Year of Release
        release_year = data.h3.find('span', class_='lister-item-year text-muted unbold').text
        release_year = release_year[-5:-1]
        year.append(release_year)

        # Runtime
        runtime = data.p.find('span', class_='runtime').text
        runtime = runtime.split(' ')
        runtime = runtime[0]
        time.append(runtime)

        # Genre
        gen = data.p.find('span', class_='genre').text
        gen = gen.strip()
        genre.append(gen)

        # Rating
        rate = data.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n', '')
        rating.append(rate)

        # Metascore
        score = data.find('span', class_='metascore').text.strip() if data.find('span', class_='metascore') else '' # extract if text exists
        metascore.append(score)

        # Votes & Gross - they have the same variable 'nv'
        value = data.find_all('span', attrs={'name': 'nv'})
        vote = value[0].text.replace(',', '')
        votes.append(vote)
        millions = value[1].text if len(value) > 1 else ''
        gross.append(millions[1:-1])

        # Description
        p_class = data.find_all('p', class_='text-muted')
        descript = p_class[1].text.strip() if len(p_class) > 1 else ''
        description.append(descript)

        # Director & Stars
        cast = data.find('p', class_='').text.replace('\n', '')
        cast = cast.split('|')
        direct = cast[0].split(':')[1]
        director.append(direct)
        star = cast[1].split(':')[1]
        stars.append(star)

    # Create dataframe of movie attributes
    df_movies = pd.DataFrame(list(zip(title, rank, year, time, genre, rating, metascore, votes, gross, description, director, stars)),
                            columns=['movie_name', 'imdb_rank', 'release_year', 'duration', 'genre', 'rating', 'metascore', 'votes', 'gross_profit', 'description', 'director', 'actors'])

    # Change data types for future analysis
    df_movies[['imdb_rank', 'release_year', 'duration', 'rating', 'metascore', 'votes', 'gross_profit']] \
        = df_movies[['imdb_rank', 'release_year', 'duration', 'rating', 'metascore', 'votes', 'gross_profit']].apply(pd.to_numeric)
    # print(df_movies.info())

    # Convert dataframe to CSV file
    df_movies.to_csv('IMDb_top_movies_new.csv', index=False)


if __name__ == '__main__':
    main()
