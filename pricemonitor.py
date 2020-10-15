import requests #connects to url
from bs4 import BeautifulSoup
import smtplib #simple mail protocol
import time


URL = 'https://www.amazon.ca/BOSOBO-Paintbrushes-Watercolor-Miniature-Detailing/dp/B07GH7WGC3/ref=sr_1_2?dchild=1&keywords=paint+brush&qid=1602734635&s=amazon-devices&sr=1-2&tag='

# no longer works sept 2020 as amazon blocks any illegitimate user-agents
# headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip', 
'DNT' : '1', # Do Not Track Request Header 
'Connection' : 'close'}

desired_price = float(input("Inform you when price drops below..."))
sentmail = False

def check_price():
	page = requests.get(URL, headers = headers)
	# soup = BeautifulSoup(page.content, 'html.parser')
	soup = BeautifulSoup(page.content, 'html5lib')
	title = soup.find(id = "productTitle").get_text()
	title = title.strip()

	price = soup.find(id ="priceblock_ourprice").get_text() #returns a string
	price = float(price[5:13]) #returns a number
	seller = soup.find(id = 'bylineInfo').get_text()

	if(price <= desired_price):
		send_email(title, seller, price)


def send_email(title, seller, price):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo() #command sent by email server to identify itself when connecting to another email
	server.starttls() #encrypts connection
	server.ehlo()

	server.login('juliemo1583@gmail.com', 'nmbroykfoniebgao')
	subject = "Price has dropped!"
	body = title + ' by ' + seller + ' is now only ' + str(price) + '! \nCheck out ' + URL + '!'
	message = 'Subject: {} \n\n {}'.format(subject, body)
	server.sendmail('juliemo1583@gmail.com', 
					'b3w0b@ugrad.cs.ubc.ca', 
					message
					)
	sentmail = True
	print('Email has been sent!')
	server.quit()


while(sentmail == False):
	check_price()
	time.sleep(60*60*8) #checks price every 8 hours
