Concept:

________________________________________________________________________________________________________________________________________

DATA:

I extract all the data from the files (addresses_for_task.csv and Counties.geojson) and townlands data via an API,
________________________________________________________________________________________________________________________________________

FILTERING DATA:

Firstly I split the address and initially assume that the last element of the list is the county name. I filter the
townlands file on that county name to reduce the data that would be required to later match the other remaining elements
of the address list, if in case this element does not match with any county name from the townlands list then the entire
list gets assigned for the same matching purpose. The townland filtered list remains unchanged while iterating over the
addresses_for_task file while the last element of the address list ( county name ) remains the same i.e we would not need
to filter the townlands file again and again if there are 5 iterations for county dublin. This will save a lot of time.

Now since the address starts from "Road or Local Area Name" (small area) to "county name" (large area). SO, taking the
remaining elements of address_list from left to right from the address list, would help with the faster retrieval of the
closest address to the required GPS co-ordinates.

Then once I get the closest address I just convert the ITM_N and ITM_E to the EPSG:4326 format using proj library.

________________________________________________________________________________________________________________________________________

Advantages:

1) Not having to filter the townlands list again and again for the county name would help in saving a lot of time.
If two or more consecutive iterations from the address_for_task.csv have the same county name, then the code will
just work with the previously filtered townlands list.

2) Once the townlands list is filtered then iterating over the address list(each address_for_task.csv entry) and using
the values from "Road or Local Area Name" (small area) to "county name" (large area) will help us get to the closest
posiisble co-ordinate faster.

3) The Counties.geojason file has been saved locally, so, it will help with faster and latancy free data retrival.

4) if we use both ways of getting the dataset i.e. API and local file then we try 2 ways of getting the data. If one fails
then other way might work

________________________________________________________________________________________________________________________________________

Disadvantages:

1) Using the API for getting the dataset means if there is any network issue then the code will not work.

2) Saving a small file locally is fine but as the dataset grows then it can use a lot of system storage.

