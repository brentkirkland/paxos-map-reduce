# PRM

Paxos and Map Reduce. This was tested on Google App Engine and worked nicely.

# Paxos

From [wikipedia](https://en.wikipedia.org/wiki/Paxos_(computer_science)), Paxos is a family of protocols for solving consensus in a network of unreliable processors. Consensus is the process of agreeing on one result among a group of participants. This problem becomes difficult when the participants or their communication medium may experience failures.

# Map Reduce

From [wikipedia](https://en.wikipedia.org/wiki/MapReduce), MapReduce is a programming model and an associated implementation for processing and generating big data sets with a parallel, distributed algorithm on a cluster.

## Config.txt

The config file contains the ip address of each machine. Replace each ip with `127.0.0.1` if you would like to test it locally.

## How to run:

First terminal:

`python run.py 1`

Second terminal:

`python run.py 2`

Third terminal:

`python run.py 3`

You then enter commands into each terminal. Sorry if the formatting may be wonky.

## Completed Commands

* map
* reduce
* replicate
* reduce
* stop
* resume
* total
* print
* merge

NOTE: This was a school project for a distributed systems project. There may be edge cases that were not tested. This should be used as a starting point in learning how these two algorithms can work together.
