set s;
param f{s};

table t IN "ODBC", "banana.ocd" : [s], f;
read table t;