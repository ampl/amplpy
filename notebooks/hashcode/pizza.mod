
# PARAMETERS AND SETS
param total_customers;

# Set of ingredients
set INGR;
# Customers lists of preferences
set Likes{1..total_customers};
set Dislikes{1..total_customers};

# VARIABLES

# Take or not to take the ingredient
var x{i in INGR}, binary;
# customer comes OR NOT
var y{j in 1..total_customers}, binary;

# OBJECTIVE FUNCTION
maximize Total_Customers: sum{j in 1..total_customers} y[j];

s.t.
Customer_Likes{j in 1..total_customers}:
	card(Likes[j])*y[j] <= sum{i in Likes[j]} x[i];

param eps := 0.5;

Customer_Dislikes{j in 1..total_customers}:
	sum{i in Dislikes[j]} x[i] <= 1-eps+(card(Dislikes[j])+eps)*(1-y[j]);
