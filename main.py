import redis
import requests

token = '68b47eb3b1f697ab426e102486f11c68fb3dc5b1'
q = f'http://api.waqi.info/feed/Roma/?token={token}'

response = requests.get(q)

print(response.text)

#r = redis.Redis(host='127.0.0.1', port=6379