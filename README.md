# Weather_Modeling

##Status:
This project is on hold until NOAA fixes the Global Summary of the Day (GSOD)
dataset. It is currently missing nearly all of the data listed in the data
inventory for the regions of interest. NOAA has been notified of the issue.

##Motivation:
To model malaria, you need good data on rainfall and temperature as mosquitoes
breed in standing water and temperature influences the rate at which the
parasite matures. However, there are very few ground based weather stations
in the equatorial African nations which suffer the greatest malaria burden.
The goal of this project is to use machine learning to extrapolate between
weather stations separated by unusually long distances.

##Data Understanding

##Data Preparation
NOAA provides the GSOD data in a proprietary index delimited text file format.
It requires extensive reprocessing before it can be used, including:
  * Converting the data to .csv format.
  * Unpacking columns that contain multiple data points, such as mean
  temperature and the number of hours in the average, into separate columns.
  * Adding machine readable missing data codes to replace hand written entries
  such as "name unknown" or "9999"

##Modeling

##Evaluation


##Next Steps
Once NOAA has released GSOD for the regions of interest, ideally Zambia,
integration of the satellite and elevation data will be completed, the model
will be re-run for both temperature and precipitation estimates, and the
results compared against the accuracy of the relevant satellite data product
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
