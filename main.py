import tweepy, dotenv, os, time

def get_reset_time_from_headers(headers: dict) -> str:
    epoch_reset_time = headers.get('x-rate-limit-reset')
    reset_time = 'Unknown'
    if epoch_reset_time:
        reset_time = time.strftime('%d-%m-%Y %H:%M:%S',
                                   time.gmtime(float(epoch_reset_time)))
        reset_time += ' GMT'
    return reset_time

print('Starting script...')
# Loading .env file
dotenv.load_dotenv()

#OAuth 1.0a
client = tweepy.Client(consumer_key=os.getenv('CONSUMER_KEY'),
                       consumer_secret=os.getenv('CONSUMER_SECRET'),
                       access_token=os.getenv('ACCESS_TOKEN'),
                       access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))

tweet_id = input("Type in an ID of a tweet you want to like: ")

try:
    print("Sending a request to the API...")
    response = client.like(tweet_id=tweet_id, user_auth=True)
    if response.data.get("liked"):
        print(f"Tweet {tweet_id} is liked successfully")
except tweepy.errors.TwitterServerError as err:
    print(f"Error: Something wrong with API. Code: {err.response.status_code}")
except tweepy.errors.HTTPException as err:
    print(f"Error: {err.response.reason}")
    status_code = err.response.status_code
    match status_code:
        case 429:
            print("Rate limit exceeded")
            print(f"Reset at: {get_reset_time_from_headers(err.response.headers)}")
        case 401:
            print("Failed to authorize. Please check your tokens")
except TypeError as err:
    print(f"Error: {repr(err)}.")
    print("Please check .env file")
except Exception as err:
    print(f"Error: {repr(err)}")

print('My job is done.')