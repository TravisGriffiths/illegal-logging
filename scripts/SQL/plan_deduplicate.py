## SQL to deduplicate POA plan data
# Each entry in the POA data has full lat/longs, permits etc. which apply to each species for that permit
# This seperates the data into 2 simpler tables:
# 1. Plan: This is all the high level data, the permits, the plot id, the city, state, lat/longs, dates etc. 
# 2. Harvest: This refernces the Plan, but just has the species and volume targeted 
#
# Each shipment record should have the Plan column added and noted to link the shipment with the plan
# Each shipment record should ALSO have the Harvest ID linked in a column to associate it with the species being shipped. 
# Each harvest record should include columns for sums of volume, and value
#
# NOTES:
# Each entry on the POA plans table is an entry from a particular technician for a species for a permit, 
# These have lots of redundant repeats, most often when the same data is entered by different technicians, but 
# sometimes when the same tech does the same entry mutiple times. 
#
# LAT/LONGS
# These have positive and negative values seemingly at random. As locations in Brazil, the longitude will always be negative
# If any longitude is positive, the sign on the latitude should be flipped. 