# TODO
* Change keys in json to be a yyyy-mm-dd timestamp so Plotly is happy with visualizing it
	* Yearly data timestamps should be [year]-01-01
	* Monthly data timestamps should be [year]-[month]-01
* Change hover tooltip to show messages/days interacted and message recipient
* Change config bar to get rid of unnecessary options
* Scramble names deterministically for privacy during presentation
* Add outlines to datapoints so it's easier to see
* Log scale for Y data
* Possibly scrap:
	* Top X slider: no time and legends allows us to pick top X
	* Change color on hover: seems to be hybrid python/js, no time
	* Stacked bars: too much trace management makes it a nightmare, so no time