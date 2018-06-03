EMBI dataset analysis
=====================

Author: Gregorio Flores

Home Page: [github](https://github.com/bygregonline/)

**Keywords:** python3 pandas pyramid matplotlib webservice

**Whats is EMBI** The JPMorgan Emerging Market Bond Index (EMBI) are a set of three bond indices to track bonds in emerging markets operated by J P Morgan. The indices are the Emerging Markets Bond Index Plus, the Emerging Markets Bond Index Global and the Emerging Markets Bond Global Diversified Index.

The index comprises a set of broker-traded debt instruments widely followed and quoted by several market makers.

In other words The JPMorgan Emerging Market Bond Index (EMBI). Weighs the country risk of all emerging markets.

**Categories**

1.	developers
2.	traders
3.	data scientific
4.	nerds
5.	technology enthusiasts
6.	python developers
7.	Data financial analysts

**What does this code do**

1.	Runs a webservice
2.	Convert raw data into CSV, JSON, XML JSON, HTML and generates real time binary streams as PICKLES and excel format
3.	Generate automatic forecasting data from CSV time series.
4.	The full forecast can be downloaded using CSV, JSON, XML JSON, HTML, serialized and excel format
5.	The data can be displayed using the maplotlib direct into your browser.

**How does it work**

Read all EMBI Time series from a csv file Calculate the full correlation data between all countries Render charts as JPEG and PNG formats send correlation dataset as CSV, JSON, XML JSON, HTML and other binary formats.

TODO, Finish documentation

**Normalized datasets**

THE normalized values allow the comparison of corresponding normalized data for different datasets in a way that eliminates the effects of certain gross influences, as in an anomaly time series. In other words normalized dataset provides the tools to compare apples with apples and orange with oranges()

**Description**

TODO FIX this documentation

**Python Version**

3.5 or above

**How to install**

<pre>pip  install argparse termcolor  numpy pandas pypng  pyramid-jinja2   pyramid  openpyxl setuptools py-common-fetch Prophet matplotlib
</pre>

**Download**<pre> git clone https://github.com/bygregonline/forecasting.git</pre>

**HOW TO RUN**<pre> python runwebapp.py</pre>

**Go to your local address port 8080 (default)**

![Image](https://raw.githubusercontent.com/bygregonline/JP_morgan_EMBI_NORMALIZED/master/images/image5.png)

**Parametrize the web service**

![Image](https://raw.githubusercontent.com/bygregonline/JP_morgan_EMBI_NORMALIZED/master/images/image1.png)

**Get normalized dataset charts with mean 0 and variance 1**

![Image](https://raw.githubusercontent.com/bygregonline/JP_morgan_EMBI_NORMALIZED/master/images/image4.png)

\**If something goes wrong. A very friendly and useful web page will be displayed. \*\*

![error page](https://raw.githubusercontent.com/bygregonline/JP_morgan_EMBI_NORMALIZED/master/images/error.png)

\**vous pouvez faire ce que vous voulez de ce truc. Si on se rencontre un jour et que vous pensez que ce truc vaut le coup, vous pouvez me payer une bière en retour. Your friend Greg flores *\*
