
# PARAMETERS AND SETS
param total_customers;

# Set of ingredients
set INGR;
# Customers lists of preferences
set Likes{1..total_customers};
set Dislikes{1..total_customers};

# VARIABLES

# customer comes OR NOT <=> node in the clique or not
var x{i in 1..total_customers}, binary;

# OBJECTIVE FUNCTION
maximize Total_Customers: sum{i in 1..total_customers} x[i];

s.t.
# Using the set operations to check if two nodes are not connected
Compatible{i in 1..total_customers-1, j in i+1..total_customers : card(Likes[i] inter Dislikes[j]) >= 1 or card(Likes[j] inter Dislikes[i]) >= 1}:
	x[i]+x[j] <= 1;
