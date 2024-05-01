# Finding closest pairs of coordinates from two arrays

The purpose of this project is to demonstrate an effective, optimized approach for point distance matching across two arrays. 

In one of my previous roles, I encountered a problem where for a list of tens of thousands of locations, I needed to find the nearest location to it from another list with thousands of potential matches (using latitude and longitude)

Initially, I used a k-nearest neighbors pairwise approach to find the distance of every location to every other location and keep the smallest distance for each one. But with over 10,000 locations in each list, this brute force method (O(n<sup>2</sup>)) took several hours (and Gb of memory) to run.

After some additional research, I was able to optimize my approach to run in under 1 minute by utilizing a Ball Tree Algorithm.
A Ball Tree works by partitioning the space of the training data (in this case 2-dimensional) into circular blocks (balls) and compares each point only to nearby points to find the closest.

Using a US housing dataset and a list of all Starbucks locations in the US, I've recreated this problem using both approaches in the k_nearest_neighbors.ipynb file.

## Finding the Closest Starbucks to Houses in the US

What's the fastest way to find the closest Starbucks to any house in the US?

**Runtime to find the closest Starbucks to each house using brute force?** 20 minutes 24 seconds.

**Runtime using the Ball Tree?** 1.44 seconds!

**Average distance to a Starbucks from over 27,000 houses in the US?** 8.15 miles :)
