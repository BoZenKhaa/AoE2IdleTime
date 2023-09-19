## Useful references
- [mgx format docs](https://github.com/stefan-kolb/aoc-mgx-format)

## Discord conversation
```
Hi! I had a question about game analysis. How do you process the output of mgz?  I was thinking of looking into writing a dark age idle TC time calculator which sounds like it should be possible, but I am not sure where it could fit in.
Is it something that would be interesting to you?

PoorRed / AoE2Insights — 09/07/2023 11:26 AM
It's unfortunately not possible without an enormous amount of work.

Blazena_Bozena — 09/07/2023 11:31 AM
Thanks for the insight, do you care to elaborate? Looking at the mgx format docs, it seems to me that some form of estimate (e.g. ignoring pop limit or civ bonuses)  should be doable

Void / AoE2Insights — 09/07/2023 11:36 AM
Well by ignoring of all side effects it might be possible to estimate something, but that's not near the real idle tc time on average.
We've even experimented with adding pop-space checks, queue-/unqueue-actions in tc (but even there you can't tell what has been unqueued, was it a vil or maybe loom? or feudal update?), for now we've given up on that topic. but maybe you are luckier 🙂

Blazena_Bozena — 09/07/2023 11:43 AM
Thank you for the answer, you obviously put quite a bit of thought into this. These are side effects I haven't considered, and clearly, these would put the timer way off.  Going above the dark age would just generate garbage very often. However, naively, I feel like in the dark, this could produce helpful info, at least for low ELO people like me.  From your feel and understanding of the data, am I off here?
Also, if I did try to look into it, is there a package you think this would fit into? And would you consider including such an estimate in your analysis output if it turned out to be accurate some of the time? 

Void / AoE2Insights — 09/07/2023 12:04 PM
if you find a possible way, which - more often then not - generates good estimations of the tc idle time in dark age we would surely consider to add this to the analysis.

Blazena_Bozena — 09/07/2023 12:48 PM
Cheers, I will reach out if I come up with anything.

Guimoute — 09/07/2023 10:01 PM
If you are ok with an extremely basic approximation, you can go with how many times the "create villager" action was required before feudal age
that will be accurate only for people whose only reason for idle TC is... not queueing villagers

Blazena_Bozena — 09/07/2023 10:06 PM
Good tips! I actually found a snippet that adds up de_queue actions that add villagers or tc techs, substracts dequeue actions, multiples that by build times and compares that to the castle age event. To me, that sound like it could be sufficiently accurate, but I will have to prepare some replays to test this with and measure the idle time with CA. 
Actually I dont see any other simple way of doing this from exploring the replay data today.
Btw, do you know if there are any docs? The mgx docs dont seem to be up to date with the DE version of the replays.

Guimoute — 09/07/2023 10:11 PM
Nope, I don't know of any. I just grab stuff from the Summary object. The best documentation I've found is to call dir on all the objects to see what they can do 11

Blazena_Bozena — 09/07/2023 10:12 PM
Only thing, I haven’t checked how to get the age-up event time, but that surely must be somewhere as it is displayed in the analysis already. Do I have to add up the sync events?

Guimoute — 09/07/2023 10:13 PM
Add 130s to the "feudal age research" action time 

Blazena_Bozena — 09/07/2023 10:13 PM
Oh but the actions dont include time, do they?
Also, that would be the time it was queued and not started researching
There is one action value that I dont know what it does, but I dont think its time after some tests.

Guimoute — 09/07/2023 10:14 PM
Ah yes, good point. You need to make yourself a list that represents the queue then
sorry I suck at SYNC actions, I've never understood how to convert them into game time
but simulating the game in steps of 1s could solve your issue of separating research queued at x time and research started for real at x time

Blazena_Bozena — 09/07/2023 10:19 PM
Well i just need the time for the age-up event, and that must be somewhere for sure (its displayed in the analysis already). So fir crude estimate, I only need to add up the buld time of queued vils and techs. For more accurate picture, I would subtract dequeed stuff, but for dequeuing I need to watch the time in the sync events.
Thats the plan at least

Void / AoE2Insights — 09/08/2023 10:21 AM
The first value in the payload of the SYNC Operation is the time-increment, you just have to add them to get the current game time.
And for the uptimes you have to look for CHAT operations and find the corresponding message, combined with the current time summed up from the SYNC operations you get the exact uptimes of the players.
```