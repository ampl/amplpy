
# ----------------------------------------
# LOCATION-TRANSPORTATION PROBLEM 
# USING BENDERS DECOMPOSITION
# (using primal formulation of subproblem)
# ----------------------------------------

### SUBPROBLEM ###

set ORIG;   # shipment origins (warehouses)
set DEST;   # shipment destinations (stores)

param supply {ORIG} > 0;
param demand {DEST} > 0;

param fix_cost {ORIG} > 0;
param var_cost {ORIG,DEST} > 0;


var Build {ORIG} binary;   # = 1 iff warehouse built at i, 
                           # fixed in subproblem
var Ship {ORIG,DEST} >= 0;  # amounts shipped

minimize Ship_Cost:
   sum {i in ORIG, j in DEST} var_cost[i,j] * Ship[i,j];

subj to Supply {i in ORIG}:
   sum {j in DEST} Ship[i,j] <= supply[i] * Build[i];

subj to Demand {j in DEST}:
   sum {i in ORIG} Ship[i,j] = demand[j];

### MASTER PROBLEM ###

param nCUT >= 0 integer;
param cut_type {1..nCUT} symbolic within {"point","ray"};
param supply_price {ORIG,1..nCUT} <= 0.000001;
param demand_price {DEST,1..nCUT};


var Max_Ship_Cost >= 0;

minimize Total_Cost:
   sum {i in ORIG} fix_cost[i] * Build[i] + Max_Ship_Cost;

subj to Cut_Defn {k in 1..nCUT}:
   if cut_type[k] = "point" then Max_Ship_Cost >= 
      sum {i in ORIG} supply_price[i,k] * supply[i] * Build[i] + 
      sum {j in DEST} demand_price[j,k] * demand[j];

problem Master: Build, Max_Ship_Cost, Total_Cost, Cut_Defn;
problem Sub: Ship, Ship_Cost, Supply, Demand;
