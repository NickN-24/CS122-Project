# Movie Trends Analyzer

**Authors** : Victoria Le,  Nick Nguyen

### Project Description

This project will save information from two popular movie rating sites (RottenTomatoes and IMDB) to figure out a trend in popular movies. The top 30 movies of the year will be saved to a database, where users can graphically compare aspects of a movie to it's popularity. These aspects contain data such as the director, studio, genre and length of the movie. Unwanted aspects can be filtered out. A line chart with respect to time is used to represent this data, with higher values representing its average popularity.

## Project Plans

### Outline

#### Main

- [ ] Design a csv file (what are the headers)
- [ ] Properly save web data into the csv
    - [ ] Save data from RottenTomatoes from 2010-current
    - [ ] Save data from IMDb from 2010-current
- [ ] Design a simple homepage
    - [ ] Header with project title and github link
    - [ ] Description of the website
    - [ ] Button to move on to the analyzing page
- [ ] Design an analytics page
    - [ ] Header with project title and github link
    - [ ] Add a button to update/reset data
    - [ ] Slot for an image
    - [ ] Selection bar to select an aspect (drop down menu?)
    - [ ] Aspect filtering system for the graph (side bar?)
- [ ] Display graphs for the data
    - [ ] Allow users to change what aspect is being graphed
    - [ ] Allow users to filter the aspects


#### Extra
- [ ] Recommendation system based on highest rating (bonuses if a movie shows up in multiple year)
- [ ] Allow users to save a graph in some format, to compare it with other graphs
- [ ] A download button to get a csv containing ONLY the data shown in the graph
- [ ] A method to estimate the popularity of a movie based on inputted aspects
- [ ] Show the two most popular movie of the latest year (if any data) on the home page
    - [ ] Save/Display the image for each movie as well

### Interface

TODO

### Data Collection/Storage

We will collect data from the following websites:
- [Rotten Tomatoes](https://www.rottentomatoes.com/)
- [IMDb](https://www.imdb.com/)

As many of the official APIs for the websites are not available for public use or require subscriptions, we will make use of the Beautiful Soup Python package for web scraping and acquiring movie information.

Data will be collected and stored as a csv file, denoting the movie title, year, rating, and the rest of it's aspects. When saving data, it will only save from the last year in the csv to the current year. Any data that is read will be appended to the end of the file. A button to reset the data file will be provided.

### Data Analysis and Visualization

TODO