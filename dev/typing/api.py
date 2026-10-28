"""Static regression cases. Run: python -m mypy --config-file dev/typing/mypy.ini."""
from typing import Any, Iterator, List, Optional, Tuple, Union

from typing_extensions import assert_type

from amplpy import (
    AMPL, AMPLException, AMPLIndex, AMPLVariant, Column, Constraint, DataFrame,
    Entity, EntityMap, Environment, ErrorHandler, Kind, Objective, OutputHandler,
    Parameter, Row, Set, Variable, add_to_path,
)


def check_api(ampl: AMPL, capture_output: bool) -> None:
    constraint = ampl.con["c"]
    assert_type(constraint[2], Constraint)
    assert_type(constraint["a", 2], Constraint)
    assert_type(constraint.get(), Constraint)
    assert_type(constraint.get(2), Constraint)
    assert_type(constraint.get("a", 2), Constraint)
    assert_type(constraint.find(("a", 2)), Optional[Constraint])
    constraint[2].drop()
    constraint.get(2).restore()
    constraint[2].fix()  # type: ignore[attr-defined]
    for index, instance in constraint:
        assert_type(index, Optional[AMPLIndex])
        assert_type(instance, Constraint)
        instance.drop()
    for index, instance in constraint.instances():
        assert_type(instance, Constraint)
        instance.restore()
    assert_type(len(constraint.instances()), int)
    for name, con in ampl.con:
        assert_type(name, str)
        assert_type(con, Constraint)
    assert_type(ampl.get_constraints(), EntityMap[Constraint])
    assert_type(next(ampl.getConstraints()), Tuple[str, Constraint])
    assert_type(ampl.get_variables()["x"], Variable)
    assert_type(ampl.var["x"]["a", 1], Variable)
    ampl.var["x"]["a", 1].fix(2)
    for name, variable in ampl.var:
        assert_type(variable, Variable)
    assert_type(ampl.obj["o"][1], Objective)
    for name, objective in ampl.obj:
        assert_type(objective, Objective)
    param = ampl.param["p"]
    assert_type(param.get(), Parameter)
    assert_type(param.get(2), AMPLVariant)
    assert_type(param["a", 2], AMPLVariant)
    assert_type(param.find(2), Optional[Parameter])
    assert_type(param.get_values(), DataFrame)
    assert_type(param.name(), str)
    for index, parameter in param:
        assert_type(parameter, Parameter)
    for name, parameter in ampl.param:
        assert_type(parameter, Parameter)
    assert_type(ampl.set["S"][1], Set)
    assert_type(ampl.set["S"].get_values(), DataFrame)
    for index, set_instance in ampl.set["S"].instances():
        assert_type(set_instance, Set)
        set_instance.set_values([1, 2])
    for name, set_entity in ampl.set:
        assert_type(set_entity, Set)
    ampl.set["S"] = {1: [1, 2], 2: [3]}
    assert_type(ampl.get_data("x", "x.lb"), DataFrame)
    assert_type(ampl.getData("x", "x.ub"), DataFrame)
    assert_type(ampl.get_data("x").to_list(), List[Union[AMPLVariant, Tuple[AMPLVariant, ...]]])
    assert_type(ampl.get_data("x")._get_column("x"), Column)
    assert_type(next(iter(ampl.get_data("x"))), Row)
    assert_type(ampl.get_data("x")._get_row(1)[0], AMPLVariant)
    assert_type(DataFrame.from_dict({1: 2.0}), DataFrame)
    assert_type(DataFrame.fromDict({1: 2.0}), DataFrame)
    assert_type(ampl.solve(), None)
    assert_type(ampl.solve(return_output=True), str)
    assert_type(ampl.solve("", "", False, True), str)
    assert_type(ampl.solve(return_output=capture_output), Optional[str])
    assert_type(ampl.solve_result, str)
    assert_type(ampl.solve_result_num, int)
    ampl.option = {"solver": "highs"}
    ampl.option["highs_options"] = {"presolve": True}
    assert_type(ampl.option["missing"], AMPLVariant)
    assert_type(ampl.get_option("missing"), AMPLVariant)
    assert_type(ampl.get_entity("x"), Entity[Any])
    env = Environment("/path/to/ampl", "ampl")
    assert_type(iter(env), Iterator[Tuple[str, str]])
    assert_type(env.getBinDir(), str)
    add_to_path("/path/to/ampl")
    assert_type(Kind.DISPLAY, int)


class CaptureOutput(OutputHandler):
    def output(self, kind: int, msg: str) -> None:
        pass


class CaptureErrors(ErrorHandler):
    def error(self, exception: AMPLException) -> None:
        assert_type(exception.get_message(), str)
