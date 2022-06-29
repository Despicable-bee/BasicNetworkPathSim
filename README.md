# Basic Network Path Sim

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/pic1.jpg"
    width="500px">

## The assignment

During one of my networking assignments, I was given the following basic
    network layout:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00001.PNG" width="600px">

As well as a pair of tables defining the characteristics of the network 
    components (i.e. the supported network `transmission rate`, 
    `propagation delay`, etc).

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00002.PNG"
    width="600px">

I should also mention that all the switches in the global network are 
    `packet switching routers`, however the switches in the local network are all
    `circuit switching routers`.

The point of the assignment was to help us get familiar with network 
    bottlenecks (in preparation for the later sections on 
    **routing algorithms**, and **congestion control**).

## How do I modify the implementation to my needs?

If you look through the `main.py` file, specifically at the `GlobalNetwork` 
    objects' `__init__` method, you'll see the following:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00008.PNG"
    width="600px">

This is essentially a programmatic implementation of pair of tables show above.

The path computer will merely try to deliver packets from a starting point to a
    destination (specified as the first and last index of the path list)

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00009.PNG"
    width="600px">

Hence you can modify the behaviour by first defining your own `nodes` and 
    `links`, and then specify a `path` for them.

If the path computer can't find a link that takes a packet directly to the next
    node, then an exception will be raised.

## Example usage

Hence, you'll probably notice that the `L2` link (described as a satellite
    connection), is very slow (`100kbps`) and is very long (`42,000km`).

A question that best demonstrates this bottleneck is as follows:

> Server S sends a webpage to client C, segmented into 7 packets (each 
>   1000 bytes long).
>
> How long does it take to receive (in ms rounded to 3 decimal places):
> - the FIRST HTTP packet?
> - the SECOND HTTP packet?
> - the LAST HTTP packet?

Which on the diagram draws a path like so:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00007.jpg"
    width="600px">

You could work this out by hand, as many in the course did, but that's error
    prone and slow, not very **PRODUCTIVE** :^).

So why not automate that process using a script and use a few hand calculations
    to verify your implementation?

Well that's exactly what we've done!

## How do I make it go?
1. To make the script go, you should ensure you have the latest version of 
    `matplotlib` (if you're unsure, run the following command)

```
pip3 install --upgrade matplotlib
```

2. `cd` into the directory that has the `main.py` file

3. Then run the following command and you should get some output
```
python3 main.py
```

You should get the following results

```
Question 8 Results -------------------------------------------------------------
Packet 0: 223.572ms
Packet 1: 305.572ms
Packet 2: 387.572ms
Packet 3: 469.572ms
Packet 4: 551.572ms
Packet 5: 633.572ms
Packet 6: 715.572ms
```

## That was pretty underwhelming...

I know right! Lucky for you I've added a `__DEBUG_ENABLE__` option in 
    `NetworkHelper.py` (by default it should be set to `False`).

Setting this to `True` should yield the following:

```
--------- Packet 0 ---------
>>> Node: S

Finished Queue: 0ms, Finished Processing: 0ms, Finished transmission: 0.16ms, Finished Propagation: 0.1603ms

>>> Node: S4

Finished Queue: 0.1603ms, Finished Processing: 0.4103ms, Finished transmission: 0.4903ms, Finished Propagation: 0.4905ms        

>>> Node: S2

Finished Queue: 0.4905ms, Finished Processing: 2.4905ms, Finished transmission: 82.4905ms, Finished Propagation: 222.4905ms     

>>> Node: S1

Finished Queue: 222.4905ms, Finished Processing: 223.4905ms, Finished transmission: 223.5705ms, Finished Propagation: 223.5717ms


--------- Packet 1 ---------
>>> Node: S

Finished Queue: 0.16ms, Finished Processing: 0.16ms, Finished transmission: 0.32ms, Finished Propagation: 0.3203ms

>>> Node: S4

Finished Queue: 0.4903ms, Finished Processing: 0.7403ms, Finished transmission: 0.8203ms, Finished Propagation: 0.8205ms

>>> Node: S2

Finished Queue: 82.4905ms, Finished Processing: 84.4905ms, Finished transmission: 164.4905ms, Finished Propagation: 304.4905ms

>>> Node: S1

Finished Queue: 304.4905ms, Finished Processing: 305.4905ms, Finished transmission: 305.5705ms, Finished Propagation: 305.5717ms

...
```

That's a bit more informative, we can now see at what points each packet leaves
    the various stages of the various nodes.

## It's not colourful enough!
I hear you, good news though, `matplotlib` will show us what we've been missing.

By default you should see the following graph after running `main.py`.

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00003.png">

That's more like it!

We can see right off the bat that only a few colours dominate the delays in the
    path (notably the `S2` switch for obvious reasons).

Zooming in on packets 0 and 1, we see the following:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00004.PNG">

As expected, as soon as `packet 0` finishes transmitting (i.e. `S2_TRANS` 
    finishes), processing of `packet 1` begins immediately (i.e. 
    packet 1 `S2_QUEUE` ends and `S2_PROC` begins).

By now you will also have noiced these weird numbers on the sides:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00005.PNG">

Zooming in on these, we uncover the following:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/NetworkPathSim/00006.PNG">

What we're seeing here is the entire `S4` node block, which just goes to show 
    how much of a bottleneck that satellite connection truely is!