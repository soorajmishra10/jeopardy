import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jeopardy.settings')

import django
django.setup()

from game.models import Question

question_file = open('jeopardy_questions.json', 'r')
data = question_file.read()

obj = json.loads(data)

l = len(Question.objects.all())
for o in range(len(obj)):
    q = Question(question_no=(l+o+1), question=obj[o]['clue'], answer=obj[o]['answer'], points=obj[o]['points'], category=obj[o]['tag'])
    q.save()





