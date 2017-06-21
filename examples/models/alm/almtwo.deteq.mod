


#PARAMETERS: SCALARS
param NT:=4;
param NA:=23;
param NS:=360;
param tbuy  := 1.025;
param tsell := 0.975;
param risklevel:=0.3;

#SETS
set assets := 1..NA;
set tp :=1.. NT;

#SCENARIO
set scen:=1..NS;

#PROBABILITIES
param Prob {scen} :=1/360;


#TREE
#tree theTree:= multibranch {15,8,3};
#tree theTree:= twostage{card(scen)};

#RANDOM PARAMETERS
param price{tp,assets,scen};	

#PARAMETERS : VECTORS (read from database!)
param liabilities{tp};
param initialholdings{assets} := 0;
param income{tp};
param target{tp};


#STAGES
suffix stage LOCAL;

#VARIABLES	
var	amounthold{t in tp,a in assets,s in scen} >=0;
var	amountbuy{t in tp,a in assets,s in scen} >=0;
var	amountsell{t in tp,a in assets,s in scen} >=0;
var	marketvalue{t in tp,s in scen} >=0 ;

#STAGING INFORMATION 
#(ampl doesn't like "suffix stage t" in the var declarations above!)

let {t in tp,a in assets,s in scen} amounthold[t,a,s].stage := if t=1 then 1 else 2;
let {t in tp,a in assets,s in scen} amountbuy[t,a,s].stage :=if t=1 then 1 else 2;
let {t in tp,a in assets,s in scen} amountsell[t,a,s].stage :=if t=1 then 1 else 2;
let {t in tp,s in scen} marketvalue[t,s].stage :=if t=1 then 1 else 2;


#OBJECTIVE
maximize wealth : sum{s in scen} Prob[s]*marketvalue[4,s];

#CONSTRAINTS
subject to

assetmarketvalue1{s in scen}:
	marketvalue[1,s]=sum{a in assets} initialholdings[a]*price[1,a,s];

assetmarketvalue2{t in 2..NT,s in scen}:	
	marketvalue[t,s] = sum{a in assets} amounthold[t,a,s]*price[t,a,s];
	
stockbalance1{a in assets,s in scen}:
	amounthold[1,a,s]=initialholdings[a]+amountbuy[1,a,s]-amountsell[1,a,s];	

stockbalance2{a in assets,t in 2..NT, s in scen}:	
	amounthold[t,a,s]=amounthold[t-1,a,s]+amountbuy[t,a,s]-amountsell[t,a,s];
	
fundbalance1{t in tp,s in scen}:
	sum{a in assets} amountbuy[t,a,s]*price[t,a,s]*tbuy
       -sum{a in assets} amountsell[t,a,s]*price[t,a,s]*tsell=
        income[t]-liabilities[t];

zeta{ t in 2..NT,s in scen}: target[t]-marketvalue[t,s]<=risklevel*target[t];
	
nant1{a in assets, t in 1..1, s in scen} : amounthold[t,a,1] = amounthold[t,a,s];
nant2{a in assets, t in 1..1, s in scen} : amountbuy[t,a,1] = amountbuy[t,a,s];
nant3{a in assets, t in 1..1, s in scen} : amountsell[t,a,1] = amountsell[t,a,s];
nant4{t in 1..1, s in scen} : marketvalue[t,1] = marketvalue[t,s];