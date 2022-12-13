import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


account_sid = "twilio_account_sid"
auth_token = "twilio_auth_token"

api_key = "your_stock_api_key"
alpha_url = "https://www.alphavantage.co/query"
stock_parameters = {
    'function': "TIME_SERIES_DAILY_ADJUSTED",
    'symbol': STOCK,
    'apikey': api_key
}

response_stock = requests.get(alpha_url, params=stock_parameters)
response_stock.raise_for_status()
stock_data = response_stock.json()
daily_data = stock_data['Time Series (Daily)']

# News api Key
news_api_key = "your_news_api_key"
news_url = "https://newsapi.org/v2/everything"
news_parameters = {
    'qInTitle': COMPANY_NAME,
    'from': '2022-11-13',
    'sortBy': 'publishedAt',
    'apiKey': news_api_key
}

news_response = requests.get(news_url, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

yesterday_stock = (daily_data[(list(daily_data.keys())[0])]['4. close'])
before_yesterday_stock = (daily_data[(list(daily_data.keys())[1])]['4. close'])

def calculate_probability():
    global yesterday_stock, before_yesterday_stock
    difference = (float(yesterday_stock) * 100) / float(before_yesterday_stock)
    prob = round(100 - difference)
    return prob


if calculate_probability() > 5:
    count = 0
    while count < 3:
        percentage_change = str(calculate_probability())
        body_message = news_data['articles'][count]['title']
        if float(yesterday_stock) - float(before_yesterday_stock) > 0:
            body_message = "🔺" + body_message
        else:
            body_message = "🔻" + body_message
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"TSLA: {percentage_change}%\n Headline: {body_message}",
            from_='twilio_provider_phone_number',
            to='your_phone_number'
        )
        count += 1
