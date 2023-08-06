# pixabay.py

api still in progress. examples in test.py for every function

To get an API key for pixabay, go to https://pixabay.com/api/docs/

Make an account, and then go to the parameters for image searching. One of the values should say 'key', with your api key. When creating a pixabay client, just input your API key

example: pixaclient = pixabay.Client(api_key=os.get_env("API_KEY"))

Then you should be good to go! You can use all of the functions in examples.py
,