# Google Hashcode 2022

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ampl/amplpy/blob/master/notebooks/hashcode/practice_problem.ipynb)

[Google Hashcode](https://codingcompetitions.withgoogle.com/hashcode) is a team programming competition to solve a complex **engineering problem**.

In this notebook we are showing how Mathematical Optimization methods as ***Mixed Integer Programming*** (MIP) are useful to solve this kind of problems, as they are really easy to implement and give optimal solutions (not only _trade-off_ ones), as opposed to greedy approaches or heuristics. We are solving the *pizza* **warm-up exercise**.

We are using [AMPL](https://ampl.com) as the modeling language to formulate the problem from two different approaches (not all the formulations are the same in terms of complexity), coming up with enhancements or alternative approaches is an important part of the solving process.

As an instructive example of how to face this kind of problems, we are using the AMPL API for Python (AMPLPY), so we can read the input of the problem, translate easily to a data file for AMPL, and retrieve the solution to get the score. Because of using MIP approach, the score will be the highest possible for the problem.

## Problem statement

The statement of this year is related to a pizzeria, the goal is to maximize the number of customers coming, and we want to pick the ingredients for the only pizza that is going to be sold:

* Each customer has a list of ingredients he loves, and a list of those he does not like.
* A customer will come to the pizzeria if the pizza has all the ingredients he likes, and does not have any disgusting ingredient for him.

**Task**: choose the exact ingredients the pizza should have so it maximizes the number of customers given their lists of preferences. The score is the number of customers coming to eat the pizza.

(The statement can be found [here](https://bytefreaks.net/google/google-hash-code-2022-practice-problem))

# First formulation

The first MIP formulation will be straightforward. We have to define the variables we are going to use, and then the objective function and constraints will be easy to figure out.

## Variables

We have to decide which ingredients to pick, so
* $x_i$ = 1 if the ingredient *i* is in the pizza, 0 otherwise.
* $y_j$ = 1 if the customer will come to the pizzeria, 0 otherwise.

Where $i = 1, .., I$ and $j = 1, .., c$ (*c* = total of customers and *I* = total of ingredients).

## Objective function

The goal is to maximize the number of customers, so this is clear:
$$maximize \ \sum \limits_{j = 1}^c y_j$$

Finally, we need to tie the variables to have the meaning we need by using constraints.

## Constraints

If the *j* customer comes, his favourite ingredients should be picked (mathematically $y_j=1$ implies all the $x_i = 1$). So, for each $j = 1, .., c$:

$$|Likes_j| \cdot y_j \leq \sum \limits_{i \in Likes_j} x[i]$$
    
Where $Likes_j$ is the set of ingredients $j$ customer likes, and $|Likes_j|$ the number of elements of the set.

If any of the disliked ingredients is in the pizza, customer $j$ can't come (any $x_i = 1$ implies $y_j = 0$). For each customer $j = 1, .., c$:

$$\sum \limits_{i \in Dislikes_j} x_i \leq \frac{1}{2}+(|Dislikes_j|+\frac{1}{2})\cdot(1-y_j)$$

So when customer $j$ comes, the right side is equal to
$$\frac{1}{2}+(|Dislikes_j|+\frac{1}{2})\cdot(1-1) = \frac{1}{2} + 0 = \frac{1}{2}$$
This implies the left side to be zero, because the $x_i$ variables are binary. If the customer $j$ does not come, the inequality is satisfied trivially.

Let's use AMPL to formulate the previous problem. The following section setup AMPL to run in also in the cloud (not only locally) with Google Colab.

## AMPLPY Setup in the cloud

Here is some documentation and examples of the API: [Documentation](http://amplpy.readthedocs.io), [GitHub Repository](https://github.com/ampl/amplpy), [PyPI Repository](https://pypi.python.org/pypi/amplpy), other [Jupyter Notebooks](https://github.com/ampl/amplpy/tree/master/notebooks). The following cell is enough to install it. We are using *ampl* (modeling language) and *gurobi* (solver) modules.


```python
!pip install -q amplpy ampltools
```


```python
import os
RUNNING_IN_GOOGLE_COLAB = 'COLAB_GPU' in os.environ
RUNNING_IN_KAGGLE = os.path.abspath(os.curdir).startswith('/kaggle/')
RUNNING_IN_THE_CLOUD = RUNNING_IN_GOOGLE_COLAB or RUNNING_IN_KAGGLE

# If you have an AMPL Cloud License or an AMPL CE license, you can use it on Google Colab and similar platforms.
# Note: Your license UUID should never be shared. Please make sure you delete the license UUID
# and rerun this cell before sharing the notebook with anyone.
LICENSE_UUID = None
# You can install individual modules from https://portal.ampl.com/dl/modules/
MODULES = ['ampl', 'gurobi']
# Set to True in order to install AMPL only once 
RUN_ONCE = True
if RUNNING_IN_THE_CLOUD:
    from ampltools import ampl_installer
    ampl_dir = os.path.abspath(os.path.join(os.curdir, 'ampl.linux-intel64'))
    ampl_installer(ampl_dir, modules=MODULES, license_uuid=LICENSE_UUID, run_once=RUN_ONCE, verbose=True)
    os.environ['PATH'] += os.pathsep + ampl_dir

# Import, instantiate an ampl object and register jupyter notebook magics
from amplpy import AMPL, register_magics
ampl = AMPL()
# ampl.eval('option version;')
# Store %%ampl cells in the list _ampl_cells
# Evaluate %%ampl_eval cells with ampl.eval()
register_magics(store_name='_ampl_cells', ampl_object=ampl)
```

## Solving problem with AMPL

First, we need to write the model file (`.mod`) containing the mathematical formulation. After that, we will write a data file (`.dat`) to solve the different instances of the Hashcode problem.


```python
%%writefile pizza.mod

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
```

    Overwriting pizza.mod


### Translate input with Python

The input files are in the folder `input_data/`, but they do not have the AMPL data format. Fortunately, we can easily parse the original input files to generate AMPL data files.


```python
import sys

# dict to map chars to hashcode original filenames
filename = {
    'a':'input_data/a_an_example.in.txt',
    'b':'input_data/b_basic.in.txt',
    'c':'input_data/c_coarse.in.txt',
    'd':'input_data/d_difficult.in.txt',
    'e':'input_data/e_elaborate.in.txt'
}

def read(testcase):
    original_stdout = sys.stdout
    with open(filename[testcase]) as input_file, open('ampl_input/pizza_'+testcase+'.dat', 'w+') as output_data_file:
        sys.stdout = output_data_file # Change the standard output to the file we created.
        # total_customers
        total_customers = int(input_file.readline())
        print('param total_customers :=',total_customers,';')
                
        # loop over customers
        ingr=set()
        for c in range(1, total_customers+1):
            likes = input_file.readline().split()
            likes.pop(0)
            print('set Likes['+str(c)+'] := ',end='')
            print(*likes, end = ' ')
            print(';')
            dislikes = input_file.readline().split()
            dislikes.pop(0)
            print('set Dislikes['+str(c)+'] := ',end='')
            print(*dislikes, end = ' ')
            print(';')
            ingr = ingr.union(set(likes))
            ingr = ingr.union(set(dislikes))
        print('set INGR :=')
        print(*sorted(ingr), end = '\n')
        print(';')
    sys.stdout = original_stdout

# Let's try with problem 'c' from hashcode
read('c')
```

The file written can be displayed with ampl:


```python
%%ampl_eval
shell 'cat ampl_input/pizza_c.dat';
```

    param total_customers := 10 ;
    set Likes[1] := akuof byyii dlust ;
    set Dislikes[1] := xdozp ;
    set Likes[2] := dlust luncl qzfyo ;
    set Dislikes[2] := xdozp ;
    set Likes[3] := akuof luncl vxglq ;
    set Dislikes[3] := qzfyo ;
    set Likes[4] := dlust vxglq luncl ;
    set Dislikes[4] :=  ;
    set Likes[5] := dlust xveqd tfeej ;
    set Dislikes[5] :=  ;
    set Likes[6] := qzfyo vxglq luncl ;
    set Dislikes[6] := byyii ;
    set Likes[7] := luncl xdozp xveqd ;
    set Dislikes[7] := sunhp ;
    set Likes[8] := byyii xdozp tfeej ;
    set Dislikes[8] := qzfyo ;
    set Likes[9] := dlust akuof tfeej ;
    set Dislikes[9] := xveqd ;
    set Likes[10] := vxglq dlust byyii ;
    set Dislikes[10] := akuof ;
    set INGR :=
    akuof byyii dlust luncl qzfyo sunhp tfeej vxglq xdozp xveqd
    ;


Now, **solve the problem** usign *AMPL* and *Gurobi* (MIP solver)


```python
%%ampl_eval
model pizza.mod;
data ampl_input/pizza_c.dat;
option solver gurobi;
solve;
display x, y;
```

    Gurobi 9.5.0: optimal solution; objective 5
    5 simplex iterations
    1 branch-and-cut nodes
    :       x   y    :=
    1       .   0
    2       .   0
    3       .   0
    4       .   1
    5       .   1
    6       .   0
    7       .   1
    8       .   1
    9       .   0
    10      .   1
    akuof   0   .
    byyii   1   .
    dlust   1   .
    luncl   1   .
    qzfyo   0   .
    sunhp   0   .
    tfeej   1   .
    vxglq   1   .
    xdozp   1   .
    xveqd   1   .
    ;
    


So the ingredients we should pick are:
* byyii, dlust, luncl, tfeej, vxglq, xdozp and xveqd.
* Customers coming are: 4, 5, 7, 8, 10. Total score: 5.

We can **write an output file** in the hashcode format:


```python
%%ampl_eval
printf "%d ", sum{i in INGR} x[i] > output_file.out;
for{i in INGR}{
    if x[i] = 1 then printf "%s ", i >> output_file.out;
}
shell 'cat output_file.out';
```

    7 byyii dlust luncl tfeej vxglq xdozp xveqd 

## You can try this with the other practice instances!

The big ones can take several hours to get the optimal solution, as MIP problems are usually hard because of the integrity constraints of the variables. That's why it is often necessary to reformulate the problem, or try to improve an existing formulation by adding of combining constraints / variables. In the following section, we present an alternative point of view to attack the Hashcode practice problem, hoping the solver finds a solution earlier this way.

# Alternative formulation

We could exploit the relations between customers and see if we can figure out of them. Actually, the goal is to get the biggest set of independent customers that are compatible (so none of their favourite ingredients are in the pizza). The ingredients we are picking may be deduced from the particular customers preferences we want to have.

With this idea, let's propose a ***graph approach*** where each customer is represented by node, and two nodes are connected by an edge if and only if the two customers are compatible. This is translated to the problem as:

* Customer *i* loved ingredients are not in the disliked ingredients list of *j* (and vice versa).

With sets, this is:

$$Liked_i \cap Disliked_j = Liked_j \cap Disliked_i = \emptyset $$

So the problem is reduced to find the maximal [clique](https://en.wikipedia.org/wiki/Clique_problem) in the graph (a clique is a subset of nodes and edges such as every pair of nodes are connected by an edge), which is an [*NP-Complete*](https://en.wikipedia.org/wiki/NP-completeness) problem. The clique is maximal respect to the number of nodes.

## New variables

To solve the clique problem we may use the binary variables:
* $x_i$ = 1 if the node belongs to the maximal clique, 0 otherwise. For each $i = 1, .., c$.

## Objective function

It is the same as in the previous approach, as a node $i$ is in the maximal clique if and only if the customer $i$ is coming to the pizzeria in the corresponding optimal solution to the original problem. A bigger clique would induce a better solution, or a better solution would imply the solution customers to generate a bigger clique as all of them are compatible.

$$maximize \ \sum \limits_{i = 1}^c x_i$$


## New constraints

The constraints are quite simple now. Two nodes that are not connected can't be in the same clique. For each pair of nodes not connected $i$ and $j$:
$$x_i + x_j \leq 1$$

## Formulation with AMPL

We are writing a new model file (very similar to the previous one). In order to reuse the data files and not get any errors, we will keep the *INGR* set although it is not going to be used anymore.

The most interesting feature in the model could be the condition to check that two customers are incompatible to generate a constraint. The condition is:

$$Liked_i \cap Disliked_j \neq \emptyset \ \text{ or } \ Liked_j \cap Disliked_i \neq \emptyset$$

A set is not empty if its cardinality is greater or equal to one, so in AMPL we could write:

`card(Likes[i] inter Dislikes[j]) >= 1 or card(Likes[j] inter Dislikes[i]) >= 1`


```python
%%writefile pizza_alternative.mod

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

```

    Overwriting pizza_alternative.mod


We can still use the same data files.


```python
%%ampl_eval
reset;
model pizza_alternative.mod;
data ampl_input/pizza_c.dat;
option solver gurobi;
solve;
display x;
```

    Gurobi 9.5.0: optimal solution; objective 5
    3 simplex iterations
    1 branch-and-cut nodes
    x [*] :=
     1  0
     2  0
     3  0
     4  1
     5  1
     6  0
     7  1
     8  1
     9  0
    10  1
    ;
    



```python
%%ampl_eval
set picked_ingr default {};
for{i in 1..total_customers}{
    if x[i] = 1 then let picked_ingr := picked_ingr union Likes[i];
}

printf "%d ", card(picked_ingr) > output_file.out;
for{i in picked_ingr}{
    printf "%s ", i >> output_file.out;
}
shell 'cat output_file.out';
```

    7 dlust vxglq luncl xveqd tfeej xdozp byyii 

# Conclusion

First, let's compare the size of the two models.

* First approach size: $c+I$ variables + $2c$ constraints.
* Second approach size: $c$ variables + $c(c-1)/2$ constraints (potentially).

Also in the second approach, each constraint has only two non-zero coefficients along with variables, which is an advantage to have more sparse coefficient matrices.

The choice of one model or another will depend on the concrete instance of the problem, so the sparsity of the matrix and the real number of constraints can change. AMPL will take care of building the coefficient matrix efficiently, so there is no extra effort to compute the constraints or sums within them once the model is prepared and sent to the solver, and we can focus on thinking algorithmically. Also a lot of constraints and variables would be removed by presolve. To know more about the AMPL modeling language you can take a look to the [manual](https://ampl.com/resources/the-ampl-book/).

Some of the **advantages** of this approach are:
* It is really easy to implement solutions.
* There is no need to debug algorithms, only the correctness of the model.
* Models are very flexible, so new constraints could be added while the rest of the model remains the same.

**Disadvantages**:
* It is hard to estimate how long it is going to take, even in simple models like the ones presented.
* Sometimes it is hard to formulate the problem, as some of the constraints or the objective function could not adjust to the usual mathematical language. The problem could be non-linear so convergence would be more difficult and even optimal solutions would not be guaranteed.
* For simple problems, more efficient algorithmic techniques could also give the best solution (Dynamic Programming, optimal greedy approaches...).

**Enhancements**:
* Study the problem to come up with presolve heuristics in order to get smaller models.
* Add termination criterias (solver options) so the solver can stop prematurely when finding a enough good solution (there is a little gap between the best found solution and the known bounds), or even a time limit. If you are lucky the solution could be the optimal one but the optimality was not proved yet.
* If the solver could not find the optimal solution on time, but we used a termination criteria, we could retrieve a good solution and run some kind of algorithm over it so we can improve and get closer to the optimal (*GRASP* or *Genetic Algorithms*, for instance). Actually, when solving a real engineering problem is desirable to combine *exact methods* as MIP, *heuristics* (greedy approaches) or *metaheuristics* (GRASP, Simulated Annealing, ...) among others, to reach better solutions.


--

*Author: Marcos Dominguez Velad. Software engineer at AMPL.*

<marcos@ampl.com>
