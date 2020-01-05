

#urls
ictd_file = "https://www.wider.unu.edu/sites/default/files/Data/ICTDWIDERGRD_2019.xlsx"
weo_file = "https://www.imf.org/external/pubs/ft/weo/2018/01/weodata/WEOApr2018all.xls"
cbcr_file = "https://www.irs.gov/pub/irs-soi/16it01acbc.xlsx"

#names of files
ictd_clean = "ICTD_2019.xlsx"
weo_clean = "WEO_Apr2018.tsv"
cbcr_clean = "CBCR2016.xlsx"

#Year study (the most recent year for CBCR)
year_study = 2016

#Merged file name
merged_file = "merged_Sep19.tsv"

#Save figures and tables here
path_results = "Sep19"

import os 
if not os.path.exists(path_results):
    os.makedirs(path_results)




#Keep only countries with positive gains
positive_gains = False

#Keep only countries with positive profits
positive_profits = False

if (not positive_gains) and (not positive_profits):
    if not os.path.exists(path_results+"/all_countries"):
        os.makedirs(path_results+"/all_countries")
    path_results = path_results+"/all_countries"
elif positive_gains and positive_profits:
    if not os.path.exists(path_results+"/pos_gains_and_pos_prof"):
        os.makedirs(path_results+"/pos_gains_and_pos_prof")
    path_results = path_results+"/pos_gains_and_pos_prof"
elif positive_gains:
    if not os.path.exists(path_results+"/pos_gains"):
        os.makedirs(path_results+"/pos_gains")
    path_results = path_results+"/pos_gains"
elif positive_profits:
    if not os.path.exists(path_results+"/pos_prof"):
        os.makedirs(path_results+"/pos_prof")
    path_results = path_results+"/pos_prof"
    
if not os.path.exists(path_results+"/Figures"):
    os.makedirs(path_results+"/Figures")
if not os.path.exists(path_results+"/Tables"):
    os.makedirs(path_results+"/Tables")
    




#IMPORTS
    
#Standard visualization/data tools
import pylab as plt
import seaborn as sns
import numpy as np
import pandas as pd
from IPython.core.display import display, HTML

#Processes
import os #file processes
import urllib #download files
import pickle #read the pickled dictionaries

#Interactive visualizations
import altair as alt
alt.renderers.enable('notebook')

#Avoid overlaps in labels of scatter plto
from adjustText import adjust_text

#Plot in notebook
#%matplotlib inline

#Change the defaults of visualizations a bit
sns.set(font_scale=1.3)
sns.set_style("whitegrid")



#Dictionaries to convert from name to ISO2 and from ISO3 to ISO2
#Country name to ISO2
name2iso2 = pickle.load(open("Data/name2iso.dump","rb"))
#ISO3 to ISO2
iso3_to_iso2 = pickle.load(open("Data/iso3_2_iso2.dump","rb"))

list_tax_havens = ["Stateless entities and other country","Mauritius","Aruba","Bahamas","Barbados","Bermuda","British Virgin Islands","Cayman Islands","Curacao","Panama","St. Kitts and Nevis","St. Lucia Island","Trinidad and Tobago","Virgin Islands","Guam","Hong Kong","Macau","Saudi Arabia","Singapore","United Arab Emirates","Cyprus","Guernsey","Ireland","Jersey","Luxembourg","Malta","Monaco","Netherlands","Switzerland","Puerto Rico"]
list_tax_havens_iso2 = set([name2iso2[th] for th in list_tax_havens]) #set for faster lookup







#STEP 1

#Check if the files have already been downloaded to speed it up
files = os.listdir("Data")

#ICTD
if ictd_clean not in files:
    urllib.request.urlretrieve(ictd_file,"./Data/{}".format(ictd_clean))

#WEO
if weo_clean not in files:
    urllib.request.urlretrieve(weo_file,"./Data/{}".format(weo_clean))

#CBCR
if cbcr_clean not in files:
    urllib.request.urlretrieve(cbcr_file, "./Data/{}".format(cbcr_clean))
    
#CLEAN WEO DATA

weo_data = pd.read_csv("./Data/{}".format(weo_clean),sep="\t",encoding="latin1")

#Keep relevant columns
weo_data = weo_data.loc[weo_data["WEO Subject Code"]=="NGDPD",["ISO","Country","Subject Descriptor","Units","Scale", "Country/Series-specific Notes", str(year_study),"Estimates Start After"]]

#Convert from Billions to dollars
weo_data["GDP_USD"] = weo_data[str(year_study)].str.replace(",","").astype(float)
weo_data["GDP_USD"] *= 1E9
weo_data["Scale"] = "Dollars"

#Convert ISO3 to ISO2
weo_data["ISO2"] = weo_data["ISO"].map(iso3_to_iso2)

#Save to file 
weo_data.to_csv("./Data/cleaned_{}".format(weo_clean),sep="\t",index=None)


#CLEAN GRD DATA
ictd_data = pd.read_excel("./Data/{}".format(ictd_clean),sheet_name="Merged",skiprows=2,keep_default_na=False,na_values=[""])

#Replacing the columns with numbers because of the multi-level olumns
ictd_data.columns = range(len(ictd_data.columns))
#Keeping the right columns
ictd_data = ictd_data.loc[:,[3,4,5,6,7,23,36,38,24]]
#New column names
ictd_data.columns = ["Country","Reg","Inc","Year_GRD","ISO","TotTax (X)","CIT (AK)","CITnr (AM)","TTxsc (Y)"]

#Convert Reg and Inc to text
d_income = {1:"LICs",2:"LMICs",3:"UMICs",4:"High Income"}
ictd_data["Inc"] = ictd_data["Inc"].map(d_income)
d_region = {1:"East Asia & Pacific",2:"Europe & Central Asia",3:"Latin America & The Caribbean",4:"Middle East & North Africa",5:"North America",6:"South Asia",7:"Sub - Saharan Africa"}
ictd_data["Reg"] = ictd_data["Reg"].map(d_region)


#Using the GDP from the GDP series sheet since it seems to be missing in the "Merged" sheet
ictd_gdp = pd.read_excel("./Data/{}".format(ictd_clean),sheet_name="GDP Series",skiprows=1)
years = list(ictd_gdp.columns)[1:-2]
ictd_gdp = ictd_gdp.melt(id_vars="ISO",value_vars=years,value_name="GDP_LCU",var_name="Year").dropna()

#Print number of countries
print(len(ictd_data["ISO"].unique()))

#Merge GDP to the other and make sure we don't lose countries
ictd_data = pd.merge(ictd_data,ictd_gdp)
print(len(ictd_data["ISO"].unique()))

#Keep only reasonable recent years and make sure we don't lose countries
ictd_data = ictd_data.loc[(ictd_data["Year_GRD"]>year_study-5)]
print(len(ictd_data["ISO"].unique()))

#Create column number_datapoints with the number of non-missing values
ictd_data["number_datapoints"] = ictd_data.groupby(["Country","Year_GRD"])[["GDP_LCU","TotTax (X)","CIT (AK)","CITnr (AM)","TTxsc (Y)"]].transform(np.isfinite).sum(1)
#Keep the most recent year with the maximum number of points
ictd_data = ictd_data.sort_values(by=["number_datapoints","Year_GRD"], ascending=False).groupby("Country").head(1)

#Make sure we don't lose countries
print(len(ictd_data["ISO"].unique()))

#Convert to iso2
ictd_data["ISO2"] = ictd_data["ISO"].map(iso3_to_iso2)
#Save to file 
ictd_data.to_csv("./Data/cleaned_{}".format(ictd_clean),sep="\t",index=None)

# CLEAN CBCR DATA
cbcr_data = pd.read_excel("./Data/{}".format(cbcr_clean),skiprows=2,skipfooter=5,thousands=",")
cbcr_data = cbcr_data.loc[2:]
cbcr_data.columns = ["Country","Number groups","revenue_unrelated","revenue_related","Revenue","P/L before tax","Income tax paid","Income tax accrued","capital","accum_earnings","Number employees","Tangible assets"]

cbcr_data["ISO2"] = cbcr_data["Country"].map(name2iso2)


cbcr_data.loc[cbcr_data["Country"] == 'Africa, other countries',"ISO2"] = "Africa_other"
cbcr_data.loc[cbcr_data["Country"] == 'Americas, other countries',"ISO2"] = "Americas_other"
cbcr_data.loc[cbcr_data["Country"] == 'Asia & Oceania, other countries',"ISO2"] = "Asia_other"
cbcr_data.loc[cbcr_data["Country"] == 'Europe, other countries',"ISO2"] = "Europe_other"

 

total_revenue = cbcr_data.loc[cbcr_data["Country"]=="All jurisdictions","Revenue"].values[0]
total_employees = cbcr_data.loc[cbcr_data["Country"]=="All jurisdictions","Number employees"].values[0]

#Key variables
cbcr_data["Income tax as % of pretax profits"] = 100*cbcr_data["Income tax paid"]/cbcr_data["P/L before tax"]


cbcr_data.to_csv("./Data/cleaned_{}".format(cbcr_clean),sep="\t",index=None)

ictd_columns = ['Reg', 'Inc', 'Year', 'ISO', 'TotTax (X)', 'CIT (AK)',
       'CITnr (AM)', 'TTxsc (Y)', 'GDP_LCU', 'number_datapoints', 'ISO2']

ictd_data = pd.read_csv("Data/cleaned_{}".format(ictd_clean),sep="\t",keep_default_na=False,na_values=[""])
ictd_data = ictd_data.loc[:,ictd_columns]

weo_columns = ['Subject Descriptor', 'Units', 'Scale',
       'Country/Series-specific Notes', 'GDP_USD', 'Estimates Start After',
       'ISO2']
weo_data = pd.read_csv("Data/cleaned_{}".format(weo_clean),sep="\t",keep_default_na=False,na_values=[""])
weo_data = weo_data.loc[:,weo_columns]

cbcr_columns = ['Country', 'Number groups', 'Revenue', 'P/L before tax', 'Income tax paid', 
                'Income tax accrued',
       'capital', 'accum_earnings', 'Number employees', 'Tangible assets',
       'ISO2', 'Income tax as % of pretax profits', 'Sales share %',
       'Employment share %', 'Profit total (M)', 'Sales total (M)',
       'Employment (th)']
cbcr_data = pd.read_csv("Data/cleaned_{}".format(cbcr_clean),sep="\t",keep_default_na=False,na_values=[""])
cbcr_data = cbcr_data.loc[:,cbcr_columns]


#Statutory tax rate (average 2010 - 2016)
cit = pd.read_csv("./Data/corporate tax rates.csv",keep_default_na=False,na_values=[""])
cit_period = cit.loc[(cit["year"]>2012)&(cit["year"]<=2017)].groupby("country_iso2").mean().to_dict()["nctr_final"]

#Update the important ones that were not available
cit_period.update(
    {"Stateless": 0.35,
    "VG": 0,
    "VI": 0,
    "Foreign_controlled":0.2})

#Add the population from the paper with Saila. Also take the GDP to fill the missing values
gdppop = pd.read_csv("Data/gdp_pop.tsv",sep="\t",keep_default_na=False,na_values=[""]).set_index("index").to_dict()
gdp = gdppop["gdp"]
pop = gdppop["population"]

#Some gdp and population were missing in the original data source and were taken from Wikipedia
miss_gdp = pd.read_csv("Data/missing_gdp.tsv",sep="\t",keep_default_na=False,na_values=[""]).set_index("iso2").dropna(subset=["Unnamed: 2"])["Unnamed: 2"]
miss_pop = pd.read_csv("Data/missing_pop.tsv",sep="\t",keep_default_na=False,na_values=[""]).set_index("iso2").dropna(subset=["population"])["population"]

gdp.update(miss_gdp)
pop.update(miss_pop)


#Merge files
merged = pd.merge(cbcr_data,weo_data,on=["ISO2"],how="outer")
merged = pd.merge(merged,ictd_data,on=["ISO2"],how="outer")
merged["CIT"] = merged["ISO2"].map(cit_period)
merged["population"] = merged["ISO2"].map(pop)
merged.loc[np.isnan(merged["GDP_USD"]),"GDP_USD"] = merged.loc[np.isnan(merged["GDP_USD"]),"ISO2"].map(gdp)


#Name the tax havens (list above)
merged.loc[merged["ISO2"].isin(list_tax_havens_iso2),"Inc"] = "Tax haven"

#Give the label "High income" to Foreign_controlled companies
merged.loc[merged["ISO2"] == 'Foreign_controlled',"Inc"] = "High Income"

#Name the other countries as in the file 
merged.loc[merged["Country"] == 'Africa, other countries',"Inc"] = "LICs"
merged.loc[merged["Country"] == 'Americas, other countries',"Inc"] = "UMICs"
merged.loc[merged["Country"] == 'Asia & Oceania, other countries',"Inc"] = "UMICs"
merged.loc[merged["Country"] == 'Europe, other countries',"Inc"] = "High Income"
merged.loc[merged["Country"] == 'Taiwan',"Inc"] = "High Income"
print(merged.shape)

#Drop raw with all missign values
merged = merged.dropna(subset=["ISO2"])
print(merged.shape)

#Add some extra characteristics
G7 = set(["CA","FR","DE","IT","JP","GB","US"])
G24 = set(['DZ', 'CI', 'CD', 'EG', 'ET', 'GA', 'GH', 'KE', 'MA', 'NG', 'ZA', 'AR', 'BR', 'CO', 'EC', 'GT', 'HT', 'MX', 'PE', 'TT', 'VE', 'CN', 'IN', 'IR', 'LB', 'PK', 'PH', 'LK', 'SY'])
G77 = set(['AF', 'DZ', 'AR', 'BJ', 'BO', 'BR', 'BF', 'BI', 'KH', 'CM', 'CF', 'TD', 'CL', 'CO', 'CG', 'CD', 'CR', 'DO', 'EC', 'EG', 'SV', 'ET', 'GA', 'GH', 'GT', 'GN', 'HT', 'HN', 'IN', 'ID', 'IR', 'IQ', 'JM', 'JO', 'KE', 'KW', 'LA', 'LB', 'LR', 'LY', 'MG', 'MY', 'ML', 'MR', 'MA', 'MM', 'NP', 'NI', 'NE', 'NG', 'PK', 'PA', 'PY', 'PE', 'PH', 'RW', 'SA', 'SN', 'SL', 'SO', 'LK', 'SD', 'SY', 'TZ', 'TH', 'TG', 'TT', 'TN', 'UG', 'UY', 'VE', 'VN', 'YE'])
EU = set(["AT","BE","BG","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE","GB"])
OECD = set(['AU', 'AT', 'BE', 'CA', 'CL', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IL', 'IT', 'JP', 'KR', 'LV', 'LT', 'LU', 'MX', 'NL', 'NZ', 'NO', 'PL', 'PT', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR', 'GB', 'US'])
G20 = set(['AR', 'AU', 'BR', 'CA', 'CN', 'FR', 'DE', 'IN', 'ID', 'IT', 'JP', 'MX', 'RU', 'SA', 'ZA', 'KR', 'TR', 'GB', 'US'])
US = set(["US"])
G7_noUS = G7 - US
OECD_noUS = OECD - US
G20_noOECD = G20 - OECD

labels_groups_countries = ["G7","G24","G77","EU","OECD","G20","US","G7_noUS","OECD_noUS","G20_noOECD"]
for cat,label in zip([G7,G24,G77,EU,OECD,G20,US,G7_noUS,OECD_noUS,G20_noOECD],
                     labels_groups_countries):
    merged[label] = merged["ISO2"].isin(cat)

#Create a column with Trues, this will be useful later when using the function to group 
merged["All"] = True



#Continues to STEP 2 i.e 2.1 

#Drorp countries not present in CBCR data (small countries)
merged = merged.dropna(subset=["Country"])
print(merged.shape)

#Drop aggregated by continent (4 instance)
merged = merged.loc[~merged["Country"].str.contains("total")]
merged = merged.loc[~merged["Country"].str.contains("controlled")]
print(merged.shape)

#Calculate tax collected using GRD + WEO data
merged["TotTax (X) USD"] = merged["TotTax (X)"] * merged["GDP_USD"]
merged["CIT (AK) USD"] = merged["CIT (AK)"] * merged["GDP_USD"]
merged["CITnr (AM) USD"] = merged["CITnr (AM)"] * merged["GDP_USD"]
merged["TTxsc (Y) USD"] = merged["TTxsc (Y)"] * merged["GDP_USD"]


merged.head()

total_revenue = merged.loc[merged["ISO2"]=="World","Revenue"].values[0]
total_employees = merged.loc[merged["ISO2"]=="World","Number employees"].values[0]
total_profit = merged.loc[merged["ISO2"]=="World","P/L before tax"].values[0]

#Save to diskCSV
merged.to_csv("New Data/mydataCSV".format(merged_file),index=None) #CSV
merged.to_csv("New Data/mydataTSV".format(merged_file),sep="\t",index=None) #TSV
merged.to_csv("New Data/mydata.csv".format(merged_file),index=None) #CSV
merged.to_csv("New Data/mydata.tsv".format(merged_file),sep="\t",index=None) #TSV

