# PhonePasswordGenerator

This is a simple Python program that graphically shows different possible mobile pattern passwords.

On first launch, it accepts three parameters from the user:

* A subpattern that the pattern has to contain
* If the subpattern given should be rotated
* The minimum number of nodes used
* The maximum number of nodes used

After that, it generates a graphic window in which the results are displayed.

At any point, the user may save the progress, which generates a .cfg file. When run again, the user may choose to continue from that point or input new parameters.

The library graphics.py is required to run this software.
