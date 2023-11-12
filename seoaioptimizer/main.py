from flask import Flask, render_template, request
from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import openai

app = Flask(__name__)

openai.api_key = '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'



def generate_log(query):
        # Use GPT-3 API to generate log text based on the user's query
        prompt = f"User clicked on query: {query}. Generate a relevant log text."

        # Replace the following line with an actual API call to OpenAI GPT-3
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the appropriate GPT-3 engine
            prompt=prompt,
            max_tokens=150,  # Adjust as needed
            n=1,  # Number of completions to generate
            stop=None,  # Token at which to stop generation
            temperature=0.7,  # Control the randomness of the output (adjust as needed)
            frequency_penalty=0.0,  # Higher value will make output more focused (adjust as needed)
            presence_penalty=0.0,  # Higher value will make output more diverse (adjust as needed)
            log_level="info",  # Change to "debug" for more detailed logs
        )
        generated_log_text = response.choices[0].text.strip()

        return jsonify({'logText': generated_log_text})

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        country = request.form['country']

        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m')

        try:
            # Get Related Queries people are searching.
            related_queries_data = pytrends.related_queries()
            top_related_queries = related_queries_data[keyword]['top']

            # Add sentiment analysis to top_related_queries
            top_related_queries['sentiment'] = top_related_queries['query'].apply(analyze_sentiment)

            # Keyword Suggestion
            suggestion_data = pytrends.suggestions(keyword=keyword)
            suggestions_df = pd.DataFrame(suggestion_data)

            # Real-time trending searches
            trending_searches = pytrends.trending_searches(pn=country.lower())

            # Plotting chart
            top_related_queries_chart = px.bar(top_related_queries, x='query', y='value', title='Top Related Queries')

            return render_template('result.html', keyword=keyword, country=country,
                                   top_related_queries=top_related_queries,
                                   top_related_queries_chart=top_related_queries_chart.to_json(),
                                   suggestions=suggestions_df.to_html(), trending_searches=trending_searches)

        except KeyError as e:
            error_message = f"Error: Country code '{country}' is not recognized. Please provide a valid country code."
            return render_template('error.html', error_message=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
