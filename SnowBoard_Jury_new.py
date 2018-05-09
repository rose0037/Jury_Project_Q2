
# coding: utf-8

# In[76]:



# coding: utf-8
import pandas as pd
import numpy as np

################### Old Data Set ###################


data = pd.read_csv('jury_data.csv', encoding= 'ISO-8859-1', skiprows=[0,2])
data.rename(columns={"Was defendant Mesa Management negligent?": "Mesa_Negligent", 
                         "Was Mesa Management's negligence a substantial factor in causing harm to  Mackenzie Dunn?":"Liability",
                         "What are the total damages that you find that MacKenzie Dunn sufferered?":"damages" ,
                         "What is your sex?": "gender",
                         "Please write your answer to the preceding damages question in words (quality check).":"damages_word",
                         "What percentage of responsibility for Mackenzie Dunn's injuries was each party responsible for? (Answers should add up to 100%) - Mesa Management Co":"Mesa_reponsible_percentage",
                         "Path":"Scenario",
                         "Was MacKenzie Dunn negligent?":"Dunn_negligent",
                         "Unnamed: 63":"perc_calc"
                         },inplace=True)
data['mm_perc'] = np.where(data['Mesa_reponsible_percentage']>=1, data['perc_calc'], data['Mesa_reponsible_percentage'])
req_data = pd.DataFrame(data[["Mesa_Negligent","damages","Liability",
                 "gender",
                 "damages_word",
                 "Scenario","Dunn_negligent","perc_calc","Start Date","End Date","mm_perc"]])


req_data['Liability'] = req_data['Liability'].map({'Yes': 1, 'No': 0})


print(req_data.columns)



print(pd.isnull(req_data).any())
print(pd.isnull(req_data['Scenario']).any())
req_data = req_data[np.isfinite(data['Scenario'])]
print(pd.isnull(req_data['Scenario']).any())
req_data['damages'].fillna(0,inplace=True)
req_data['damages_word'].fillna(0,inplace=True)
req_data['mm_perc'].fillna(1,inplace=True)
req_data['perc_calc'].fillna(0,inplace=True)
#Dropping the last two rows which has null values
#data[pd.isnull(data['Path'])]
#data['Path']=data.Path.dropna(inplace= True)
#data[pd.isnull(data['Path'])]
print(pd.isnull(req_data).any())




#Changing data types of columns
req_data['End Date'] = pd.to_datetime(data['End Date'])
req_data['Start Date'] = pd.to_datetime(data['Start Date'])
req_data['Scenario']= req_data.Scenario.astype(int)
req_data['Liability']= req_data.Liability.astype(int)
req_data.dtypes





# Getting the id of the column
data.columns.get_loc("Liability")










# In[77]:


#Cleaning Damages and perc_calc column
print(req_data.isnull().any())
req_data['damages'] = req_data['damages'].str.replace(',', '')
req_data['perc_calc'] = req_data['perc_calc'].str.replace('$', '')
req_data['perc_calc'] = req_data['perc_calc'].str.replace(',', '')
req_data['perc_calc'] = req_data['perc_calc'].str.replace('-', '')
req_data['perc_calc'] = req_data['perc_calc'].str.replace("  ", '')
req_data['mm_perc'] = req_data['mm_perc'].str.replace("$", '')
req_data['mm_perc'] = req_data['mm_perc'].str.replace(",", '')
req_data['mm_perc'] = req_data['mm_perc'].str.replace("  ", '')
#req_data.damages=pd.to_numeric(req_data['damages'].str.replace(',', ''))
#req_data.perc_calc=pd.to_numeric(req_data.perc_calc)
#print(req_data.isnull().any())




req_data.damages=pd.to_numeric(req_data['damages'])
req_data.perc_calc=pd.to_numeric(req_data.perc_calc)
req_data['damages'].fillna(0,inplace=True)  
req_data['mm_perc'].fillna(1,inplace=True)
req_data['perc_calc'].fillna(0,inplace=True)
#print(req_data.damages)
print(req_data.isnull().any())





print(req_data[pd.isnull(req_data['Dunn_negligent'])])














# In[78]:


#EDA





req_data['winrate_percentage']=req_data.Liability
req_data['damages_mean']=req_data.damages+req_data.perc_calc
req_data['damages_median']=req_data.damages
req_data['damages_sd']=req_data.damages

winrate_damages_expected=req_data.groupby('Scenario').aggregate(
    {'winrate_percentage': np.mean, 'damages_mean': np.mean,'damages_median':np.median,'damages_sd':np.std})


winrate_damages_expected


# In[79]:



#req_data['winrate_percentage']=np.mean(req_data.Juror_Response)
#print(req_data)
req_data['mm_perc'].fillna(1,inplace=True)
req_data['damages_mean1']=req_data.damages*pd.to_numeric(req_data.mm_perc)
req_data['damages_median1']=req_data.damages
req_data['damages_sd1']=req_data.damages
#print(req_data.mm_perc)

winrate_damages_plaintiffwin=req_data.loc[(req_data['Dunn_negligent']=='No') & (req_data['Liability']==1)].groupby('Scenario').aggregate({'damages_mean1': np.mean,'damages_median1':np.median,'damages_sd1':np.std})


winrate_damages_plaintiffwin


# In[80]:


import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

sns.factorplot(x='Scenario', y='damages', kind='box',data=req_data)



# In[81]:


pd.crosstab(data.Scenario,data.Liability).plot(kind='bar')
plt.title('Purchase Frequency for Job Title')
plt.xlabel('Scenario')
plt.ylabel('Liability')
plt.savefig('Juror Response per each Scenario')





a = req_data['Scenario']
b = req_data['Liability']
pd.crosstab(a,b)


# In[82]:


########### New data set ################


# In[83]:


import pandas as pd
df =pd.read_csv('Low_Anchor.tsv', sep='\t+',skiprows=[0,2, 4]+list(range(1,1614,2)) + [1614], names = ['StartDate', 'EndDate',
       'ResponseType', 
       'IP Address', 
       'Progress', 
       'Duration',
       'Finished',
       'RecordedDate',
       'ResponseID', 
       'RecipientLastName','RecipientFirstName','RecipientEmail',
       'ExternalDataReference','LocationLatitude', 'LocationLongitude',
       'DistributionChannel', 'UserLanguage', 'Participation_in_this_project.',
       'Browser Meta Info - Browser',
       'Browser Meta Info - Version',
       'Browser Meta Info - Operating System',
       'Browser Meta Info - Resolution',
       'What number did you hear?',
       'What word did you see?',
       'What is your sex?',
       'How old are you?',
       'Which of the following best describes your ethnicity?',
       'Are you Spanish/Hispanic/Latino',
       'What is the highest degree or level of school you have completed?',
       'This is an attention check.  Select 200.',
       'Which of the following best describes your total household income?',
       'Where would you place yourself on this scale?',
       'What is your zip code?',
       'Timing - First Click','Timing - Last Click','Timing - Page Submit', 'Timing - Click Count',
       'Timing - First Click.1', 'Timing - Last Click.1', 'Timing - Page Submit.1',
       'Timing - Click Count.1', 'Timing - First Click.2','Timing - Last Click.2',
       'Timing - Page Submit.2','Timing - Click Count.2','Timing - First Click.3','Timing - Last Click.3',
       'Timing - Page Submit.3','Timing - Click Count.3','Timing - First Click.4', 'Timing - Last Click.4',
       'Timing - Page Submit.4','Timing - Click Count.4', 'Timing - First Click.5', 'Timing - Last Click.5',
       'Timing - Page Submit.5','Timing - Click Count.5', 'Timing - First Click.6', 'Timing - Last Click.6',
       'Timing - Page Submit.6',  'Timing - Click Count.6', 'Timing - First Click.7','Timing - Last Click.7',
       'Timing - Page Submit.7',  'Timing - Click Count.7',
       'Identify the statement that correctly describes the facts of this case. (This is the attention check)',
       'Was_snowboard_sold_McNeil_defective_14', ## using this
       "Is_substantial_factor_McNeil_injuries_14",
       'Non_economic_damages_McNeil_suffered_14',
       'Damages_words_14',
       'Was_McNeil_negligent',
       'McNeil_negligence_substantial_factor_for_injuries',
       'Percentage_of_responsibility_X5',
       'Percentage_of_responsibility_McNeil',
       'Was_snowboard_sold_McNeil_defective_58',
       "Is_substantial_factor_McNeil_injuries_58",
       'Economic_damages_McNeil_suffer_58',
       'Economic_Damages_In_Word_58',
       'Non_economic_damages_McNeil_suffered_58',
       'Non_Economic_Damages_In_Word_58',
       'Please explain why you arrived at your decision? (50 character minimum)',
       'Q40',#'Did the fact that X5 added core inserts to the later Carve 3000 model, affect your view as to whether the original Carve 3000 was defective?',
       'Were you able to ignore the  fact that X5 added core inserts to the later Carve 3000 model when deciding whether the original Carve 3000 was defective?',
       'Path'])
        
df.head()


# In[84]:


df.dtypes


# In[85]:


## replacing hexadecimal value of damages'/x00' to ''
for i in range(len(df)):
    df['Was_snowboard_sold_McNeil_defective_14'].values[i] = df['Was_snowboard_sold_McNeil_defective_14'].values[i].replace('\x00','')
    df['Is_substantial_factor_McNeil_injuries_14'].values[i] = df['Is_substantial_factor_McNeil_injuries_14'].values[i].replace('\x00','')
    df['Non_economic_damages_McNeil_suffered_14'].values[i] = df['Non_economic_damages_McNeil_suffered_14'].values[i].replace('\x00','')
    df['Damages_words_14'].values[i] = df['Damages_words_14'].values[i].replace('\x00','')
    df['Was_McNeil_negligent'].values[i] = df['Was_McNeil_negligent'].values[i].replace('\x00','') ;
    df['McNeil_negligence_substantial_factor_for_injuries'].values[i] = df['McNeil_negligence_substantial_factor_for_injuries'].values[i].replace('\x00','') ;
    df['Percentage_of_responsibility_X5'].values[i] = df['Percentage_of_responsibility_X5'].values[i].replace('\x00','') ;
    df['Percentage_of_responsibility_McNeil'].values[i] = df['Percentage_of_responsibility_McNeil'].values[i].replace('\x00','') ;
    df['Was_snowboard_sold_McNeil_defective_58'].values[i] = df['Was_snowboard_sold_McNeil_defective_58'].values[i].replace('\x00','') ;
    df['Is_substantial_factor_McNeil_injuries_58'].values[i] = df['Is_substantial_factor_McNeil_injuries_58'].values[i].replace('\x00','') ;
    df['Economic_damages_McNeil_suffer_58'].values[i] = df['Economic_damages_McNeil_suffer_58'].values[i].replace('\x00','') ;
    df['Economic_Damages_In_Word_58'].values[i] = df['Economic_Damages_In_Word_58'].values[i].replace('\x00','') ;
    df['Non_economic_damages_McNeil_suffered_58'].values[i] = df['Non_economic_damages_McNeil_suffered_58'].values[i].replace('\x00','') ;
    df['Non_Economic_Damages_In_Word_58'].values[i] = df['Non_Economic_Damages_In_Word_58'].values[i].replace('\x00','') ;
    df['Path'].values[i] = df['Path'].values[i].replace('\x00','') ;  
    df['Q40'].values[i] = df['Q40'].values[i].replace('\x00','') ; 
    #df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?'].values[i] =  df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?'].values[i].replace('\x00','') ;  


# In[86]:


## Changing Data type
df.StartDate = pd.to_datetime(df.StartDate)
df.EndDate   = pd.to_datetime(df.EndDate) 
#df.Was_snowboard_sold_McNeil_defective_14   = pd.to_numeric(df.Was_snowboard_sold_McNeil_defective_14)
df.Is_substantial_factor_McNeil_injuries_14 = pd.to_numeric(df.Is_substantial_factor_McNeil_injuries_14)
df.Non_economic_damages_McNeil_suffered_14  = pd.to_numeric(df.Non_economic_damages_McNeil_suffered_14)
df.Was_McNeil_negligent                     = pd.to_numeric(df.Was_McNeil_negligent)
df.McNeil_negligence_substantial_factor_for_injuries= pd.to_numeric(df.McNeil_negligence_substantial_factor_for_injuries)
df.Percentage_of_responsibility_X5          = pd.to_numeric(df.Percentage_of_responsibility_X5)
df.Percentage_of_responsibility_McNeil      = pd.to_numeric(df.Percentage_of_responsibility_McNeil)
#df.Was_snowboard_sold_McNeil_defective_58   = pd.to_numeric(df.Was_snowboard_sold_McNeil_defective_58)
df.Is_substantial_factor_McNeil_injuries_58 = pd.to_numeric(df.Is_substantial_factor_McNeil_injuries_58)
df.Economic_damages_McNeil_suffer_58        = pd.to_numeric(df.Economic_damages_McNeil_suffer_58)
df.Non_economic_damages_McNeil_suffered_58  = pd.to_numeric(df.Non_economic_damages_McNeil_suffered_58)
df.Q40 =pd.to_numeric(df.Q40) 
# Handling for Path
df.Path = pd.to_numeric(df.Path) 
df['Path'].fillna(0,inplace = True)
df.Path =  df.Path.astype(int)
df.dtypes


# # Extracting the required columns and storing it in "newdf" data frame.

# In[87]:


newdf =pd.DataFrame(df[['StartDate', 'EndDate',
       'Was_snowboard_sold_McNeil_defective_14', 
       "Is_substantial_factor_McNeil_injuries_14",
       'Non_economic_damages_McNeil_suffered_14',                                                                                         
       'Was_McNeil_negligent',
       'McNeil_negligence_substantial_factor_for_injuries',                                                                                         
       'Percentage_of_responsibility_X5',
       'Percentage_of_responsibility_McNeil'                                                                                      ,
       'Was_snowboard_sold_McNeil_defective_58',
       "Is_substantial_factor_McNeil_injuries_58",
       'Economic_damages_McNeil_suffer_58',
       'Non_economic_damages_McNeil_suffered_58',
       'Q40',
       'Path']])
        
##newdf.head(5)
newdf.sample(5)


# ## See how many missing data points we have

# #### Ok, now we know that we do have some missing values. Let's see how many we have in each column.

# In[88]:


import numpy as np

missing_values_count = newdf.isnull().sum()

print(missing_values_count)

total_cells = np.product(newdf.shape)
total_missing = missing_values_count.sum()

# percent of data that is missing
(total_missing/total_cells) * 100


# In[89]:


#newdf.isnull().sum()
newdf.shape


# ### As we are just working on from path 1 to 8, Lets remove path with value 0.

# In[90]:


newdf[newdf.Path <=0]


# In[91]:


newdf[newdf.Path <=0].shape


# <font color = 'red' size = "5"> As we can see there are 13 observation with path value equal to 0. We are removing these observation </font>

# In[92]:


# removed path with 0 values 
newdf = newdf[newdf.Path > 0]


# ## Replacing the Null Values with empty string(Easy to convert to other datatypes Later)

# In[93]:



print(pd.isnull(newdf).any())
newdf = newdf[np.isfinite(newdf['Path'])]
newdf['Is_substantial_factor_McNeil_injuries_14'].fillna("",inplace=True)
newdf['Non_economic_damages_McNeil_suffered_14'].fillna("",inplace=True)
newdf['Was_McNeil_negligent'].fillna("",inplace=True)
newdf['McNeil_negligence_substantial_factor_for_injuries'].fillna("",inplace=True)
newdf['Percentage_of_responsibility_X5'].fillna("",inplace=True)
newdf['Percentage_of_responsibility_McNeil'].fillna("",inplace=True)
newdf['Was_snowboard_sold_McNeil_defective_58'].fillna("",inplace=True)
newdf['Is_substantial_factor_McNeil_injuries_58'].fillna("",inplace=True)
newdf['Economic_damages_McNeil_suffer_58'].fillna("",inplace=True)
newdf['Non_economic_damages_McNeil_suffered_58'].fillna("",inplace=True)
newdf['Q40'].fillna("",inplace=True)
# Printing the first 5 lines.
newdf.head(5)


# ### Changing datatype of damages and filling NULL values with 0s.

# As per the requirement we have to calculate the Total Damages for each path.
# There are 8 different Paths. 
# 
# - Path 1 2 3 4 : Scenarios with no Low Anchor. 
# - Path 5 6 7 8 : Scenarios with Low Anchor. 
# 
# As we are not taking consideration of Low Anchor,we renamed Path 5,6,7,8 as 1,2,3,4 respectively. 
# 
# Later we converted the data type of Path as "Int".

# In[94]:


newdf['Path'].replace([5, 6 ,7,8], [1,2,3,4], inplace = True)
newdf['Path']= newdf.Path.astype(int)


# <font color='red'>We need to change the data type of damages. There are 3 different columns that have the damages 
# information. From previous data type check, we found that there are so many missing values for damages.
# So we replaced them with 0.
# </font>
# 
# For simplicity to plot Path vs damages we combined all damages into one column and named it 
# as "Total_Damages". 

# In[95]:


newdf.Economic_damages_McNeil_suffer_58        = pd.to_numeric(newdf.Economic_damages_McNeil_suffer_58)
newdf.Non_economic_damages_McNeil_suffered_58  = pd.to_numeric(newdf.Non_economic_damages_McNeil_suffered_58)
newdf.Non_economic_damages_McNeil_suffered_14  = pd.to_numeric(newdf.Non_economic_damages_McNeil_suffered_14) 


# ## Plot of Path vs Economic Damages.
# 
# #### We have economic damages only from Path 5 to 8, so ploting the graph for the same.

# In[96]:


import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
newdf58 = df[df.Path>4]
plt = sns.factorplot(x='Path', y='Economic_damages_McNeil_suffer_58', kind='box',data=newdf58, size=5)
_ = plt.set(xlabel='Path', ylabel='Economic Damages')


# ## Plot of Path(5 to 8) vs Non Economic Damages.

# In[97]:


import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

plt1 = sns.factorplot(x='Path', y='Non_economic_damages_McNeil_suffered_58', kind='box',data=newdf58, size=6)
_ = plt1.set(xlabel='Path', ylabel='Non Economic Damages')


# ## Plot of Path(1 to 4) vs Non Economic Damages.

# In[98]:


plt2 = sns.factorplot(x='Path', y='Non_economic_damages_McNeil_suffered_14', kind='box',data=newdf, size=5)
_ = plt2.set(xlabel='Path', ylabel='Non Economic Damages')


# In[99]:


#create new column for non economic damages(for path 1 to 4 and path 5 to 8--do boxplot)


# Before Filling the NaN values with 0, first lets check if any juror has put 0 intentionally

# In[100]:


newdf.query('Non_economic_damages_McNeil_suffered_14 == 0 | Non_economic_damages_McNeil_suffered_58 == 0 |Economic_damages_McNeil_suffer_58 ==0')


# <font color='red'> We found that one row has 0 value for Non_economic damages McNeil suffered. 
# </font>

# In[101]:


newdf.Economic_damages_McNeil_suffer_58.fillna(0, inplace = True)
newdf.Non_economic_damages_McNeil_suffered_58.fillna(0, inplace = True)
newdf.Non_economic_damages_McNeil_suffered_14.fillna(0, inplace = True)

newdf['Total_Damages'] =  newdf['Economic_damages_McNeil_suffer_58']+newdf['Non_economic_damages_McNeil_suffered_58'] + newdf['Non_economic_damages_McNeil_suffered_14']


# # Box Plot for Total Damages vs Path.
# 
# We used Violin Plot because it allows a deeper understanding of the density. 

# In[102]:


(newdf.Total_Damages==0).sum()


# In[103]:


import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
# import matplotlib.axes as p


newdf["Path"] = newdf.Path.astype('category')
#_=sns.factorplot(x='Path', y='Total_Damages', kind='violin',data=newdf, size=5)#.set(ylim=0)
#sns.factorplot(x='Path', y='Total_Damages',kind='violin',data=newdf, size=5)#.fit_kde

sns.violinplot(x="Path", y="Total_Damages", data=newdf, inner = 'box')

# Note: This happens because to calculate the lowest whisker you use : 
#The values for Q1 – 1.5×IQR are the "fences" that mark off the "reasonable" 
# values from the outlier values.  gaussian_kde works for both uni-variate and multi-variate data. 
# It includes automatic bandwidth determination.
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
   


# From the box plot, we can see there are some outlier for Path 1 and 4. Lets find what are the outliers are.
# For Path column in newdf, we can get 0.99 quantile and then we printed the rows having outlier.

# In[104]:


damage_df = newdf[newdf.Total_Damages >0]
sns.factorplot(x='Path', y='Total_Damages', kind='box',data=damage_df, size=6)


# **based on above boxplot path 4 has an outlier value around 1000000. Hence we will remove this value**

# In[105]:


sns.factorplot(x='Path', y='Total_Damages', kind='violin',data=damage_df, size=6)


# In[106]:


q = newdf["Total_Damages"].quantile(0.99)
print(q)
newdf.query("Total_Damages >= 500000")


# So Lets remove the outlier and plot the box plot again.

# In[107]:


newdf1 = newdf[(newdf.Total_Damages < q) & (newdf.Total_Damages >0) ]
sns.factorplot(x='Path', y='Total_Damages', kind='box',data=newdf1, size=5)


# In[108]:


newdf['Liability'] = newdf['Was_snowboard_sold_McNeil_defective_14'] + newdf['Was_snowboard_sold_McNeil_defective_58']


# For graph we are changing the value 4 and 6 to Yes and No. Liability with blank is replace with "No Reponse"

# In[109]:


newdf['Liability'].replace(['4', '6' , ''], ['Yes','No', 'No Reponse'], inplace = True)


# In[110]:


## Cleaning data(checking if any column has null values)
newdf.isnull().any()


# ## Graph showing the responses of jurors for each path

# In[111]:


## Plot Juror Responce vs Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


pd.crosstab(newdf.Path,newdf.Liability).plot(kind='bar', fontsize = 15, figsize=(10,6))
plt.title('Liability Vs Path Graph')
plt.xlabel('Path')
plt.ylabel('Liability')
plt.savefig('Juror Response vs Path')

a = newdf['Path']
b = newdf['Liability']
pd.crosstab(a,b)


# In[112]:


## Finding winrate percentage for each path 
ratedf=pd.DataFrame(newdf[['Liability','Path','Was_McNeil_negligent']])
ratedf['winrate_percentage']=ratedf.Liability


# ## Finding the Winrate, Expected Damages, mean , median and SD

# In[113]:



ratedf['winrate_percentage']=newdf.Liability
ratedf['damages_mean']=pd.to_numeric(newdf.Non_economic_damages_McNeil_suffered_14) + pd.to_numeric(newdf.Non_economic_damages_McNeil_suffered_58) 
ratedf['damages_median']=pd.to_numeric(newdf.Non_economic_damages_McNeil_suffered_14 )+pd.to_numeric( newdf.Non_economic_damages_McNeil_suffered_58) 
ratedf['damages_sd']=pd.to_numeric(newdf.Non_economic_damages_McNeil_suffered_14) + pd.to_numeric(newdf.Non_economic_damages_McNeil_suffered_58)
ratedf['winrate_percentage'] = ratedf['winrate_percentage'].map({"Yes":1, "No":0})

winrate_damages_expected=ratedf.groupby('Path').aggregate(
    {'winrate_percentage': np.mean
     ,'damages_mean': np.mean
     ,'damages_median':np.median
     ,'damages_sd':np.std
    })

winrate_damages_expected


# ## Finding the Damages, mean , median and SD when plaintiff wins.

# In[114]:



winrate_damages_plaintiffwin = ratedf.loc[(ratedf['Was_McNeil_negligent']== 1) & (ratedf['Liability']=='Yes')].groupby('Path').aggregate(
    {'damages_mean': np.mean
     ,'damages_median':np.median
     ,'damages_sd':np.std
    })
winrate_damages_plaintiffwin


# ## Answering to the question.
# 
# 
# 
# <font color = red>
# With respect to the first question, I realize that answers from participants in versions 1 and 5 are meaningless.  They did not see evidence of added core inserts. As far as the analysis, I think we want to see if this answer predicted how people responded to the liability questions. For example, did people that said "Yes this evidence strongly suggested the Carve 3000 was defective” find liability more often than people that answered “No”. 
# </font>
# 
# Here Q40 is "Did the fact that X5 added core inserts to the later Carve 3000 model, affect your view as to whether the original Carve 3000 was defective?"
# 
# The Values are: 
# - 1 = Yes, it strongly suggested that the original Carve 3000 was defective.
# - 2 = Yes, it somewhat suggested that the original Carve 3000 was defective.
# - 3 = No, it did not suggest that the original Carve 3000 was defective.
# 
# So first lets check the brief summary table for each scenarios.

# In[126]:


a = newdf['Q40'].replace([1.0,2.0,3.0], ['Yes','Maybe','No'])
a = a[a.apply(len) > 0]
b = newdf['Liability']
pd.crosstab([df.Path,b], a)


# ## Observation 
# 
# - Among 54 Juror who <font color = 'red'>Strongly</font> supported the  that the fact that the original Carve 3000 was defective, 50 said Yes for Liability. 
# 
# - Among 238 Juror who said No to question 40, 185 said No for Liability i:e <font color = red> No for "Was the Carve 3000  snowboard X5 sold Connor McNeil defective?" </font> and 54 Juror said 'Yes' for Liability. 
# 
# #### Below is the plot for Path 1 and 5

# In[130]:


newdf15 = df[(df.Path == 1)| (df.Path == 5)]
_ = pd.crosstab([newdf15.Path,b], a).plot(kind='bar', fontsize = 10, figsize=(7,5))


# ## Question 2:
# 
# With respect to the 2nd questions, again answers from participants in versions 1,2 and 5 and 6  are meaningless. They did not receive the jury instruction telling them to ignore the evidence.  Again, we should do the same analysis as above. Do people that say they can ignore the evidence have lower liability verdicts than people that say they cannot ignore the evidence (for the remaining scenarios 3-4 and 7-8).
# 
# .
# 
# <font color = red>Q41: 'Were you able to ignore the  fact that X5 added core inserts to the later Carve 3000 model when deciding whether the original Carve 3000 was defective?'</font>
# 
# ### Plot for Path 3, 4 , 7 and 8

# In[129]:


newdf3478 = df[(df.Path == 3)| (df.Path == 4)|(df.Path == 7)| (df.Path == 8)]
_ = pd.crosstab([newdf3478.Path,b], a).plot(kind='bar', fontsize = 10, figsize=(7,5))  


# In[ ]:


newdf.columns
newdf1=pd.DataFrame(newdf[["StartDate","EndDate","Liability",'Total_Damages','Path','Was_McNeil_negligent']])
newdf1


# In[ ]:


newdf1.rename(columns={"StartDate": "Start Date", 
                         "EndDate":"End Date",
                         "Total_Damages":"damages",
                       "Was_McNeil_negligent":"Plaintiff_negligent"
                         },inplace=True)

newdf1['Plaintiff_negligent'] = newdf1['Plaintiff_negligent'].map({1:"Yes", 2:"No"})
newdf1['Liability'] = newdf1['Liability'].map({"Yes":1, "No":0})


# In[ ]:


req_data.columns
req_data1=pd.DataFrame(req_data[["Start Date","End Date","Liability",'damages','Scenario','perc_calc','mm_perc','Dunn_negligent']])
req_data1.rename(columns={
                       "Scenario":"Path","Dunn_negligent":"Plaintiff_negligent"
                         },inplace=True)


# In[ ]:


frames=[newdf1,req_data1]
merge_data = pd.concat(frames, keys=['x', 'y'])

merge_data


# Case Expected Value Damages for the merge data
# Showing the total expected damages mean,median and sd with winrate percentage (entire version)
# 
# 

# In[ ]:


merge_data
merge_data['winrate_percentage']=merge_data.Liability
merge_data['damages_mean']=merge_data.damages+merge_data.perc_calc
merge_data['damages_median']=merge_data.damages
merge_data['damages_sd']=merge_data.damages



winrate_damages_expected=merge_data.groupby('Path').aggregate(
    {'winrate_percentage': np.mean, 'damages_mean': np.mean,'damages_median':np.median,'damages_sd':np.std})


winrate_damages_expected.winrate_percentage*=100
winrate_damages_expected



# In[ ]:


#To retrive data based on the keys:
merge_data.loc['y']


# ## Finding the Damages, mean , median and SD when plaintiff wins for the merge data

# In[ ]:


#req_data['winrate_percentage']=np.mean(req_data.Juror_Response)
#print(req_data)
merge_data['mm_perc'].fillna(1,inplace=True)
merge_data['damages_mean1']=merge_data.damages*pd.to_numeric(merge_data.mm_perc)
merge_data['damages_median1']=merge_data.damages
merge_data['damages_sd1']=merge_data.damages
#print(req_data.mm_perc)

winrate_damages_plaintiffwin=merge_data.loc[(merge_data['Plaintiff_negligent']=='No') & (merge_data['Liability']==1)].groupby('Path').aggregate({'damages_mean1': np.mean,'damages_median1':np.median,'damages_sd1':np.std})


winrate_damages_plaintiffwin


