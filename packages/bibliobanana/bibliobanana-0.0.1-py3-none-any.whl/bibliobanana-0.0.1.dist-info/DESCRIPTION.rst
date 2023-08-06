# Bibliographic banana for scale

If you're an academic, there's a big chance you've seen a graph of the yearly 
number of publications on a topic. This will likely have shown an increase, 
on the basis of which the writer concluded the topic was gaining in 
popularity. This, in short, was likely nonsense.

Academic research is ever expanding, and thus any visualisation of the number 
of publications on topic X will look like there is an increased interest in X. 
The solution is to normalise publication rates against the outputs of a whole 
discipline, but doing so can be very hard and require a lot of work.

The **bibliobanana** Python package can be used to more accurately quantify 
changes in academic interest. It comes with the following features:

- Loading bibliometric data from PubMed or Google Scholar on any topic

- Normalising publication rates on one or more keywords of interest with one or a collection of reference keywords.

- Storing bibliographic data in neatly organised text files.

- Plotting the raw, normalised, or max-scaled publication rates.



## Installation

**Option 1: Installing from the command line**
0) Make sure you have a running Python 3 installation.
1) Open a terminal (Linux or Mac OS X) or a command prompt (Windows)
2) Run the following command: `pip install bibliobanana`

**Option 2: Installing from Python**
1) Open Python.
2) Run the following commands:

```python
import pip
pip.main(["install", "bibliobanana"])
```

For example, please see: https://github.com/esdalmaijer/bibliobanana

