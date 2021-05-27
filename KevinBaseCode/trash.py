import key_input

with key_input.KeyPoller() as keyPoller:
    while True:
        c = keyPoller.poll()
        if not c is None:
            if c == "c":
                break
            print (c)