Matthew Chamberlain
mattchamberlain2@gmail.com / mattcham@umich.edu
https://github.com/MattChamberlain


Usage: python ROTA.py 
I developed using python 3.5.2 but I suspect any python3 version will work.


I played a number of manual games to get acquainted with the game. I discovered that as long as I kept my pieces separated from one another, and not in the middle spot, I could keep the game going forever. I abused this extremely basic strategy to force every game into a "win" (> 30 turns) for me. I had two sections to my strategy. 

The first section was the opening strategy. I placed pieces according to a few basic rules. The initial piece is placed next to an existing enemy piece or placed in the south spot. The second piece is placed so as to stop a win condition for the enemy or it is placed to box in an enemy piece. The third piece is placed to stop a win condition for the enemy or it is placed to keep distance between all of my friendly pieces.

The second section was the fully defensive strategy. I moved pieces according to immediate win conditions. Any time that the opponent had an immediate win condition available, I moved into that spot with a piece that would not cause a new win condition to be opened up for the opponent. While my overall strategy was extremely defensive, I did add in a clause about moving into a winning spot if I could win immediately. In all of my testing that never happened.

Overall I thoroughly enjoyed the project. I had never heard of ROTA before I tried the challenge. There were two parts that I struggled with the most in order of difficulty: 

Debugging: The api does not allow me to step through lines very easily because of the timeout. When I was debugging, I was forced to "concede" each that I wanted to analyse because of the timeout and that made it more difficult to find problems in my code. I don't have a good solution to this problem because allowing people to run the AI locally would open up many avenues of cheating the system.

Implementation: The implementation gave me some trouble because there were a lot properties that I could only think to hardcode in. It wasn't so much difficult as it was tedious. For example, look at my Board.clockwise and Board.counter_clockwise functions or even my Board.opening_moves function. All of those required a (what I think to be) large number of if statements.

Overall, I thought this was a very fun project. I think the effort put into making the challenge accessible makes a big difference for how approachable the problem is.

I have made my github repo for this challenge public. Let me know at one of the above emails if you would prefer I made it private. If there are any questions not answered in this readme or in the comments, feel free to email me.

Anyone should be able to generate more hashes using ROTA.py and looking at stdout for a line that starts with "Hash: "

hashes:

1b74031ca326e30802ed4437e4eb7090b5fedcf26a115077b5a10fa4b9f982567b2275736572223a226d6174746368616d6265726c61696e3240676d61696c2e636f6d222c2274696d657374616d70223a313531383233363338307d

a66ba7c8c32a64df7d47003dc6e8720fb070ed6de3bd1bdb157e1c93e7edfc057b2275736572223a226d6174746368616d6265726c61696e3240676d61696c2e636f6d222c2274696d657374616d70223a313531383233373339377d

375233d62ebf99a6cc5d5ffbefe6823f81fda0d4b6380b69948e68afa87d7c577b2275736572223a226d6174746368616d6265726c61696e3240676d61696c2e636f6d222c2274696d657374616d70223a313531383233373938397d

acace4eb521520aff6e13b9b87ca2f562be55b34ac4a0cab5a5b3bf24ba9a9ba7b2275736572223a226d6174746368616d6265726c61696e3240676d61696c2e636f6d222c2274696d657374616d70223a313531383233383134357d

f849ca881c92437979379ab837f3ba0e7759b54b392c2ef72296eeca5c88c7287b2275736572223a226d6174746368616d6265726c61696e3240676d61696c2e636f6d222c2274696d657374616d70223a313531383233383431367d
