import numpy as np
from scipy.spatial import ConvexHull


def farthest_points_2d(points):
    """
    Given an Nx2 array 'points' (in 2D), returns the pair of points
    that are farthest apart and their distance.
    """
    # Compute the convex hull via SciPy (O(n log n))
    hull = ConvexHull(points)

    # Extract the hull vertices (in counterclockwise order)
    hull_points = points[hull.vertices]
    h = len(hull_points)

    # A helper function for squared Euclidean distance
    def squared_dist(a, b):
        return np.sum((a - b) ** 2)

    # Edge case: if the hull has only 1 or 2 points, handle directly
    if h == 1:
        return (hull_points[0], hull_points[0], 0.0)
    if h == 2:
        dist = np.sqrt(squared_dist(hull_points[0], hull_points[1]))
        return (hull_points[0], hull_points[1], dist)

    # Rotating calipers initialization
    # We'll track the largest distance found
    max_sqdist = 0
    best_pair = (0, 1)

    # j starts at 1 for i=0
    j = 1

    # Main rotating calipers loop (O(h))
    for i in range(h):
        # Move j while the 'area check' indicates we can rotate further
        # Next index in cyclical manner
        while True:
            # Current cross product
            cross_current = np.cross(
                hull_points[(i + 1) % h] - hull_points[i],
                hull_points[(j + 1) % h] - hull_points[i]
            )
            # Previous cross product
            cross_previous = np.cross(
                hull_points[(i + 1) % h] - hull_points[i],
                hull_points[j] - hull_points[i]
            )
            if cross_current > cross_previous:
                j = (j + 1) % h
            else:
                break

        # Update maximum distance with the current pair (i, j)
        cur_sqdist = squared_dist(hull_points[i], hull_points[j])
        if cur_sqdist > max_sqdist:
            max_sqdist = cur_sqdist
            best_pair = (i, j)

    # Get the actual distance and points
    p1, p2 = hull_points[best_pair[0]], hull_points[best_pair[1]]
    max_dist = np.sqrt(max_sqdist)

    return p1, p2, max_dist

# if __name__ == '__main__':
#     import time
#     t1 = time.time()
#     n = 10000
#     for _ in range(n):
#         points = np.random.rand(100, 2)
#         farthest_points_2d(points)
#     t2 = time.time()
#     print("Time per calculation: {:.6f} ms".format((t2 - t1) * 1000 / n))
