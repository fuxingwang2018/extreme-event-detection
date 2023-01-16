Basic algorithms
=================


Threshold Based Algorithm
-------------------------

**Steps for detection of extreme convective precipitation events from a coarse model (e.g. GCM):**

#. Define a (sub)domain and use daily cr (convective precipitation) from the coarse model
#. Combine the days from the desired period (e.g. a number of years or seasons) in a single dataset
#. Find N-th percentile (crN; e.g. N = 95) of all the data in the dataset
#. For each day, find grid points with cr > crN and add the cr values over these grid points to get cr_sum
#. Select a percentage (e.g. 10%) of the days with the largest cr_sum as the potential events of interest (extreme events) and downscale them


**Explanations:**

 *  Points 1 and 2: daily data is used because hourly data was not available from GCMs
 *  Point 3 finds a single high precipitation value (threshold) for the entire chosen (sub)domain and time period
 *  Point 4: finds high precipitation events at each grid point and day as values larger than the threshold; adds them together to get a single value over the (sub)domain for each day.
 *  Point 5 chooses only those days that have the largest sums of heavy precipitation events


.. note:: Obviously, this approach tends to favour larger-scale systems (except when a single grid point has a very large precipitation amount) because it adds the precipitation at all grid points above the threshold. Simpler approaches than this could be envisaged.

