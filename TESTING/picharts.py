import matplotlib.pyplot as plt
import numpy as np
import pickle
import webreader


if __name__ == "__main__" :
    year = 2011
    data = webreader.scrape_top50(year, 50)

    with open(f"{year}_movies.pickle", "wb") as f:
        pickle.dump(data, f)

    all_genres = [genre for genres_list in data["Genres"] for genre in genres_list]
    unique_genres, genre_counts = np.unique(all_genres, return_counts=True)

    plt.pie(genre_counts, labels=unique_genres, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Distribution of Genres')
    plt.show()