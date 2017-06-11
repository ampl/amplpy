from entity import Entity


class Objective(Entity):
    def __init__(self, _impl):
        Entity.__init__(self, _impl, Objective)

    def value(self, value):
        return self._impl.value(value)

    def astatus(self):
        return self._impl.astatus()

    def sstatus(self, value):
        return self._impl.sstatus(value)

    def exitcode(self):
        return self._impl.exitcode()

    def message(self):
        return self._impl.message()

    def result(self):
        return self._impl.result()

    def drop(self):
        self._impl.drop()

    def restore(self):
        self._impl.restore()

    def minimization(self):
        return self._impl.minimization()


class Variable(Entity):
    def __init__(self, _impl):
        Entity.__init__(self, _impl, Variable)

    def fix(self, value):
        self._impl.fix(value)

    def unfix(self):
        self._impl.unfix()

    def setValue(self, value):
        self._impl.setValue(value)

    def value(self):
        return self._impl.value()

    def astatus(self):
        return self._impl.astatus()

    def defeqn(self):
        return self._impl.defeqn()

    def dual(self):
        return self._impl.dual()

    def sstatus(self):
        return self._impl.sstatus()

    def status(self):
        return self._impl.status()


class Constraint(Entity):
    def __init__(self, _impl):
        Entity.__init__(self, _impl, Constraint)

    def isLogical(self):
        self._impl.isLogical()

    def drop(self):
        self._impl.drop()

    def restore(self):
        self._impl.restore()

    def body(self):
        return self._impl.body()

    def astatus(self):
        return self._impl.astatus()

    def defvar(self):
        return self._impl.defvar()

    def dinit(self):
        return self._impl.dinit()

    def dinit0(self):
        return self._impl.dinit0()

    def dual(self):
        return self._impl.sstatus()

    def lb(self):
        return self._impl.lb()

    def ub(self):
        return self._impl.ub()

    def lbs(self):
        return self._impl.lbs()

    def ubs(self):
        return self._impl.ubs()

    def ldual(self):
        return self._impl.ldual()

    def udual(self):
        return self._impl.udual()

    def lslack(self):
        return self._impl.lslack()

    def uslack(self):
        return self._impl.uslack()

    def slack(self):
        return self._impl.slack()

    def sstatus(self):
        return self._impl.sstatus()

    def status(self):
        return self._impl.status()

    def setDual(self, dual):
        self._impl.setDual(dual)

    def val(self):
        return self._impl.val()
