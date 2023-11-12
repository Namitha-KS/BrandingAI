import pytrends
from pytrends.request import TrendReq
import pandas as pd

import openai

openai.api_key = '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'

pytrends = TrendReq(hl='en-US', tz=360)


# Get Related Queries people are searching.
kw_list = ["machine learning"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')

data  = pytrends.related_queries()

print(data['machine learning']['top'])

# Keyword Suggestion
keywords = pytrends.suggestions(keyword='Business Intelligence')
df = pd.DataFrame(keywords)
print(df['query'][0])



# real time trending searches


print(pytrends.trending_searches(pn='united_states'))
pytrends.trending_searches(pn='japan') # Japan

