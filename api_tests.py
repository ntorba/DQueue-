from votr import db, votr, Topics, Polls
import requests

db.app = votr
db.init_app(votr)


polls = Topics.query.join(Polls).all()
for num,poll in enumerate(polls):
    print(num, poll)

r = requests.patch('http://localhost:5000/api/poll/vote', json={"poll_title": "Which side is going to win the EPL this season", "option": "Spurssss"})
print(r)
print(r.text)

print('OPTIONS ENDPOINT')
r = requests.get('http://localhost:5000/api/polls')
print(r)
print(r.text)

#r = requests.get('http://localhost:5000/api/polls')
#print(r)
#print(r.json())

#r = requests.post('http://localhost:5000/api/polls', json={"title": "who's the fastest footballer","options": ["Hector bellerin", "Gareth Bale", "Arjen robben"]})
#print(r)
#print(r.text)

#r = requests.get('http://localhost:5000/api/polls')
#print(r)
#print(r.json())




