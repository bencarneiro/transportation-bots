# transportation-bots

This repo contains, among other things, an open source data visualization tool built around timeseries datasets from the National Transit Database. The tool lets the user explore any public transportation spending in the USA since 1991. 

The tool is up in a Beta at http://transit.observer

Give it a try and leave some feedback

![Screenshot from 2023-05-09 19-41-35](https://github.com/bencarneiro/transportation-bots/assets/63479105/5165020f-5822-44bd-8bd7-cae027a481d0)

# other stuff

THIS REPO also contains some twitter bots (but on mastodon)

This is a robot which takes real time traffic reports from the City of Austin Open Data Portal (https://data.austintexas.gov/Transportation-and-Mobility/Real-Time-Traffic-Incident-Reports/dx9v-zd7x)
And posts them with a picture of the intersection, and a link to the intersection on google maps. 

Built using Django // A Linode // Crontab // A Bash script


![Screenshot from 2023-04-14 09-46-20](https://user-images.githubusercontent.com/63479105/232082372-0aa54021-fd30-4d77-a241-c2a495ff3de1.png)

https://mastodon.social/@austin_traffic_bot

OK UPDATE 4/20:

This repo also now contains a lot of ETL code for NTD expenses timeseries, and performance timeseries as well. I'll eventually use this repo to build and API / site for visualizing transit data
