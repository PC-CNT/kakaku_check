from bs4 import BeautifulSoup
import datetime
import requests
import json
import os

j = {}

default = {
	'labels': [],
	'datasets':[
		{
			'title':'Switch',
			'color':'red',
			'values':[],
		},
		{
			'title':'PS4',
			'color':'blue',
			'values':[],
		},
		{
			'title':'PS5',
			'color':'grey',
			'values':[],
		},
		{
			'title':'STEAM',
			'color':'purple',
			'values':[],
		},
	],
}

#============================================================

def price_get(load_url):
	if load_url == '':
		return False

	html = requests.get(load_url)
	data = BeautifulSoup(html.content, "html.parser")

	if r'https://store.playstation.com/' in load_url:
		P = int( data.find(class_="psw-t-title-m").text.replace(r'￥', r'').replace(r',', r'') )

	elif r'https://store-jp.nintendo.com/list/software/' in load_url:
		P = int( data.find(class_="productDetail--detail__price js-productMainRenderedPrice").find('span').text.replace(r',', r'') )
	
	elif r'https://store.steampowered.com/app/' in load_url:
		P = int( data.find(class_="game_purchase_price").text.replace(r'¥', r'').replace(r',', r'').replace('\t', r'').replace(' ', r'').replace('\r\n', r'') )

	else:
		P = False

	return P

#============================================================

with open('__game.csv', 'r', encoding='shift_jis') as c:
	for line in c:
		if not '----------タイトル----------' in line:#最初の行だけ飛ばしたいので
			l = line.split(r',')
			t = l[0] + '.json'

			if not os.path.exists(t):#なかったら作る
				with open(t, 'w') as f:
					f.write( json.dumps(default) )

			with open(t, 'r') as f:
				j = json.loads(f.read())

				d_today = ( str(datetime.date.today())[2:] ).replace(r'-', '')#日付を持ってくる
				
				if not d_today in j['labels']:#今日の日付がないなら(≒一日2回以上書き込まないにする)
					j['labels'] += [ d_today ]


					j['datasets'][0]['values'] += [ price_get(l[1]) ]
					j['datasets'][1]['values'] += [ price_get(l[2]) ]
					j['datasets'][2]['values'] += [ price_get(l[3]) ]
					j['datasets'][3]['values'] += [ price_get(l[4]) ]

					with open(t, 'w') as f:
						f.write( json.dumps(j) )

					print(j)







			



#with open('kakaku.json', 'w') as f:
#	f.write( json.dumps(j) )

#d_today = ( str(datetime.date.today())[2:] ).replace(r'-', '')
#print(d_today, price_get("https://store.steampowered.com/app/391540/Undertale/"))
#print(d_today, price_get("https://store-jp.nintendo.com/list/software/70010000009922.html"))
#print(d_today, price_get("https://store-jp.nintendo.com/list/software/70010000009922.html"))
#print(d_today, price_get("https://store.playstation.com/ja-jp/product/JP0215-CUSA09239_00-TFSHVCUTPS4JP084"))
#print(d_today, price_get(""))
