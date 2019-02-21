# TODO
* ~~Change keys in json to be a yyyy-mm-dd timestamp so Plotly is happy with visualizing it~~ (Prashant)
	* ~~Yearly data timestamps should be [year]-01-01~~
	* ~~Monthly data timestamps should be [year]-[month]-01~~
* Change hover tooltip to show messages/days interacted and message recipient (Dennis)
* Change config bar to get rid of unnecessary options (Dennis)
* ~~Scramble names deterministically for privacy during presentation~~ (Prashant)
* ~~Add outlines to datapoints so it's easier to see~~ (Dennis)
* ~~Log scale for Y data~~ (Sebastian)
* ~~Top 10 per year then append together in Global~~ (Sebastian)
* Refactor main generate viz method to one (Sebastian)
* Subplot for barchart? (Sebastian)
* Possibly scrap:
	* Top X slider: no time and legends allows us to pick top X
	* Change color on hover: seems to be hybrid python/js, no time
	* Stacked bars: too much trace management makes it a nightmare, so no time (India)