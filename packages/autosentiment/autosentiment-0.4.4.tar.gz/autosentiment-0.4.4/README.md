##Automate sentiment analysis tool
* Author : Sazin Reshed Samin <sazinsamin50@gmail.com>


#autosentiment is an open source library that generates sentiment type(positive,negetive,neutral) pie char,percentage,number and ternary value for pandas dataframe text portion.


- Usage
For analysis the seintiment type in positive,negetive or neutral


- Setup in normal environment and command window:
```
pip install autosentiment
```


- Setup in jupyter notebook:
```
!pip install autosentiment
```


- Import library : 
```
import autosentiment as at
```


- The library is pandas dataframe dependent.
```
Have to get dataframe('text columns') and give to command.
Like df['text]
```




#Features
- sentiment type pie chart :
```
at.pie()
```

- sentiment type amount : 
```
at.number()
```


- sentiment percentage :
```
at.percentage()
```


- An example usages
```
>>import autosentiment as at
>>import pandas as pd

>>df=pd.read_csv("dataset_2.csv")


>>number=at.number(df['text'])
>>print(number)

>>{'postive': 1087, 'negetive': 684, 'neutral': 1492}

>>percen=at.percentage(df['text'])
>>print(percen)
>>postive': 33.31, 'negetive': 20.96, 'neutral': 45.72}


>>analysis=at.analysis_ternary(df['text'])
>>analysis

>> [1,
 0.0,
 1,
 1,
 1,
 -1,
 1,
 -1,
 0.0,
 ...]
```


