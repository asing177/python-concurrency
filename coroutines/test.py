def func(prefix): 
    print(f"First part:{prefix}")
    try: 
        while True: 
            name = (yield) 
            if prefix in name: 
                print(name)
    except GeneratorExit:
        print("Closing coroutine!!")
  
co = func("Hello") 
next(co)
co.send("There") 
co.send("Hello There") 