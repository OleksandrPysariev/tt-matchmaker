# tt-matchmaker
The task had the following description:
```
Imagine a game like League of Legend or Overwatch. They use a matchmaking service to
match users with the same skill. So each user calls the matchmaker and after a reasonable
amount of time, he receives the address of a match-server to connect to, and play a match with
some other players with about the same skill.
```
I can see at least 4 distinct responsibilities here: 
1) waiting queue manager service
2) match groups composer service
3) game server resolver (based on current load per server)
4) player DB service (to track states, ids, skill levels etc.)
As a seasoned developer that I am, I know better than to couple all those things into one app. However, the time required
to develop 4 distinct apps is way above what I am able to commit to this task. Instead, I am consciously going to focus on
part number 2) the match groups composer, but with a caveat other services already exist and working.

# Service Design
Q. Please describe how you envision the subsystems of the matchmaking application.

A. According to the description, the system may have such subsystems: 
- a some sort of player queue manager for waiting players: it should keep track of incoming players 
(ID, skill level, timestamp when the player has joined a queue). This will effectively manage converting a request from
single player to an array of requests we can arrange into game matches.  
- an app with matching logic that groups players into balanced teams (what I am going to be implementing HERE.)
- a Match Allocator that assigns them to game servers. (Should know server state, load, region, etc.)
- a Session Manager that tracks player state. (Some system in place probably with cache to return and update player info.)
2. Inter-Service Communication
Subsystems communicate internally via in-memory queues or a message broker. Externally, the system calls game server
API to organize matches and send results back to clients via HTTP responses or webhooks.
3. Game Interface
Three FastAPI endpoints expose the matchmaking logic: POST /matches/simple, POST /matches/squad, and POST /matches/improved,
each accepting a player list and returning matched teams with a server address, or empty if no quality match exists.


3. Bonus : Further matchmaking improvements.
What could you add to this system to prevent players from waiting too long for a match?

Modify the previous code.

IDEA: some sort of priority queue for players with long wait times.
