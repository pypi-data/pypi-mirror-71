# twitter_activity

You can use this library in order to :

  - Register, get, and delete the webhook url 
  - Make a user subscribe his account for the twitter activity API 
  - Classify twitter account activities
  
*In order to install, open the command prompt and type:*
```
pip install twitter_activity
```

It  has two main module:

  - webhook_manager
  - activity_manager

In order to use this library  you should have a verified twitter application and you have to save your credential  inside a json file as following:
 ```
 {
"consumer_key": " your one", 
"consumer_secret": "your one", 
"access_token": "your one", 
"access_token_secret": "your one",
"env_name": "your one"
}
```

The following [Notebook](https://github.com/Samer92/twitter_activity/blob/master/Example/setup.ipynb) shows multiple example about how to use webhook_manager modules

