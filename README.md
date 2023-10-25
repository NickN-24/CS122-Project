# Movie Rating Analyzer

**Authors** : Victoria Le,  Nick Nguyen

### Project Description

This project acts as a database, allowing users to search up information relating to movies. It will take information from multiple sites (ie. Letterboxd, IMDb) and combine the data into a single space. Information such as the rating, year it was made, length of the movie, etc. can all be combined in one area. The user score, however, will be averaged across all sites. The main movie description shown will be from the website with the highest score for that movie, however, users can check the other descriptions by clicking on icons representing the other sites.

## Project Plans and Outline

### Interface

A simple search bar, with a dropdown menu for filtering. Filters include year, rating, score and genres. To make sure we don't get rate limited, only the first three items of a site are shown. The user can change what the main site is from a selection.

Each item will only show it's title, year, rating, score and image. Clicking on it expands it, showing the length, genres and description. Extra icons will be added for each site, allowing users to hover over them and see each sites individual description and rating.

### Data Collection/Storage

We will collect data from the following websites:
- [Letterboxd](https://letterboxd.com/)
- [Rotten Tomatoes](https://www.rottentomatoes.com/)
- [IMDb](https://www.imdb.com/)

As many of the official APIs for the websites are not available for public use or require subscriptions, we will make use of the Beautiful Soup Python package for web scraping and acquiring movie ratings. Data will be collected and stored in a spreadsheet for analysis.

### Data Analysis and Visualization

Movie scores will be analyzed and averaged through the usage of Python's numpy package. This project contains a visualization component that will generate a bar graph displaying the different ratings from each website. 
