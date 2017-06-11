from model import Objective, Variable, Constraint
from data import Set, Parameter
from dataframe import DataFrame
from iterators import MapEntities
import amplpython


class AMPL:
    def __init__(self):
        self._impl = amplpython.AMPL()
        self._outputhandler = None
        self._errorhandler = None

    def eval(self, amplstatements):
        self._impl.eval(amplstatements)

    def read(self, fileName):
        self._impl.read(fileName)

    def readData(self, fileName):
        self._impl.readData(fileName)

    def getOption(self, name):
        try:
            value = self._impl.getOption(name).value()
        except RuntimeError:
            return None
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def setOption(self, name, value):
        if isinstance(value, int):
            return self._impl.setIntOption(name, value)
        elif isinstance(value, float):
            return self._impl.setIntOption(name, value)
        elif isinstance(value, bool):
            return self._impl.setBoolOption(name, value)
        elif isinstance(value, basestring):
            return self._impl.setOption(name, value)
        else:
            raise TypeError

    def cd(self, path=None):
        if path is None:
            return self._impl.cd()
        else:
            return self._impl.cd(path)

    def reset(self):
        self.eval("reset;")
        # self._impl.reset()  # FIXME: causes Segmentation fault

    def solve(self):
        self._impl.solve()

    def close(self):
        self._impl.close()

    def __del__(self):
        self.close()

    def getValue(self, statement):
        return self._impl.getValue(statement)

    def getSet(self, name):
        return Set.fromSetRef(self._impl.getSet(name))

    def getSets(self):
        return MapEntities(Set.fromSetRef, self._impl.getSets())

    def getParameter(self, name):
        return Parameter.fromParameterRef(self._impl.getParameter(name))

    def getParameters(self):
        return MapEntities(
            Parameter.fromParameterRef, self._impl.getParameters()
        )

    def getObjective(self, name):
        return Objective(self._impl.getObjective(name))

    def getObjectives(self):
        return MapEntities(Objective, self._impl.getObjectives())

    def getVariable(self, name):
        return Variable(self._impl.getVariable(name))

    def getVariables(self):
        return MapEntities(Variable, self._impl.getVariables())

    def getConstraint(self, name):
        return Constraint(self._impl.getConstraint(name))

    def getConstraints(self):
        return MapEntities(Constraint, self._impl.getConstraints())

    def getData(self, *statements):
        return DataFrame.fromDataFrameRef(
            self._impl.getData(list(statements), len(statements))
        )

    def setData(self, dataframe):
        self._impl.setData(dataframe._impl)

    def getValue(self, statement):
        return self._impl.getValue(statement)

    def setOutputHandler(self, outputhandler):
        self._outputhandler = outputhandler
        self._impl.setOutputHandler(outputhandler)

    def getOutputHandler(self):
        self._outputhandler = self._impl.getOutputHandler()
        return self._outputhandler

    def setErrorHandler(self, errorhandler):
        self._errorhandler = errorhandler
        self._impl.setErrorHandler(errorhandler)

    def getErrorHandler(self):
        self._errorhandler = self._impl.getErrorHandler()
        return self._errorhandler


class Environment:
    def __init__(self):
        self._impl = amplpython.Environment()

    def __iter__(self):
        return EnvIterator(self._impl)
