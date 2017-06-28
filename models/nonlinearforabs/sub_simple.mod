# Sets:
set PERIODS               = 1..24 by 1 ;    # Load demand periods
set STAGES within PERIODS = 4..24 by 4 ;    # Step periods for reservoirs 
set HYDRO ordered                      ;    # Hydro Plants
set GENS ordered                       ;    # Thermal Plants





# =============
# Parameters:
# =============
# a) Bring from Matlab:
param LOAD{PERIODS};
param U   {GENS,PERIODS};
param UH  {HYDRO,STAGES};




# b) Thermal System
param A1  {GENS} ; # Linear coefficient of cost function
param A2  {GENS} ; # Quadratic coefficient of cost function
param PMAX{GENS} ;
param PMIN{GENS} ;
param VOLL:= 1500;


# c) Hydro system
# Filtration function coefficients for reservoir 1 (cuadratic)
param K0;  
param K1;
param K2;
# Filtration function coefficients (linear)
param B0;  
param B1;
# Future cost function coefficients (Reservoir 1):
param p3:= -1.352e-5;
param p2:= 0.1765;
param p1:= -811.1;
param p0:= 1.775e6;
# Hydropower Productivity Function coefficients
param C0 {HYDRO};
param C1 {HYDRO};
param C2 {HYDRO};
param C3 {HYDRO};
param C4 {HYDRO};
param C5 {HYDRO};
param C00{HYDRO};

param TOPOLOGY{HYDRO,HYDRO} ;
param FC:=1.44e-2           ;     # Con DeltaT= 4 horas;
param INFLOW{HYDRO}         ;
param VMIN{HYDRO}           ;
param VMAX{HYDRO}           ;
param V0  {HYDRO}           ;
param QMIN{HYDRO}           ;
param QMAX{HYDRO}           ;


# ======================
#      Variables:
# ======================
var   P  {GENS,PERIODS}    ;
var   u  {GENS,PERIODS};
var   ENS{PERIODS}>=0      ;
var   H  {HYDRO,PERIODS}>=0;
var   V  {HYDRO,STAGES}    ;
var   Q  {HYDRO,STAGES} >=0;
var   S  {HYDRO,STAGES} >=0;
var   uh {HYDRO,STAGES};

var   ce = sum{t in PERIODS}(sum{i in GENS} (A1[i]*P[i,t]+P[i,t]*A2[i]*P[i,t]) + VOLL*ENS[t]);
var   cf = p1*V['U1',24]+p2*V['U1',24]*V['U1',24]+p3*V['U1',24]*V['U1',24]*V['U1',24];


# ==========================================
#          Optimization Problem
# ==========================================
minimize of : ce + cf; 



#Constraints:
subject to R1{t in PERIODS}: 
sum{i in GENS} P[i,t]+ sum{j in HYDRO}H[j,t]+ENS[t]= LOAD[t];

subject to R2{i in GENS, t in PERIODS}: P[i,t] <= PMAX[i]*u[i,t];
subject to R3{i in GENS, t in PERIODS}: P[i,t] >= PMIN[i]*u[i,t];
subject to R4{t in PERIODS}: ENS[t] <= LOAD[t];

# Water Balance :
subject to R10{j in HYDRO, h in STAGES}:
V[j,h] = (if h=4 then V0[j] else V[j,h-4]) + 
FC*(INFLOW[j] - sum{jj in HYDRO} TOPOLOGY[j,jj]*(Q[jj,h]+S[jj,h])) -
FC*(if j='U1' then (K0+K1*V[j,h]+V[j,h]*K2*V[j,h]));


# Productivity function:
#subject to R11{j in HYDRO, h in STAGES, t in PERIODS: (t>=h-3 and t<=h)}:
#H[j,t]= C0[j]*Q[j,h]+C1[j]*Q[j,h]*V[j,h]+C2[j]*V[j,h]*Q[j,h]*V[j,h] +
#        Q[j,h]*C3[j]*Q[j,h] + C4[j]*Q[j,h]*Q[j,h]*Q[j,h] + C5[j]*Q[j,h]*Q[j,h]*Q[j,h]*Q[j,h]+
#        (if j='U5' then C00[j]*uh[j,h]);
 
# Productivity function:
subject to R11{j in HYDRO, h in STAGES, t in PERIODS: (t>=h-3 and t<=h)}:
H[j,t]= C0[j]*Q[j,h];
 
 
        
subject to R12{j in HYDRO, h in STAGES}: V[j,h] <= VMAX[j];
subject to R13{j in HYDRO, h in STAGES}: V[j,h] >= VMIN[j];
subject to R14{j in HYDRO, h in STAGES}: Q[j,h] >= QMIN[j]*uh[j,h];
subject to R15{j in HYDRO, h in STAGES}: Q[j,h] <= QMAX[j]*uh[j,h];

 
# Hydroelectric plants without reservoir; 
subject to R16{j in HYDRO, h in STAGES: j='U2' and j='U3' and j='U5' and j='U6' and j='U8'}:
V[j,h]=0;


subject to R20{i in GENS, t in PERIODS}: u[i,t]  = U[i,t];
subject to R21{j in HYDRO, h in STAGES}: uh[j,h] = UH[j,h];

