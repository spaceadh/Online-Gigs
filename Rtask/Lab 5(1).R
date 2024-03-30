# Load libraries
library(sf)
library(tidyverse)

# Set your working directory
setwd("~/Documents/GIGS/Rtask")

# Part I. Cleanup

# 1. Read in District Areas Shapefile and transform CRS
districts <- st_read("California_School_District_Areas_2021-22/DistrictAreas2122.shp") %>%
  st_transform(crs = "+proj=aea +lat_1=34 +lat_2=40.5 +lon_0=-120 +x_0=0 +y_0=-4000000 +datum=NAD83 +units=m +no_defs")

# 2. Read in District College Outcomes csv file
college_outcomes <- read_csv("District College Outcomes.csv") %>%
  mutate(CDCode = as.character(CDCode),
         CSU_rate = CSU / TotalStudents,
         UC_rate = UC / TotalStudents)

# 3. Left join District Areas sf object to District College outcomes
districts_college <- left_join(districts, college_outcomes, by = "CDCode")

# 4. Read in college locations csv file and create sf objects for CSU and UC campuses in LA County
college_locations <- read_csv("college locations.csv") %>%
  st_as_sf(coords = c("Longitude", "Latitude"), crs = 4326) %>%
  st_transform(crs = st_crs(districts))

CSU_LA <- college_locations %>%
  filter(System == "CSU", County == "Los Angeles")

UC_LA <- college_locations %>%
  filter(System == "UC", County == "Los Angeles")

# Part II. Analysis

# 1. Create map of CSU going rates for districts in Los Angeles County
ggplot() +
  geom_sf(data = districts_college %>% filter(County == "Los Angeles"), aes(fill = CSU_rate)) +
  geom_sf(data = CSU_LA, color = "black", size = 2) +
  scale_fill_gradient(low = "red", high = "green") +
  labs(title = "CSU Going Rates for Districts in Los Angeles County", fill = "CSU Rate")

# 2. Create map of UC going rates for districts in Los Angeles County
ggplot() +
  geom_sf(data = districts_college %>% filter(County == "Los Angeles"), aes(fill = UC_rate)) +
  geom_sf(data = UC_LA, color = "black", size = 2) +
  scale_fill_gradient(low = "red", high = "green") +
  labs(title = "UC Going Rates for Districts in Los Angeles County", fill = "UC Rate")

# 3. Discussion of relationship between college proximity and going rates
# This can be done by analyzing the maps and discussing the patterns observed.

# 4. Calculate distances between school district centroids and CSU's in LA county
distances <- st_distance(districts_college %>% filter(County == "Los Angeles"), CSU_LA)

# Compute average distance by school district
avg_distances <- tibble(
  School_District = districts_college$DistrictName,
  Average_Distance = sapply(distances, mean)
)

# Compare with CSU going rate
avg_distances <- left_join(avg_distances, college_outcomes %>% select(DistrictName, CSU_rate), by = "School_District")

# 5. Create one additional visualization related to college going rates
# This can be done based on the specific data and analysis objectives.

# For example, you could create a bar plot of CSU going rates by school district
ggplot(college_outcomes, aes(x = reorder(DistrictName, CSU_rate), y = CSU_rate)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
  labs(title = "CSU Going Rates by School District", x = "School District", y = "CSU Rate")