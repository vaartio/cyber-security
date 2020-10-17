from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json
import sqlite3
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

def add_feedback(author, feedback):
	conn = sqlite3.connect('./src/db.sqlite3')
	cur = conn.cursor()
	# A solution for Cross-Site Scripting issue.
	# feedback = strip_tags(feedback)
	cur.executescript("INSERT INTO Feedback (author, content) VALUES ('"+author+"','"+feedback+"')")
	# A solution for SQL injection issue.
	# cur.execute("INSERT INTO Feedback (author, content) VALUES (:author, :feedback)", { 'author': author, 'feedback': feedback })
	conn.commit()

def read_feedback(author):
	conn = sqlite3.connect('./src/db.sqlite3')
	cur = conn.cursor()
	cur.execute("SELECT author, content FROM Feedback WHERE author='"+author+"' ORDER BY id")
	# A solution for SQL injection issue.
	# cur.execute("SELECT author, content FROM Feedback WHERE author=:author ORDER BY id", { 'author': author })
	rows = cur.fetchall()
	feedbacks = []
	for row in rows:
		feedbacks.append({ 'author': row[0], 'content': row[1] })
	return feedbacks

@login_required
@csrf_exempt
def homePageView(request):
	if request.method == 'POST':
		author = request.POST.get('author')
		# A solution for Broken Access Control issue.
		# author = str(request.user)
		feedback = request.POST.get('content')
		add_feedback(author, feedback)

	context = {}
	context['feedbacks'] = read_feedback(str(request.user))
	context['author'] = str(request.user)
	return render(request, 'pages/index.html', context)
