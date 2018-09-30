# FDA_Drugs_INSIGHT
Supplement to Health Apps that shows the likelihood of a serious reaction to drugs. Project for Insight Fellows


People are routinely frightened by the results of online health app, albeit irrationally. In this work I utilize data from the FDA on adverse help effects to predict the outcome of an adverse effect, given that it should occur. I utilize a range of wrangling techniques along with a random forest classifier and unsupervised clustering models to outline the probabilities of a serious event given an adverse case. 

Necessary packages:
- scki-kit learn, pandas, numpy, django, urllib, matplotlib, seaborn

- AWS_scripts are the .py files used to analyze the data on Amazon Web Services
- App is a preliminary set of .py files for application display and interactivity
- Presentations are general files for presenting the project during the Fellowship
- helper_funcs is a folder with the core files used for the bulk of the raw analysis
- jupyter_notebooks_CORE has a set of notebooks to explain the code, probably the best place to start in the project
- medDRA is a folder with supplementary files for analysis

The app is on display at http://www.scottpwhite.com/DataProducts/FDA


Link to data source:
- https://open.fda.gov/apis/drug/event/

