# PEMS API

This tiny python package provides an API for Caltrans Performance Measurement System (PeMS).

The traffic data is collected in real-time from over 39,000 individual detectors. 
These sensors span the freeway system across all major metropolitan areas of the State of California.
PeMS is also an Archived Data User Service (ADUS) that provides over ten years of data for historical analysis. 
It integrates a wide variety of information from Caltrans and other local agency systems including:
* Traffic Detectors
* Incidents
* Lane Closures
* Toll Tags
* Census Traffic Counts
* Vehicle Classification
* Weight-In-Motion
* Roadway Inventory

To use this API,[ you must apply for an account](http://pems.dot.ca.gov/?dnode=apply). 
Registering only takes a few minutes. 
Accounts are typically approved within one to two business days.

**Be careful! The original site doesn't use a secured communication channel (https), so use a unique password!!!**

You find the original website [here](http://pems.dot.ca.gov).

At this moment pems_api supports the following data sources:
* Station meta information ([description](http://pems.dot.ca.gov/?dnode=Clearinghouse&type=meta&district_id=3&submit=Submit)): use `StationMetaDataHandler`
* Raw station data ([description](http://pems.dot.ca.gov/?dnode=Clearinghouse&type=station_raw&district_id=3&submit=Submit)): use `StationRawDataHandler`
* 5mins aggregated station data: use `Station5MinDataHandler`
* Baleset adatok ([description](http://pems.dot.ca.gov/?dnode=Clearinghouse&type=chp_incidents_day&district_id=all&submit=Submit)): use `CHPDailyIncidentDataHandler`


## Installation

You can install pems_api via pip:

```bash
pip3 install pems_api
```


## Usage

The usage pattern is the same as below for all the Datahandlers:

```python
import pems_api as pa
import pandas as pd

# Login to http://pems.dot.ca.gov
pa.PeMSConnection.initialize("<username>", "<password>")

# Initializing a data handler
data_handler = pa.Station5MinDataHandler()


# Defining a start date, end date and a district_id
start_date, end_date, district_id = date(2016, 3, 1), date(2016, 3, 5), 3

# Downloading data between start date and end date from the 3rd district
data_chunks = dh.load_between(from_date=start_date, to_date=end_date, district=5)

```
The data_chunks will be a generator object, in which each data chunk is a pandas DataFrame.
We use generator because the long time intervals are too big to hold them in the memory at the same time.
If you are not familiar with generators please check [this tutorial](https://wiki.python.org/moin/Generators).

If you want to concatenate the data chunks we recommend the following method:

```python
df = pd.concat([data for data in data_chunks])
df.head()

```



