consumer_key = 'K2RVWcYTGp0QIzylLWqyzipnDfubTzy06vx7MqKb'
consumer_secret = 'AJDC5d3vVX84xiazuZZGBvCfPI9iiu3ZnUVgRvXi'


from splitwise import Splitwise

import oauth2 as oauth
sObj = Splitwise("K2RVWcYTGp0QIzylLWqyzipnDfubTzy06vx7MqKb","AJDC5d3vVX84xiazuZZGBvCfPI9iiu3ZnUVgRvXi")
'''Consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(Consumer)'''
sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
sObj.setAccessToken(session['access_token'])
id = 7123
user = sObj.getUser(id)