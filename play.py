import solver

colorConversion = {0: 'Red', 1: 'Green', 2: 'Blue', 3: 'Yellow', 4: 'Black', 5: 'White'}
colorConversionReverse = dict((v,k) for k,v in colorConversion.items())

s = solver.mini_max()

while True:
    guess = s.makeGuess()
    print("Make guess %s" % " ".join([colorConversion[a] for a in guess]))

    val = input("Input result from game 'Black Pegs, White Pegs' e.g. '12' for 1 black and 2 white or press 'q' to quit\n")
    
    if val[0].lower() == 'q':
        break
    else:
        try:
            s.adjustMoves(guess, [int(a) for a in list(val)])
        except KeyError:
            print("Not a valid color")
        