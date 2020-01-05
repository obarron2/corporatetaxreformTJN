# The Effects of Corporate Tax Policy Reforms  

Published 10/12/19

Contact:  
oliver@taxjustice.net  
[@OliverBarron_](https://twitter.com/OliverBarron_)  



### Project Description

The aim of this project is to develop a programme that calculates the effects of changes in corporate tax policy on tax revenues for different jurisdictions. Then to create an interactive graphic which displays these effects with adjustable variables. This 'create your own policy' graphic will display a range of tax revenue change outcomes based on the percentage of corporations' global profits taxed, and the percentage of taxing rights that are apportioned on sales vs employment. This project is based on paper Cobham et al (2019), and accompanying code - both available [here](https://osf.io/preprints/socarxiv/j3p48/).  

### Context 

The Organisation for Economic Cooperation and Development (OECD) is currently developing corporate tax policy reofrms, as explained by Cobham et al (2019) 

> "the OECD is consulting on the biggest reshaping of international tax rules for ninety years, following an earlier attempt (through phase 1 of the OECD Base Erosion and Profit Shifting initiative, 2013-2015) to patch up the existing tax rules.
Negotiations are ongoing within the OECD/G20 Inclusive Framework on BEPS3 (Inclusive Framework), which brings together 134 countries (both OECD and non- OECD members)."

Comissioned by the Independent Commission for the Reform of International Corporate Taxation (ICRICT), Cobham et al (2019) analyse the corporate tax reform proposal from the OECD. This is compared to proposals from the International Monetary Fund (IMF) and tax justice campaigners. 

### Data

This project uses the data from this paper, which are the current best estimates on corporations sales, employees, and profits, based on country-by-country reporting data released from the US relating to US multinational corporations. The full global data will be released by the OECD in January. This project intends to be update upon this release. 

Further Data:
WEO: World Economic Outlook database (GDP in dollars)
GRD: Government Revenue Dataset (Government corporate and tax revenues)
Data on statutory tax rate: Janský, Petr; Palanský, Miroslav (2018)

***

### Using This Code 

Download the project folder and set this as the working directory. Run the code to generate the GUI. Adjust the variables and outcomes, making sure to press the 'Update Jurisdictions' button after selecting your jurisdictions below the search box. Use code below the GUI to save the results from based on your values of the widgets.

Files:
1. maincode.ipynb - the Jupyter Notebook containing that main code.   
2. mydata.csv - from Cobham et al (2019) code - section 2.1 line 19.  
3. datacode.py - a python script that creates mydata.csv from Cobham et al (2019) code and data. 
4. README - Readme file in markdown 
5. License - License file of GNU GPL

Sections:
1. Load Data  
2. Create Summaries and Prepare Dataset  
3. Create GUI  
4. Testing

Requirements:
- Python 3.0 
- IPython, ipywidgets, matplotlib, numpy, pandas, difflib and os. 

License:
- Licensed under GNU General Public License v3.0. 


## References 

Cobham, Faccio, FitzGerald (2019) Global inequalities in taxing rights: An early evaluation of the OECD tax reform proposals (Preliminary Draft) Available here https://osf.io/preprints/socarxiv/j3p48/

