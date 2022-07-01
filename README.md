# Big Data Technologies project - 2022

**Assignment**: Design and implement a big data system for automatically building and maintaining a ranking of European cities in terms of quality of life.

Various factors influence the quality of life of a city. Air Quality Index is one of those factors. The cleaner the air is the more livable the city is. For this project, however, we make us of only AQI (Air Quality Index) as the considering factor to decide quality of life of cities. The reason behind this being the key area of focus on the big data pipeline. 

The image here shows the entire pipeline of the project.

![BigDataProject_Pipeline (1)-1](https://user-images.githubusercontent.com/20270507/176953286-c5af4b7a-9c0d-453c-9d92-271a14e4b3e5.jpg)


At first the names of all European cities are gathered. The cities information is handled using a URL schema. A publisher send these to several channels & we have listeners who manage to transform the URLs into proper requests, whose responses are stored into a document database. 

We prefered to use NoSQL, because of the flexibility offered by a NoSQL database. AQI values are expected to be integers, but in some cases missing values (recorded as ‘-’) are sent back. MongoDB allows handling these exceptions easily. In the perspective of further development, a NoSQL database is suggested, since it is easy to modify the structure of the data. 

From the database then, the data is queried and displayed on a webpage that refreshes every minute to ensure availability of most updated information to the potential viewer. 
