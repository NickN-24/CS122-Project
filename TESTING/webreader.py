import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def scrape_top50(year, items=50) :
    url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={year}-01-01,{year}-12-31&sort=user_rating,desc&num_votes=50000,"
    headers = {"user-agent": "my-agent/1.0.1"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    li_elements = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-423b7cdc-0 eHyIPG detailed-list-view ipc-metadata-list--base", role="presentation").find_all("li")
    
    data = list()
    for li in li_elements[:items] :
        print(items)
        items-=1
        data.append(fetch_movie_data(year, li, headers))
    return np.array(data, [("Year", "i"), ("Title", "O"), ("Score", "f"),
                           ("Image", "O"), ("Time", "i"), ("Rating", "O"),
                           ("Genres", "O"), ("Description", "O")])

def fetch_movie_data(year, li_element, headers) :
    li = li_element.find_all("div", recursive=True)

    title = re.sub(r"^\d+\.\s", "", li[11].text)
    # print(f"Title : {title}")
    score = li[13].text.split()[0]
    # print(f"Score : {score}")
    image = li[8].find('img')['src']
    # print(f"Image : {image}")
    tr = li[12].find_all("span")
    time, rating = None, None
    if len(tr)>1 :
        time = li[12].find_all("span")[1].text
    # print(f"Time : {time}")
    if len(tr)>2 :
        rating = li[12].find_all("span")[2].text
    # print(f"Rating : {rating}")

    genre_url = "https://www.imdb.com"+li[11].find('a', class_="ipc-title-link-wrapper")['href']
    # print(f"Genre URL : {genre_url}")
    genre_response = requests.get(genre_url, headers=headers)
    genre_soup = BeautifulSoup(genre_response.text, "html.parser")

    genres = [str(g.text) for g in genre_soup.find_all("a", class_="ipc-chip ipc-chip--on-baseAlt")]
    # print(f"Genres : {' '.join(genres)}")

    description_url = genre_url.split("?")[0]+"plotsummary"
    # print(f"Decription URL : {description_url}")
    description_response = requests.get(description_url, headers=headers)
    description_soup = BeautifulSoup(description_response.text, "html.parser")

    description = description_soup.find("li", class_="ipc-metadata-list__item").text
    # print(f"Description : {description}")

    return (year, title, score, image, convert_to_minutes(time), rating, genres, description)

def convert_to_minutes(time_str):
    hours = re.search(r'(\d+)h', time_str)
    minutes = re.search(r'(\d+)m', time_str)

    hours = int(hours.group(1)) if hours else 0
    minutes = int(minutes.group(1)) if minutes else 0

    return hours * 60 + minutes

# if __name__ == "__main__" :
#     url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2010-01-01,2010-12-31&sort=user_rating,desc&num_votes=50000,"
#     data = scrape_top50(url, 5)
#     print(data)
    