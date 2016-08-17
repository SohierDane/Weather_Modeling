# Weather_Modeling

##Status:
This project is on hold until NOAA fixes the Global Summary of the Day (GSOD)
dataset. It is currently missing nearly all of the data listed in NOAA's data
inventory for the regions of interest. I have notified NOAA of the problem.


##Motivation:
To model malaria, you need good data on rainfall and temperature as mosquitoes
breed in standing water and temperature influences the rate at which the
parasite matures. However, there are very few ground based weather stations
in the equatorial African nations which suffer the greatest malaria burden.
NOAA is using machine learning to improve the accuracy of [other weather datasets](https://pmm.nasa.gov/sites/default/files/document_files/IMERG_FinalRun_Day1_release_notes.pdf)
, but will not update historic data for some time yet.
The goal of this project is to use machine learning to extrapolate between
weather stations separated by unusually long distances.  


##Data Understanding
NOAA's metadata for the GSOD turns out to have a very high error rate. Out of the
thirty thousand stations listed in the metadata, approximately 9% are not actually hosted on
the FTP server. This can be easily confirmed by hand for the first three
stations in NOAA's data inventory. An additional 5% of the stations actually
hosted on the FTP website are not listed in the metadata. For an example, see
station 999999-00308. The remaining data for Africa are sparse to the point of being
unusable. For example, exactly one day of data was found for Zambia in the years of interest
for this project (when there is satellite data available) though the metadata show
42 stations active in that timeframe. It will not be possible to achieve the original
project goals until NOAA publishes more complete GSOD data.

As the GSOD ftp server is organized by year rather than by
station these limitations were not apparent until the data had been scraped,
reprocessed, filtered, and aggregated on a per-station basis.

In response to these problems I have:
  * Alerted NOAA to the errors.
  * Contacted the AWS team that manages [Amazon's public GSOD mirror](https://aws.amazon.com/datasets/daily-global-weather-measurements-1929-2009-ncdc-gsod/)
  about hosting a version of GSOD with reprocessed data & corrected metadata
  * Launched a separate project ([easy_GSOD](https://github.com/SohierDane/easy_GSOD))
  focused entirely on providing tools downloading, cleaning, and correcting NOAA's
  raw GSOD data.


##Data Preparation
NOAA provides the GSOD data in a proprietary index delimited text file format.
It requires extensive reprocessing before it can be used, including:
  * Converting the data from .op index delimited format to .csv.
  * Aggregating single years of station data into one file per station.
  * Unpacking columns that contain multiple data points, such as mean
  temperature and the number of hours in the average, into separate columns.
  * Adding machine readable missing data codes to replace hand written entries
  such as "name unknown" or "9999".

Using a random subset of the stations as label stations, I identified the five
 nearest neighboring stations (based on the haversine distance) and
 populated the analytics base table with metrics describing the relationship
between the neighbors and the label station.


##Modeling
Given the lack of data in Africa, I ran the initial tests using a shard of
Australian stations. To mimic the density of African weather stations, I only
included neighbors at least 200 miles from the label station.

I ran several different regression models using sklearn's grid search
cross validation tool: RandomForestRegressor, LinearRegression,
GradientBoostingRegressor, and AdaBoostRegressor.


##Results & Evaluation
|                   | R^2^   | RMSE | MAE  |
|-------------------|-------|------|------|
| Gradient Boost    | 0.954 | 7.2  | 2.05 |
| Linear Regression | 0.913 | 13.6 | 2.82 |
| Random Forest     | 0.903 | 15.1 | 2.96 |
| Ada Boost         | 0.879 | 18.9 | 3.36 |


##Next Steps
Once NOAA has released GSOD for the regions of interest (ideally Zambia):
  * Integrate of the satellite and elevation data.
  * Re-run the model for both temperature and precipitation estimates
  * Compare the results against the accuracy of the relevant satellite data product
(MODIS for temperature, TRMM3B43 for precipitation).


##Running the Model
The codebase is intentionally set up to not run with one click due as some
steps take a very long time to execute but only ever need to be run once.

1. Populate the blank entries in "define_constants_template.py" and use it to
create a .json file. This file includes passwords, so please do not store it
in your git repo.
2. Update the paths in "get_constants.py" to point to the .json from step one.
3. Run "download_gsod". This is will use ~50 gb of storage and will likely
take a few tens of hours to download.
4. Run "prep_grnd_data.py" to unpack the raw gsod data into a machine readable
format, pivot the data to just one file per weather station, and run a station
quality filter.
5. The data are now in usable format. Run "build_weather_predictor.py" to
build, cross validate, and score several candidate models.
