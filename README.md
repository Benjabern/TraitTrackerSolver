## INSTALLATION
To install the command line tool run:

> git clone https://github.com/Benjabern/TraitTrackerSolver.git

> cd TraitTrackerSolver

> pip3 install -r requirements.txt

> pip3 install -e .

## USAGE
The tool offers three modules: track, compute and analyse.
The track tool searches for valid compositions stored in binary files computed with the compute module.
The input is a number of champions and the output is a list of comps sorted by percentage of owned champs and remaining cost.

With default settings for normal play just using 
> tts track champ1 champ2

should be sufficient if you are simply looking for recomendations to fulfill the TraitTracker requirements at Level 7 using maximum tier 3 champions.
Additional capabilities of the modules are outlined below
# Track example usage
Owning bard and zoe and limiting the board size to 6 (default is 7) while considering champions of maximum cost 5 (default is 3):
> tts track zoe bard -cs 6 -mc 5

The -i flag can be followed by a custom computed binary file located in the data folder (the default for max board size 8 and a minimum of 7 active traits is bundled with the repo)
# Compute example usage
Compute all compositions with at least 6 active traits, a max board size of 7 and a shapeshifter emblem:
> tts compute -t 6 -c 7 -e shapeshifter

The binary file is stored in data and can afterwards be used as input for the track and analyse module
# Analyse example usage
This module is very rudimentary but should provide a starting point for users wanting to analyse generated compositions with specific constraints.
Generate and plot distribution of activated traits and number of active traits in compositions generated above:
> tts analyse -i 9_champs_8+_traits_shapeshifter_emb.bin

## Time and hardware considerations
The generation and checking of champ combinations is done sequentially as to not require storing large arrays in memory. 
This allows for relatively inexpensive generation of compositions of length 9 in terms of memory and time.
Larger boards and looser constraints on active traits quickly lead to very high generating and searching times as well as memory demands.
On the fly tracking of compositions is also not really feasable for board sizes of more than 8 as search times get longer.
For users with slow hardware generating the 7 champion 7+ trait composition file might be advisable as most players will be working with a boardspace of 7 at the relevant time anyway.
