from __future__ import print_function
import amplpy

a = amplpy.AMPL()

# Environment
e = amplpy.Environment()
# for s in e:
#     print(s[0], ' = ', s[1])

# Entities and instances
a.reset()
a.eval("set S := 2..20 cross 1..10;")
S = a.getSet("S")
print(list(S.get()))

a.eval("var x;")
a.eval("var y {1..2};")
a.eval("var z {1..2,3..4};")
a.eval("var zz {{(1, 2)}};")
x = a.getVariable("x")
y = a.getVariable("y")
z = a.getVariable("z")
zz1 = a.getVariable("zz")
zz2 = a.getVariable("zz").get((1, 2))
zz3 = a.getVariable("zz")[(1, 2)]
zz4 = a.getVariable("zz")[1, 2]
print(list(a.getVariables()))
print(list(a.getSets()))
print(x, y, z, zz1, zz2, zz3, zz4)
lst = list(a.getVariable("zz"))
print(lst)
print(lst[0][1].value())

a.reset()

a.eval("set X{i in 1..10} := 1..i;")
print(list(a.getSet("X").get(10)))
a.eval("var x{i in 1..5} := i;")
a.eval("s.t. con{i in 1..4}: x[i] = x[i+1];")
a.eval("var y := 6;")
x = a.getVariable("x")
y = a.getVariable("y")
print(list(a.getConstraints()))
print(a.getConstraint("con")[2])
# assert False
print(y.value())
for i in x:
    print(i[1].value())


class MyOutput(amplpy.OutputHandler):
    def output(self, kind, text):
        print("From python: ")
        print(text)


print(a.cd())
a.setOutputHandler(MyOutput())
a.eval("display x;")
a.setOption("solver", "gurobi")
print(">>", a.getOption("solver"))
print(">>", a.getOption("gentimes"), type(a.getOption("gentimes")))

# DataFrame
d = amplpy.DataFrame(index=('one',), columns=('two',))
d.addColumn("x")
d.setValues({
    1: (-1, 5),
    (2,): (-1, '5'),
})
d.addRow([1, -4, 5])
d.addRow([4, -6, '5'])
dd = d.toDict()
print(dd)
one, two, x = amplpy.multidict(dd)
print("one:", one)
print("two:", two)
print("x:", x)
print(d)
a.eval("display two;")
print('>>>', d.getColumn("one"), list(d.getColumn("one")))
print('>>>', d.getRow(2), list(d.getRow(2)))
print('>>>', d.getRowByIndex(0), list(d.getRowByIndex(0)))
print("Headers:", d.getHeaders())
print("---")
d.addColumn("four", ["Seven", "Eight", "x", "y"])
d.addColumn("five", [9.5, 10.6, 1, 2])
print(d)
print(d.getNumCols(), d.getNumRows(), d.getNumIndices())

v = a.getValue("y")
print(v.dbl())
d1 = a.getData("x")
print(d1)


ampl = amplpy.AMPL()
ampl.eval("set S;")
ampl.eval("set T;")
ampl.eval("data;")
ampl.eval("set S := A B C D;")
ampl.eval("set T := 1 2 3;")
print(ampl.getData("{S,T}"))

ampl = amplpy.AMPL()
ampl.eval("set S;")
ampl.eval("set T{s in S};")
ampl.eval("set U{s in S, t in T[s]};")
ampl.eval("data;")
ampl.eval("set S := 'keyS';")
ampl.eval("set T['keyS'] := 'keyT';")
ampl.eval("set U['keyS','keyT'] := 'keyU1','keyU2';")
print(ampl.getData("U['keyS','keyT']"))
df = ampl.getData("{3..4,1..2}")
print(df)
print(df.getHeaders())
print(df.getColumn("index0"))
print(df.getColumn("index1"))
a.eval("param b{i in 1..10} := i;")
print(a.getParameter("b")[5])
print(list(a.getParameters()))
