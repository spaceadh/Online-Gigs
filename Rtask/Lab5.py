# Load libraries
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopy.distance import geodesic

# Set your working directory
path_to_files = "~/Documents/GIGS/Rtask/"

# Part I. Cleanup

# 1. Read in District Areas Shapefile and transform CRS
districts = gpd.read_file(path_to_files + "California_School_District_Areas_2021-22/DistrictAreas2122.shp")
districts = districts.to_crs("EPSG:3310")  # CA Albers Equal Area

# 2. Read in District College Outcomes csv file
college_outcomes = pd.read_csv(path_to_files + "District College Outcomes.csv")
college_outcomes['CDCode'] = college_outcomes['CDCode'].astype(str)
# Calculate CSU rate and UC rate
college_outcomes['CSU_rate'] = college_outcomes['Enrolled CSU (12 Months)'] / college_outcomes['High School Completers']
college_outcomes['UC_rate'] = college_outcomes['Enrolled UC (12 Months)'] / college_outcomes['High School Completers']


# 3. Left join District Areas GeoDataFrame to District College outcomes
districts_college = pd.merge(districts, college_outcomes, left_on='CDCode', right_on='CDCode', how='left')

# Print the column names of the resulting dataframe
# print(districts_college.columns)

# Print the first few rows of the resulting dataframe
# print(districts_college.head())

# 4. Read in college locations csv file and create GeoDataFrame for CSU and UC campuses in LA County
# college_locations = pd.read_csv(path_to_files + "college locations.csv")
# Read in college locations csv file and create GeoDataFrame for CSU and UC campuses in LA County
college_locations = pd.read_csv(path_to_files + "college locations.csv", encoding='latin1')
# print(college_locations.columns)
college_locations['geometry'] = [Point(x, y) for x, y in zip(college_locations['LONGITUD'], college_locations['LATITUDE'])]
college_locations = gpd.GeoDataFrame(college_locations, crs="EPSG:4326")

# Check if 'Los Angeles' is present in the CITY column
print('Los Angeles' in college_locations['CITY'].values)

# Verify latitude and longitude coordinates
print(college_locations[['LONGITUD', 'LATITUDE']].head())

# Filter CSU campuses in Los Angeles County based on college_outcomes DataFrame
CSU_LA = college_outcomes[(college_outcomes['CSU_rate'].notnull()) & (districts_college['CountyName_x'] == 'Los Angeles')]

# Filter UC campuses in Los Angeles County based on college_locations DataFrame
UC_LA = college_outcomes[(college_outcomes['UC_rate'].notnull()) & (districts_college['CountyName_x'] == 'Los Angeles')]

print("CSU Campuses in Los Angeles County:")
print(CSU_LA)

print("\nUC Campuses in Los Angeles County:")
print(UC_LA)

# Check if the 'geometry' column is present in CSU_LA after filtering
print('geometry' in CSU_LA.columns)

# Print data types of columns in college_locations
print(college_locations.dtypes)
# Part II. Analysis

# 1. Create map of CSU going rates for districts in Los Angeles County
fig, ax = plt.subplots(figsize=(10, 8))
districts_college[districts_college['CountyName_x'] == 'Los Angeles'].plot(column='CSU_rate', cmap='RdYlGn', edgecolor='black', legend=True, ax=ax)
CSU_LA.plot(ax=ax, color='red', markersize=50)
plt.title("CSU Going Rates for Districts in Los Angeles County")
plt.show()

# 2. Create map of UC going rates for districts in Los Angeles County
fig, ax = plt.subplots(figsize=(10, 8))
districts_college[districts_college['CountyName_x'] == 'Los Angeles'].plot(column='UC_rate', cmap='RdYlGn', edgecolor='black', legend=True, ax=ax)
UC_LA.plot(ax=ax, color='blue', markersize=50)
plt.title("UC Going Rates for Districts in Los Angeles County")
plt.show()

# 3. Discussion of relationship between college proximity and going rates
# This can be done by analyzing the maps and discussing the patterns observed.

# 4. Calculate distances between school district centroids and CSU's in LA county
# Compute average distance by school district
# Compute average distance by school district
avg_distances = []
# print(CSU_LA.columns)
# Print column names and inspect for the presence of the geometry column
# print(college_locations.columns)

# Check if the geometry column is present
print('geometry' in college_locations.columns)

# # Compute average distance by school district
# avg_distances = []
# for district in districts_college[districts_college['CountyName_x'] == 'Los Angeles'].iterrows():
#     district_geometry = district[1]['geometry']
#     district_centroid = district_geometry.centroid.coords[0]  # Get centroid coordinates
#     distances = []
#     for campus_geometry in CSU_LA['geometry']:
#         campus_coords = campus_geometry.centroid.coords[0]  # Get campus centroid coordinates
#         distance = geodesic(district_centroid, campus_coords).kilometers  # Compute distance
#         distances.append(distance)
#     avg_distance = sum(distances) / len(distances)
#     avg_distances.append(avg_distance)

avg_distances_df = pd.DataFrame({'School_District': districts_college[districts_college['CountyName_x'] == 'Los Angeles']['DistrictName']})
# print(avg_distances_df.columns)
# print(college_outcomes.columns)
# # Compare with CSU going rate
# # Compare with CSU going rate
# avg_distances_df = pd.merge(avg_distances_df, 
# college_outcomes[['DistrictName', 'CSU_rate']],
#  left_on='DistrictName', 
#  right_on='DistrictName', 
#  how='left')

# # Compare with UC going rate
# avg_distances_df = pd.merge(avg_distances_df, college_outcomes[['UC_rate']])
combined_df = pd.concat([avg_distances_df, college_outcomes[['UC_rate']]], axis=0)

combined_df = pd.concat([combined_df, college_outcomes[['CSU_rate']]], axis=0)

# 5. Create one additional visualization related to college going rates
# This can be done based on the specific data and analysis objectives.
print(combined_df.columns)
# For example, you could create a bar plot of CSU going rates by school district
plt.figure(figsize=(12, 6))
plt.bar(avg_distances_df['School_District'], avg_distances_df['CSU_rate'], color='skyblue')
plt.xticks(rotation=90)
plt.xlabel('School District')
plt.ylabel('CSU Rate')
plt.title('CSU Going Rates by School District')
plt.show()