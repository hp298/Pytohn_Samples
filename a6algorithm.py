"""
Primary algorithm for k-Means clustering

This file contains the Algorithm class for performing k-means clustering.  While it is
the last part of the assignment, it is the heart of the clustering algorithm.  You
need this class to view the complete visualizer.

YOUR NAME(S) AND NETID(S) HERE
DATE COMPLETED HERE
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6checks
import a6dataset
import a6cluster


class Algorithm(object):
    """
    A class to manage and run the k-means algorithm.

    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset which this is a clustering of
        _clusters [list of Cluster]: the clusters in this clustering (not empty)
    """

    # Part A
    def __init__(self, dset, k, seeds=None):
        """
        Initializes the algorithm for the dataset ds, using k clusters.

        If the optional argument seeds is supplied, it will be a list of indices into the
        dataset that specifies which points should be the initial cluster centroids.
        Otherwise, the clusters are initialized by randomly selecting k different points
        from the database to be the cluster centroids.

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter k: the number of clusters
        Precondition: k is an int, 0 < k <= dset.getSize()

        Paramter seeds: the initial cluster indices (OPTIONAL)
        Precondition seeds is None, or a list of k valid indices into dset.
        """
        assert isinstance(dset, a6dataset.Dataset)
        assert type(k) == int and 0 < k <= a6dataset.Dataset.getSize(dset)
        assert seeds == None or (type(seeds) == list and len(seeds) == k)
        self._dataset = dset
        if seeds is None:
            cluster = []
            l = random.sample(a6dataset.Dataset.getContents(dset), k)
            for x in l:
                cluster = cluster + [a6cluster.Cluster(dset, x)]
            self._clusters = cluster
        else:
            cluster = []
            for x in seeds:
                cluster = cluster + [a6cluster.Cluster(dset, a6dataset.Dataset.getPoint(dset,x))]
            self._clusters = cluster

    def getClusters(self):
        """
        Returns the list of clusters in this object.

        This method returns the attribute _clusters directly.  Any changes made to this
        list will modify the set of clusters.
        """
        return self._clusters

    # Part B
    def _nearest(self, point):
        """
        Returns the cluster nearest to point

        This method uses the distance method of each Cluster to compute the distance
        between point and the cluster centroid. It returns the Cluster that is closest.

        Ties are broken in favor of clusters occurring earlier self._clusters.

        Parameter point: The point to compare.
        Precondition: point is a list of numbers (int or float), with the same dimension
        as the dataset.
        """
        assert a6checks.is_point(point)
        assert len(point) == a6dataset.Dataset.getDimension(self._dataset)
        q = self.getClusters()[0]
        min = a6cluster.Cluster.distance(q,point)
        nearest = q
        for x in self.getClusters():
            d = a6cluster.Cluster.distance(x,point)
            if d < min:
                min = d
                nearest = x
        return nearest


    def _partition(self):
        """
        Repartitions the dataset so each point is in exactly one Cluster.
        """
        # First, clear each cluster of its points.  Then, for each point in the
        # dataset, find the nearest cluster and add the point to that cluster.
        for y in range(len(self.getClusters())):
            a6cluster.Cluster.clear(self.getClusters()[y])
        for x in range(len(a6dataset.Dataset.getContents(self._dataset))):
            nearest = self._nearest(a6dataset.Dataset.getPoint(self._dataset,x))
            a6cluster.Cluster.addIndex(nearest,x)


    # Part C
    def _update(self):
        """
        Returns true if all centroids are unchanged after an update; False otherwise.

        This method first updates the centroids of all clusters'.  When it is done, it
        checks whether any of them have changed. It then returns the appropriate value.
        """
        result = True
        for x in self.getClusters():
            tf = a6cluster.Cluster.update(x)
            if tf == False:
                result = False
        return result


    def step(self):
        """
        Returns True if the algorithm converges after one step; False otherwise.

        This method performs one cycle of the k-means algorithm. It then checks if
        the algorithm has converged and returns the appropriate value.
        """
        # In a cycle, we partition the points and then update the means.
        self._partition()
        return self._update()

    # Part D
    def run(self, maxstep):
        """
        Continues clustering until either it converges or maxstep steps
        (which ever comes first).

        This method calls step() repeatedly, up to maxstep times, until the
        algorithm converges. It stops after maxstep iterations even if the
        algorithm has not converged.

        Parameter maxstep: the maximum number of steps to try
        Precondition: maxstep is an int >= 0
        """
        assert type(maxstep) == int and maxstep >= 0
        y = False
        for x in range(maxstep):
            y = self.step()
            if y == True:
                return
