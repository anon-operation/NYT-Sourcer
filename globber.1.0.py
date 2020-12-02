
## Splitting instructions:
## use: split -l 10000 inputFile outputPrefix


import glob

reads=glob.glob("split_*")

with open("reglobbed.sqlite", "wb") as outfile:
    for f in reads:
        with open(f, "rb") as goingIn:
            outfile.write(goingIn.read())

print("The globulator is done.")
