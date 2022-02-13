## Alpha Spectroscopy
#phy535

1. Adjust the distance between the source stage and the silicon detector to be somewhat larger than 3.5 cm. 

To do this I had to evacuate the chamber with two valves and wait for it to equalize ~$745$ torr. While it was open I measured

| Implement | Length (mm) |
| --- | --- |
| Detector | $14\pm 2$ |
| Source | $54 \pm 2$ |
| Detector diameter | $13 \pm 0.5 mm$ |

2. Apply $+30V$ to the detector bias over the course of 60s, connect the energy line to the oscilloscope. I had to adjust the trigger to see anything. 

Directly from the preamplifier, the oscilloscope creates peaks of heigh less than $100mV$, with a width of $ ~100\mu s $.

These are the peaks that I should replicate using the function generator. 

3. Using the amplifier, and a course shaping of $6\mu s$ the peaks look gaussian. I forgot to measure the width. I should probably look at the FWHM

## Analysis

 - `curie.ipynb` contains details on the calculation of the radioactivity of the ${}^{210}Po$ sample in the lab.
> The measured radioactivity of our sample is $0.1085 \pm 0.0018$ µci, note [this posting](https://www.pasco.com/products/lab-apparatus/atomic-and-nuclear/sn-9085) which sells them in $0.1$ µci samples.
 - `cal.py` only contains a function which converts MCA signals into calibration curves. Calibration curves were compared for different days and found to be effectively the same.
   - see `calibration.ipynb` for the derivation of these functions
   > `cal.E(channel: int)` converts channels to energy 
   
   > `cal.σ(channel: int)` returns the standard deviation of the Energy associated with a channel. These values are very small, but I kept them for good measure.
 - `Bragg.ipynb` details the calculation of the average slope of the Pressure v Peak Energy graph. 
    > $$\frac{dE}{dP}$$
 - `tabulate.ipynb` creates the tables in the text and styled plots of the energy and energy loss. 