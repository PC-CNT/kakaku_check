from bs4 import BeautifulSoup
import datetime
import requests
import json
import os

j = {}
#============================================================

def price_get(load_url):
	if load_url == '':
		return

	html = requests.get(load_url)
	data = BeautifulSoup(html.content, "html.parser")

	if r'https://store.playstation.com/' in load_url:
		P = int( data.find(class_="psw-t-title-m").text.replace(r'￥', r'').replace(r',', r'') )

	elif r'https://store-jp.nintendo.com/list/software/' in load_url:
		P = int( data.find(class_="productDetail--detail__price js-productMainRenderedPrice").find('span').text.replace(r',', r'') )
	
	elif r'https://store.steampowered.com/app/' in load_url:
		price = data.find(class_="game_purchase_price")

		if not price:#セール時
			price = data.find(class_="discount_final_price")

		P = int( price.text.replace(r'¥', r'').replace(r',', r'').replace('\t', r'').replace(' ', r'').replace('\r\n', r'') )

	else:
		P = False

	return P


def get_hardware(x):
	for i,d in enumerate( j['datasets'] ):
		keys = [k for k, v in d.items() if v == x]
		if keys:
			r = i
	
	return r

#============================================================

with open('__game.csv', 'r', encoding='UTF-8') as c:
	for line in c:
		if not '----------タイトル----------' in line:#最初の行だけ飛ばしたいので
			l = line.split(r',')
			t = l[0] + '.json'

			if not os.path.exists(t):#なかったら作る
				j_set = {'labels': [], 'datasets':[] }

				if l[1]:
					j_set['datasets'] += [ {'title':'Switch', 'color':'red', 'values':[],} ]
				if l[2]:
					j_set['datasets'] += [ {'title':'PS4', 'color':'blue', 'values':[], } ]
				if l[3]:
					j_set['datasets'] += [ {'title':'PS5', 'color':'gray', 'values':[], } ]
				if l[4]:
					j_set['datasets'] += [ {'title':'STEAM', 'color':'purple', 'values':[],} ]

				with open(t, 'w') as f:
					f.write( json.dumps(j_set) )


			with open(t, 'r') as f:
				j = json.loads(f.read())

				d_today = ( str(datetime.date.today())[2:] ).replace(r'-', '')#日付を持ってくる
				
				if not d_today in j['labels']:#今日の日付がないなら(≒一日2回以上書き込まないにする)
					j['labels'] += [ d_today ]

					if l[1]:
						j['datasets'][get_hardware('Switch')]['values'] += [ price_get(l[1]) ]
					if l[2]:
						j['datasets'][get_hardware('PS4')]['values'] += [ price_get(l[2]) ]
					if l[3]:
						j['datasets'][get_hardware('PS5')]['values'] += [ price_get(l[3]) ]
					if l[4]:
						j['datasets'][get_hardware('STEAM')]['values'] += [ price_get(l[4]) ]

					with open(t, 'w') as f:
						f.write( json.dumps(j) )
