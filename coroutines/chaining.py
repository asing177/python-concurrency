def producer(sentence, next_coroutine): 
    ''' 
    Normal Func which Initiates the Chain
    A Producer which just split strings and 
    feed it to parse_token coroutine 
    '''
    tokens = sentence.split(" ") 
    for token in tokens: 
        next_coroutine.send(token) 
    next_coroutine.close() 
  
def parse_token(pattern="ing", next_coroutine=None): 
    ''' 
    Search for pattern in received token  
    and if pattern got matched, send it to 
    print_token() coroutine for printing 
    '''
    print(f"Matching Pattern is {pattern}") 
    try: 
        while True: 
            token = (yield) 
            if pattern in token: 
                next_coroutine.send(token) 
    except GeneratorExit: 
        print("Parsing completed!!") 
  
def print_token(): 
    ''' 
    Act as a sink, which simply prints the 
    received tokens 
    '''
    print("Starting with Sink !!") 
    try: 
        while True: 
            token = (yield) 
            print(token) 
    except GeneratorExit: 
        print("Sink Finished!!") 
  
pt = print_token() 
next(pt) 
pf = parse_token(next_coroutine = pt) 
next(pf) 
  
token = "Bob is running behind a fast moving car"
producer(token, pf) 
