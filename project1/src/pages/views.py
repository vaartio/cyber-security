from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
#from .models import Account
#from django.db.models import Q
import json
import sqlite3

#@login_required
#def addView(request):
#	acc = Account.objects.create(owner=request.user, iban=request.POST.get('iban'))
#
#	return redirect('/')


#@login_required
#def homePageView(request):
#	accounts = Account.objects.filter(owner=request.user)
#	return render(request, 'pages/index.html', { 'accounts': accounts, })

def add_feedback(author, feedback):
	conn = sqlite3.connect('./src/db.sqlite3')
	cur = conn.cursor()
	cur.execute("INSERT INTO Feedback (author, content) VALUES ('"+author+"','"+feedback+"')")
	conn.commit()

def read_feedback(author):
	conn = sqlite3.connect('./src/db.sqlite3')
	cur = conn.cursor()
	cur.execute("SELECT author, content FROM Feedback WHERE author='"+author+"' ORDER BY id")
	rows = cur.fetchall()
 
	feedbacks = []
	for row in rows:
		feedbacks.append({ 'author': row[0], 'content': row[1] })
 
	print(feedbacks)
	return feedbacks

@login_required
def homePageView(request):
	if request.method == 'POST':
		author = request.POST.get('author')
		feedback = request.POST.get('content')
		add_feedback(author, feedback)

	context = {}
	context['feedbacks'] = read_feedback(str(request.user))
	context['author'] = str(request.user)
	return render(request, 'pages/index.html', context)
