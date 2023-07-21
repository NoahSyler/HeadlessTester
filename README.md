# Headless Tester Script

headless_tester.py was designed for a specific use case; however, it could easily be modified for other applications. The "toggles" dictionary in the code is an important variable that will toggle many different settings, depending on how the user would like to run it.

## Quick Description
When the program is run, the main function is called.  
The “toggles“ dictionary contains many settings. A better way to do this would be to move away from this program being only functions, and add a layer of abstraction.  
- The toggles dictionary would represent the attributes of the object, and they would have their own getters and setters  
- They would have default values, so that not every attribute would need to be set.  
The driver is instantiated, then the login function is called.  
- A try except block should be used here  
The driver is then passed to test_all_links(). This returns the failed urls.
- It might be better to filter out the URLs with the ‘#,’ (or make it an option at least)  
- It also might be a good option to filter out external URLs  
- To prevent an endless loop, it will either check that a link is good, or check the links on the next page also. This depends on the value of toggles['secondary_links']  
  - Another way to do this could be with a recursive search. The previous links visited would not be revisited, and links outside of the domain could be tested, but the program would not proceed past them.  
  - Currently, the site is tested in a development environment, so searching for the word ‘error’ suffices.  
  - If a link fails, the URL is saved in the list “failures.” Data from the console log is also written to a file, and a screenshot is captured.  
