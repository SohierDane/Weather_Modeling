# Weather_Modeling

##Status:
This project is on hold until NOAA fixes the Global Summary of the Day (GSOD)
dataset. It is currently missing nearly all of the data listed in NOAA's data
inventory for the regions of interest. NOAA has been notified of the issue.

##Motivation:
To model malaria, you need good data on rainfall and temperature as mosquitoes
breed in standing water and temperature influences the rate at which the
parasite matures. However, there are very few ground based weather stations
in the equatorial African nations which suffer the greatest malaria burden.
NOAA is using
machine learning to improve the accuracy of [other weather datasets](https://pmm.nasa.gov/sites/default/files/document_files/IMERG_FinalRun_Day1_release_notes.pdf)
, but will not update historic data for some time yet.
The goal of this project is to use machine learning to extrapolate between
weather stations separated by unusually long distances.  

##Data Understanding
NOAA's metadata for the GSOD turns out to have a very high error rate. Out of the
thirty thousand stations listed in the metadata, approximately 9% are not actually hosted on
the FTP server. This can be easily confirmed by hand for the first three
stations in NOAA's data inventory. An additional 5% of the stations actually
hosted on the FTP website are not listed in the metadata. For an example, see
station 999999-00308. The remaining data for Africa are extremely sparse.
For example, exactly one day of data was found for Zambia in the years of interest
for this project (when there is satellite data available) though the metadata show
42 stations each active for several years.

Unfortunately, as the GSOD ftp server is organized by year rather than by
station these limitations were not apparent until the data had been scraped,
reprocessed, filtered, and aggregated on a per-station basis.  


##Data Preparation
NOAA provides the GSOD data in a proprietary index delimited text file format.
It requires extensive reprocessing before it can be used, including:
  * Converting the data to .csv format.
  * Aggregating single years of station data into one file per station.
  * Unpacking columns that contain multiple data points, such as mean
  temperature and the number of hours in the average, into separate columns.
  * Adding machine readable missing data codes to replace hand written entries
  such as "name unknown" or "9999".

##Modeling

##Evaluation


##Next Steps
Once NOAA has released GSOD for the regions of interest (ideally Zambia):
  * Integration of the satellite and elevation data will be completed
  * The model will be re-run for both temperature and precipitation estimates
  * The new results will compared against the accuracy of the relevant satellite data product
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
