import sys
import os
import json
import random
import textwrap
from collections import Counter
if sys.version < '3':
    _input = raw_input
else:
    _input = input

# -----------------------------------------------------------------------------

def wrapped_out(i, s):
    lead = '{0}. '.format(i)
    wrapper = textwrap.TextWrapper(initial_indent=lead,
                                   subsequent_indent=' ' * len(lead))
    s = wrapper.fill(s)
    print(s)

def ask(i, q):
    os.system('cls' if os.name == 'nt' else 'clear')

    wrapped_out(i, q['text'])
    print('\n')

    for k in sorted(q['options']):
        wrapped_out(k, q['options'][k])
    print('\n')

    if sys.version < '3':
        a = raw_input('> ').upper().translate(None, ' ,')
    else:
        a = input('> ').upper().translate({ord(' '): None, ord(','): None})

    return [x for x in a]

def check(q, a):
    compare = Counter(q['answers']) == Counter(a)
    return 1 if compare else 0

def reveal(q, a, s):
    print('Correct' if s else 'Incorrect')
    if not s:
        print(', '.join(sorted(q['answers'])))
    _input("'Enter' to continue")

# -----------------------------------------------------------------------------

def run():
    with open('questions.json') as f:
        questions = json.load(f)

    total = 0
#    exam_length = 40
    exam_length = int(sys.argv[1]) if len(sys.argv) >1 else 40
    passing = (exam_length * 65) / 100
    study_guide = {}

    exam = random.sample(questions, exam_length)
    for i, question in enumerate(exam):
        answer = ask(i + 1, question)
        score = check(question, answer)
        total += score
        #reveal(question, answer, score)
        
        correct_answers = ''
        for correct_answer in question['answers']:
            correct_answers+= question['options'][correct_answer]+" | "
            
        if not score:
            study_guide[i+1] = question['text']+" (answers: "+correct_answers+")"

    print('Your score: {0} of {1}'.format(total, exam_length))
    print('Passed!' if total >= passing else 'Failed')

    print('\nMisses\n')
    for i,review in study_guide.items():
        wrapped_out(i, review)

if __name__ == '__main__':
    run()
