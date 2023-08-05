import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from math import floor,ceil

"""Pie chart"""


def pie(data):
    comment = pd.DataFrame(data)
    comment = pd.DataFrame(data)
    comment = data.dropna()
    comment = pd.DataFrame(comment)
    comment.reset_index()
    comment.shape

    # Comment columns name
    name = list(comment.columns)
    name = ''.join(name)

    # Extracting the sentiment from commnet
    sentimentx = []
    for i in comment[name]:
        i = TextBlob(i)
        polarity = i.sentiment.polarity
        sentimentx.append(polarity)

        # Put sentiment into commnets
    comment['sentiment'] = sentimentx

    # Sentiment amount count
    positive = (comment['sentiment'] > 0).sum()
    negetive = (comment['sentiment'] < 0).sum()
    neutral = (comment['sentiment'] == 0).sum()

    # Comments percentage(%) and Pie chart
    fig1, ax1 = plt.subplots();
    sentiment_amount = [positive, negetive, neutral];
    pie_chart = plt.pie(sentiment_amount, labels=['Positive', 'Negetive', 'Neutral'], autopct='%1.1f%%',
                        shadow=True, startangle=90, radius=1.8, textprops={'fontsize': 18});

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white');
    fig = plt.gcf();
    fig.gca().add_artist(centre_circle);
    plt.title('Comment sentiment percentage(%)', bbox={'facecolor': '0.8', 'pad': 5});

    return pie_chart


def number(data):
    comment = pd.DataFrame(data)
    comment = pd.DataFrame(data)
    comment = data.dropna()
    comment = pd.DataFrame(comment)
    comment.reset_index()
    comment.shape

    # Comment columns name
    name = list(comment.columns)
    name = ''.join(name)

    # Extracting the sentiment from commnet
    sentimentx = []
    for i in comment[name]:
        i = TextBlob(i)
        polarity = i.sentiment.polarity
        sentimentx.append(polarity)

        # Put sentiment into commnets
    comment['sentiment'] = sentimentx

    # Sentiment amount count
    positive = (comment['sentiment'] > 0).sum()
    negetive = (comment['sentiment'] < 0).sum()
    neutral = (comment['sentiment'] == 0).sum()

    sentiment_list = {'postive': positive, 'negetive': negetive, 'neutral': neutral}
    return sentiment_list


def percentage(data):
    comment = pd.DataFrame(data)
    comment = pd.DataFrame(data)
    comment = data.dropna()
    comment = pd.DataFrame(comment)
    comment.reset_index()
    comment.shape

    # Comment columns name
    name = list(comment.columns)
    name = ''.join(name)

    # Extracting the sentiment from commnet
    sentimentx = []
    for i in comment[name]:
        i = TextBlob(i)
        polarity = i.sentiment.polarity
        sentimentx.append(polarity)

        # Put sentiment into commnets
    comment['sentiment'] = sentimentx

    # Sentiment amount count
    positive = (comment['sentiment'] > 0).sum()
    negetive = (comment['sentiment'] < 0).sum()
    neutral = (comment['sentiment'] == 0).sum()

    total = positive + negetive + neutral;

    pop = (positive / total) * 100;
    nep = (negetive / total) * 100;
    nup = (neutral / total) * 100;

    pop = float(pop)

    sentiment_list = {'postive': pop, 'negetive': nep, 'neutral': nup}

    return sentiment_list


"""The analysis"""


def analysis_binary(data):
    comment = pd.DataFrame(data)
    comment = pd.DataFrame(data)
    comment = data.dropna()
    comment = pd.DataFrame(comment)
    name = list(comment.columns)
    name = ''.join(name)

    # Extracting the sentiment from commnet
    sentimentp = []
    for i in comment[name]:
        i = TextBlob(i)
        polarity = i.sentiment.polarity
        if polarity > 0:
            polarity = ceil(polarity)
        if polarity < 0:
            polarity = floor(polarity)
        sentimentp.append(polarity)

    return sentimentp



