grammar = [
        ('S', ['P']),
        ('P', ['(', 'P', ')']),
        ('P', []),
           ]
tokens = ['(', '(', ')', ')']
def shift (tokens, i, x, ab, cd, j):
    if cd == [] or tokens[i] != cd[0]:
        return None
    return (x, ab + [cd[0]], cd[1:], j)

def reductions(chart, i, x, ab, cd, j):
    return [(e[0], e[1] + [e[2][0]] , e[2][1:], e[3]) for e in chart[j] if cd == [] and e[2] != [] and e[2][0] == x]

def closure (grammar, i, x, ab, cd):
    return  [
             (rule[0], [], rule[1], i)
             for rule in grammar if cd != [] and rule[0] == cd[0]
            ]
def addtochart(chart, index, state):
    if state in chart[index]:
        return False
    chart[index] += [state]
    return True
    
def parse(tokens, grammar):
    tokens = tokens + ["end_of_input_marker"]
    chart = {}
    start_rule = grammar[0]
    for i in range(len(tokens) + 1):
        chart[i] = []
    start_state = (start_rule[0], [], start_rule[1], 0)
    chart[0] = [start_state]
    chng = 0
    for i in range(len(tokens)):
        while True:
            changes = False
            for state in chart[i]:
                x = state[0]
                ab = state[1]
                cd = state[2]
                j = state[3]
                
                next_states = closure(grammar, i ,x ,ab, cd)
                for next_state in next_states:
                    changes = addtochart(chart, i , next_state) or changes
                
                next_state = shift(tokens,i,x,ab,cd,j)
                if next_state != None:
                    changes = addtochart(chart,i+1,next_state) or changes
                    
                next_states = reductions(chart, i, x, ab, cd, j)
                for next_state in next_states:
                    changes = addtochart(chart, i, next_state) or changes
                    
            if not changes:
                chng=chng+1
            else:
                chng=0
            if chng>3:
                break
    accepting_state = (start_rule[0], start_rule[1], [], 0)
    return accepting_state in chart[len(tokens)-1]
    
result = parse(tokens, grammar)                    
print result        