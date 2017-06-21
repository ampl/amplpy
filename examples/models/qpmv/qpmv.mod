# This is a mean-variance model, with additional sets and
# parameters to support the heuristics implemented in the script.

set stockall ordered;                  # All stocks in the universe of assets
set stockrun ordered default stockall; # Stocks used for this run
set stockopall ordered default {};     # Stocks which had more than 0.5 weight

param ncard default 10;                # Maximum cardinality of portfolio
param averret{stockall};               # Average return of each stock
param covar{stockall, stockall};       # Covariance matrix
param cutoffl default 0.0001;          # Lower cutoff (weight < cutoffl -> stock out)
param cutoffh{stockall} default 1;     # High cutoff (weight > cutoffh -> stock in)
param targetret default 0;             # Target return for the efficient frontier

var weights{s in stockrun} >= 0;       # Weight of each stock in the current run
var ifstock{s in stockrun} binary;     # Indicates if a stock had weight > cutoffl
var portret >= targetret;              # Portfolio return

# Minimize risk (X * C * X)
minimize cst: sum{s in stockrun, s1 in stockrun} weights[s] * covar[s, s1] * weights[s1];

subject to

# Total weights = 1
invest: sum{s in stockrun} weights[s] = 1;

# Portfolio return definition
defret: sum{s in stockrun} averret[s] * weights[s] = portret;

# Force ifstock to be 0 if weight < cutoffl
lowlnk{s in stockrun}: weights[s] >= cutoffl * ifstock[s];

# Force ifstock to be one if weight > cutoffh
uplink{s in stockrun}: weights[s] <= cutoffh[s] * ifstock[s];

# Fix each stock in stockopall to be included
fixing{s in stockopall}: ifstock[s] = 1;

# Cardinality constraint
carda: sum{s in stockrun} ifstock[s] <= ncard;
