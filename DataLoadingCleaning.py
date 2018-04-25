
# coding: utf-8
import pandas as pd

# Read jury data 
jury_data1 = pd.read_csv('jury_data.csv', encoding= 'ISO-8859-1',skiprows=[0,2])
jury_data1.head(5)

## To describe columns
jury_data1.columns

jury_data1.describe()

# To check data type of each columns.
print(data.dtypes)

## Changing Data type
data['End Date'] = pd.to_datetime(data['End Date'])
data['Start Date'] = pd.to_datetime(data['Start Date'])
data.dtypes

## stating code for quater 2

import pandas as pd
df =pd.read_csv('jury2.tsv', sep='\t+',skiprows=[0,2, 4]+list(range(1,1614,2)) + [1614], names = ['StartDate', 'EndDate',
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
       'Was the Carve 3000 snowboard X5 sold Connor McNeil defective?',
       "Was the defect(s) a substantial factor in causing Connor McNeil's injuries?",
       'non_economic_damages_suffered',
       'Please write your answer to the preceding damages question in words (quality check).',
       'Was Connor McNeil negligent?',
       'Was Connor McNeil negligence a substantial factor in causing her own injuries?',
       'What percentage of responsibility for Connor McNeil injuries was each party responsible for? (Answers should add up to 100%) - X5',
       'What percentage of responsibility for Connor McNeil injuries was each party responsible for? (Answers should add up to 100%) - Connor McNeil',
       'Was the Carve 3000 snowboard X5 sold Connor McNeil defective?.1',
       "Was the defect(s) a substantial factor in causing Connor McNeil's injuries?.1",
       'What economic damages did Connor McNeil suffer?  (in dollars)',
       'Please write your answer to the preceding damages question in words (quality check)..1',
       'What non-economic damages did Connor McNeil suffer? (in dollars)',
       'Please write your answer to the preceding damages question in words (quality check)..2',
       'Please explain why you arrived at your decision? (50 character minimum)',
       'Did the fact that X5 added core inserts to the later Carve 3000 model, affect your view as to whether the original Carve 3000 was defective?',
       'Were you able to ignore the  fact that X5 added core inserts to the later Carve 3000 model when deciding whether the original Carve 3000 was defective?',
       'Path'])
        
## Data type
df.dtypes

## check column names 
print (df.columns)

# Null Checking
any(df.isnull().any())

## replacing hexadecimal value of damages to ''
for i in range(len(df['non_economic_damages_suffered'])):
    df['non_economic_damages_suffered'].values[i] = df['non_economic_damages_suffered'].values[i].replace('\x00','')
    df['Path'].values[i] = df['Path'].values[i].replace('\x00','') ;  
    df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?'].values[i] =  df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?'].values[i].replace('\x00','') ;  
    
# replacing NAN value to 0 for path to change the datatype to int
df['Path'].fillna(0,inplace = True)


df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?'].fillna(-1,inplace = True)


## Changing Data type
df.StartDate = pd.to_datetime(df.StartDate)
df.EndDate = pd.to_datetime(df.EndDate) 
df.non_economic_damages_suffered = pd.to_numeric(df.non_economic_damages_suffered)
df.Path =  df.Path.astype(int)
df.dtypes
# everything is nice

#df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?'] = df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?'].astype(int)
df['Was the Carve 3000 snowboard X5 sold Connor McNeil defective?']

t = map( filter(lambda x: len(str(x)) == 1, df['non_economic_damages_suffered'].values),0)

## To merge both data set(work in progress): 
jury_data1.shape
df.shape

## Test code to convert currency in word to integer value (work in progress): 

newdf = df.filter(['What non-economic damages did Connor McNeil suffer? (in dollars)','Please write your answer to the preceding damages question in words (quality check)..2'], axis=1)
newdf['Newcol'] = 0
newdf.columns = ['a', 'b', 'c']
newdf.head()

from word2number import w2n
a = "2 hundred thousand dollars"
lst = list(range(1,1000))
t = a.split
print(t)
try:
    print(w2n.word_to_num(a))
except:
    print("error occur")
df.columns

for index,row in newdf.iterrows():
    word = row['b']
    print(row['b'])
    try:
        row['c'] = w2n.word_to_num(word)
    except:
        print("error occur", word)
newdf['c'].unique

