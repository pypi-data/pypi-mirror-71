Automate sentiment analysis tool


Usage
For analysis the seintiment type in positive,negetive or neutral

Setup in normal environment and command window:
```
pip install automatic_sentiment
```


Setup in jupyter notebook:
```
!pip install automatic_sentiment
```


Import library : 
```
import automatic_sentiment as at
```


The library is pandas dataframe dependent.
```
Have to get dataframe('text columns') and give to command.
Like df['text]
```





sentiment type pie chart :
```
at.pie()
```

sentiment type amount : 
```
at.number()
```


sentiment percentage :
```
at.percentage()
```


An example
```
at.pie(df['text'])
```
