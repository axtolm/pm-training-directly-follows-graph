### A streamlit web app "Process Mining training" - "Directly-Follows Graph (DFG)" module
This web app is designed to help beginners in Process Mining understand the Directly-Follows Graphs topic using simple examples. It works with event logs that users can select from a list of pre-installed ones or create their own via easy manual input. We specifically use the event log format found in Process Mining textbooks [1]: $L =[< a, c, d>^{45},< b, c, e >^{42}]$. The app includes five exercises that cover various aspects of DFGs, such as the baseline discovery algorithm, constructing the DFG matrix and footprint, and applying different filtering techniques.    

### Usage   
You can try the app on the Streamlit Cloud via the following [URL](http://185.105.88.103:8591/).    
Alternatively, you can download and deploy it on your computer as a Python application based on the Streamlit framework (see `requirements.txt` and `packages.txt` for details).    

### Features
This web app is designed solely for training purposes to help users understand the essential aspects of DFGs step-by-step using small event logs and learn how to create them using Python if desired. To this end:    
1. There are no options for uploading event logs from any files - only manual input or selection from the pre-installed list.
2. Python code is easy to read - only one file, no classes, and all text information in one dictionary.
3. All intermediate calculation results are displayed.
4. Tables, matrices, and graphs are used to visualize DFGs.
5. The filtering exercises provide visualization of DFGs before and after filtering to enable their comparison and analysis.

### Exercises
The app includes the following five exercises:
1. **Baseline Discovery Algorithm** - create a Directly-Follows Graph using this algorithm.    
2. **DFG Matrix and Footprint** - obtain a matrix representation of the DFG and build a matrix of relations between activities.    
3. **Activity-Based Filtering** - remove some activities from the event log and recreate the DFG.    
4. **Variant-Based Filtering** - remove some cases from the event log and recreate the DFG.    
5. **Arc-Based Filtering** - remove some DFG arcs and recreate the DFG.     
     
You can do all the exercises manually and compare the results with the app.

### References
[1] van der Aalst, W.M.P.: Foundations of Process Discovery. In: van der Aalst, W.M.P., Carmona, J. (eds.) PMSS 2022. LNBIP, vol. 448, pp. 37–75. Springer, Cham (2022).
https://doi.org/10.1007/978-3-031-08848-3_2    

### Contact information
The initial version of the `pm-training-directly-follows-graph` was developed by Alexander Tolmachev.    
E-mail: axtolm@gmail.com 
