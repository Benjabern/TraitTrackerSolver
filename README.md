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

The -i flag can be followed by a custom computed binary file located in the data folder (the default for max board size 7 and a minimum of 7 active traits is bundled with the repo)
# Compute example usage
Compute all compositions with at least 8 active traits, a max board size of 9 and a shapeshifter emblem:
> tts compute -t 8 -c 9 -e shapeshifter

The binary file is stored in data and can afterwards be used as input for the track and analyse module
# Analyse example usage
This module is very rudimentary but should provide a starting point for users wanting to analyse generated compositions with specific constraints
Generate and plot distribution of activated traits and number of active traits in compositions generated above:
> tts analyse -i 9_champs_8+_traits_shapeshifter_emb.bin

## Time and hardware considerations
The generation and checking of champ combinations is done sequentially to not have to store large arrays in memory. 
This allows for relatively inexpensive generation of compositions of length 9 in terms of memory and time.
Larger boards and loser constraints on active traits quickly lead to very high time and memory demands.
For most ingame usecases, the bundled 7 champion, 7+ trait combinations are sufficient.
