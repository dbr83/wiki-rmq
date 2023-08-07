# Case study Wikipedia edits

## Setup

### Packages to install

- linux
- docker version > 19
- docker compose

## Steps to run

- clone git repository
- enter directory
- run docker-compose up

An output file will be created in the output directory containing the edit rate

## Further questions

### What would be a possible database to store the data? (Advantages disadvantages)
InfluxDb as a time series database could be a good fit for storing this data. It contains also aggregation functionality allowing different representations also on stored data like the required aggregations in this case study. 

Alternatively it could be stored in a normal relational database although the schema had to be created for this data and also this is quite uncommon and disadvantageous to do since change in data would be require schema adaptions, so using a database like postgres would not work well. Also it operates over rows than columns.

A nosql database is be a better fit for the data since it allows flexible data structures compared to relational databases.

### Which data model do you think would be useful for storing the events?
A time series databases that can operate over columns. Aggregating over columns is more efficient in this case as we deal with lots of data.

### Which exchange model would make sense? Describe the pros/cons of your chosen exchange in terms of scalability and fault tolerance.
In this case study I chose direct exchange because we have only one consumer.
If the message should be available to multiple consumers without using a routing key and without using persistence to increase performance.
