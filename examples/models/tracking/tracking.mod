# This model implements a simple index tracking model,
# in which we choose out holdings to minimize deviations from an index
# over a time horizon.
# It also includes some facilities to implement the simple heuristic
# described in the source file.
param data_dir symbolic;		# Directory of data files

set asset;						# Set of assets
set time:=1..290;				# Set of timeperiods considered
set rtime;						# Set of timeperiods for which we have data

param indret{rtime};			# Index return 
param astret{rtime,asset};		# Assets returns
param ifinuniverse{asset} default 1;	# Indicator for heuristic
# set to 1 to be able to choose that asset for the portfolio, 
# to 0 to force it out, to 2 to force it in

var overindex{time} >=0;	# Amount of overdeviation
var underindex{time} >=0;	# Amount of underdeviation
var hold{i in asset : ifinuniverse[i]>=1} >=0;		# Positions
var ifhold{i in asset : ifinuniverse[i]>=1} binary;	# Indicates whether we have 
# invested in an asset at all

# Minimize total deviation over time
minimize cst: sum{t in time} (overindex[t]+underindex[t]);

subject to

# Balance constraint Considers only the assets which are in the universe
target{t in time}:  sum{i in asset : ifinuniverse[i]>=1} hold[i]*astret[t,i]=
indret[t]+overindex[t]-underindex[t];
# Total holdings = 100%
stckbal: sum{i in asset : ifinuniverse[i]>=1} hold[i]=1;
# Forces ifhold to 0 if we do not hold any of the asset
lowlink{a in asset : ifinuniverse[a]>=1}: hold[a]>=0.005*ifhold[a];
# Forces ifhold to 1 if we hold any amount of the asset
uplink{a in asset : ifinuniverse[a]>=1}: hold[a]<=ifhold[a];
# Cardinality constraint
cardlim: sum{a in asset : ifinuniverse[a]>=1}ifhold[a]<=15;
# For "ifinuniverse=2", force the asset in
fixing{a in asset :ifinuniverse[a]=2}:ifhold[a]=1;
