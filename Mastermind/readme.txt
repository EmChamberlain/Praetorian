Matthew Chamberlain
mattchamberlain2@gmail.com / mattcham@umich.edu
https://github.com/MattChamberlain


Usage: python Mastermind.py 
I developed using python 3.5.2 but I suspect any python3 version will work.


I have played a version of Mastermind before. The version I have played had the same rules as this. For each color you got exactly correct both color and position you got a black circle. For each color you got correct in color but not position you got a white circle. The main difference in this game is that I had to handle two main issues, the guess limit and the number of weapons.

Guess Limit:
I handled the guess limit mostly by using the Five-guess Algorithm (https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm) I would choose my next guess based on a score that estimated the amount of information gained if I guessed that permutation. Once I guessed, I would prune the set of all possible correct permutations by checking the permutations against my guess and seeing if the permutation conformed to the response to my guess.

Construction of S:
s was the set of all possible permutations of weapons. Because of this, the size of s blows up with large numbers of weapons. I was limited to a time of 10 seconds before I lost the level so I had to come up with a way to construct s using a heuristic if the number of weapons was greater than around 15. My solution involved guessing a number of "trash" guesses so that I could narrow down the possible weapon combinations. After the "trash" guesses I was able to construct a massively smaller s. I do not think that this is an optimal construction of s, only that it is good enough and I just use the full s if the number of weapons is <= 15.

 
 Overall, I enjoyed this challenge a lot. Even though I have played manual Mastermind before I have never written anything to solve it automatically.
 
 
I have made my github repo for this challenge public. Let me know at one of the above emails if you would prefer I made it private. If there are any questions not answered in this readme or in the comments, feel free to email me.

Anyone should be able to generate more hashes using Mastermind.py and looking at stdout for a line that starts with "Hash: ". Seems like the hash is based on email so you will need to change that.

Hash:
c6a61a35a727bdfd18a77860acd1f2136f57787a486e5e50e929445412dcb7977b2275736572223a20226d6174746368616d6265726c61696e3240676d61696c2e636f6d227d
