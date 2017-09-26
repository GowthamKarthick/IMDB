from __future__ import division
import requests
import json
from bs4 import BeautifulSoup
import os
import sys
class IMDBparser:

	all_movies_details={}
	mov_list=[]
	final_list={}
	count=0
	user_gen=[['Love','Action','Drama'],[0,0,0]]

	def __init__(self,mov_list):
		self.movies_list=mov_list
		self.mov_list=mov_list
		self.movies_count=len(mov_list)
	
		
	def prioritizing_movies(self):
		self.final_list=sorted(self.all_movies_details.items(), key=lambda a: a[1]['sys_rating'], reverse=True)
		return self.final_list


	def calculate_genre_rating(self):
		for allmovies in self.all_movies_details:
			self.count=0
			genval=0
			for usergen in self.user_gen[0]:
				for movgen in self.all_movies_details[allmovies]["movie_genre"]:
					if usergen == movgen:
						self.count = self.count + self.user_gen[1][genval]
				genval +=  1
			self.all_movies_details[allmovies]["sys_rating"] += float(self.count)
			
	
	def init_user_genre(self,usr_gen):
			self.user_gen=usr_gen

	
	def get_each_movie_name(self):
		
		for movies in self.movies_list:
			id=self.get_movie_id(movies)
			if id != "False":
				info=self.get_movie_details(id)			
			else:
				info={'movie_name':movies,
				'movie_rating':0.0,
				'movie_genre':[],
				'movie_year':0,
				'movie_meta_score':0,
				'sys_rating':0}
			self.all_movies_details.update({movies:info})

		

	def get_movie_id(self,movie_name):
		results = requests.get('http://www.omdbapi.com/?t='+movie_name+'&y=&plot=short&r=json')
		dictionary = json.loads(results.content)
		Response = str(dictionary["Response"])
		if Response  == "True":
			movie_id=str(dictionary["imdbID"])
			return movie_id
		else:
			return "False"

	def get_movie_details(self,movie_id):
		results = requests.get('http://www.imdb.com/title/'+movie_id)
		soup = BeautifulSoup(results.content,"html.parser")
		genre_list = self.get_movie_genre(soup)
		r_val = self.get_rating(soup)
		meta_score = self.get_meta_score(soup)
		year = self.get_release_year(soup)
		name = self.get_movie_name(soup)
		our_rate = (year/1000)+(r_val/10)+(meta_score/100)

		dic={'movie_name':name,
		'movie_rating':r_val,
		'movie_genre':genre_list,
		'movie_year':year,
		'movie_meta_score':meta_score,
		'sys_rating':our_rate}
		return dic

	def get_movie_name(self, soup):
		name = soup.find('h1',attrs={"itemprop":"name"})
		name=name.text
		return name

	def get_rating(self, soup):
		r_val = soup.find('span',attrs={"itemprop":"ratingValue"})
		r_val=float(str(r_val.text))
		return r_val

	def get_release_year(self, soup):
		year = soup.find('span',attrs={"id":"titleYear"})
		year = year.find('a')
		year = int((year.text).strip())
		return year

	def get_meta_score(self, soup):
		meta_score = soup.find('div',attrs={"class":"metacriticScore score_favorable titleReviewBarSubItem"})
		meta_score1 = soup.find('div',attrs={"class":"metacriticScore score_mixed titleReviewBarSubItem"})
		m_score = -1
		c = len(str(meta_score))
		c1 = len(str(meta_score1))
		if ((c == 4) & (c1==4) ):
			m_score = 0
		elif(c==4):
			meta_score1 = str(meta_score1.text.strip())
			meta_score1 = int(meta_score1)
			m_score = meta_score1
		else :
			meta_score = str(meta_score.text.strip())
			meta_score = int(meta_score)
			m_score = meta_score
		
		return m_score

	def get_movie_genre(self, soup):
		genre = soup.find('div',attrs={"itemprop":"genre"})
		genre_list = []
		if genre != None:
			genre_li=genre.find_all('a')
			length=len(genre_li)
			genre_list=[]

			for gen in genre_li:
				genre_list.append(str(gen.text).strip())

		return genre_list	
	
print "IMDB PARSER"

movie_path = "" 
while(True):
	movie_path = raw_input("Give me a path")
	if (movie_path == ""):
		movie_path = os.getcwd()
		break
	else:
		isvalid = os.path.isdir(movie_path)
		if(isvalid==False):
			print "Ivalid Directory"
			continue
		break


movie_list = []
for movies in os.listdir(movie_path):
	movie_name=movies.split(".")
	movie_list.append(movie_name[0])
user_genre = [['Action','Adventure','Animation','Comedy','Crime','Family','Fantasy','History','Horror','Romance','Sci-Fi','Sport','Thriller','War'],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
print user_genre
print "Want to change Priority ?" 
print "[1 -> Change]"

genre_choice = raw_input("Want to change Priority ? [y/n]")
genre_choice = str(genre_choice)
if(genre_choice == 'Y' or genre_choice == 'y'):
	for num in range(1,14):
		print "Current : ",user_genre[0][num],":",user_genre[1][num]
		print "New : ",user_genre[0][num],":"
		user_genre[1][num] = raw_input()
		user_genre[1][num] = int(user_genre[1][num])


print "Processing....."
obj=IMDBparser(movie_list)
obj.get_each_movie_name()
obj.init_user_genre(user_genre)
obj.calculate_genre_rating()
res=obj.prioritizing_movies()
print "Done..."
print "Got "+str(len(res)-1)+" Movies !!!!"
while(True):
	choice = raw_input("How many movies want to display ? [press enter to show all movies ]")
	choice = int(choice)
	if(choice > len(res)-1):
		print "Choice more than movie count"
		continue
	break

if(choice == ""):
	for movie in res:
		print movie[0]
else:
	for i in range(int(choice)):
print res[i][0]