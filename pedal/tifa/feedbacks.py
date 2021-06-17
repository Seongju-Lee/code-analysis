"""
All of the feedback responses generated by TIFA.
"""
from pedal.utilities.operators import OPERATION_DESCRIPTION
from pedal.core.report import MAIN_REPORT
from pedal.core.feedback import FeedbackResponse


class TifaFeedback(FeedbackResponse):
    """ Base class for all TIFA feedback """
    muted = False
    category = FeedbackResponse.CATEGORIES.ALGORITHMIC
    kind = FeedbackResponse.KINDS.MISTAKE


class action_after_return(TifaFeedback):
    """ Statement after return """
    title = "Action after Return"
    message_template = ("{location.line}번 줄에서 이미 함수에서 돌아온 후 작업을 수행했습니다."
                        "\n\n함수에서 한 번만 돌아올 수 있습니다.")
    justification = ("TIFA visited a node not in the top scope when its "
                     "*return variable was definitely set in this scope.")

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class return_outside_function(TifaFeedback):
    """ Return statement outside of function """
    title = "Return outside Function"
    message_template = ("{location.line}번줄에서 함수 외부로 반환하려고 했습니다."
                        "\n\n반환은 함수 내에서만 할 수 있습니다.")
    justification = "TIFA visited a return node at the top level."

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class multiple_return_types(TifaFeedback):
    """ Multiple returned types in single function """
    title = "Multiple Return Types"
    message_template = ("{expected}를(을) 반환하도록 정의 했음에도 불구하고,\n {location.line}번줄에서 함수가 {actual}을 반환했습니다."
                        "\n\n함수는 값을 일관되게 반환해야 합니다..!!")
    justification = ("TIFA visited a function definition with multiple returns "
                     "that unequal types.")

    def __init__(self, location, expected, actual, **kwargs):
        super().__init__(location=location, expected=expected,
                         actual=actual, **kwargs)


class write_out_of_scope(TifaFeedback):
    """ Write out of Scope """
    title = "Write Out of Scope"
    message_template = ("{location.line}번줄을 확인해보세요! \n더 높은 범위(함수 외부)에서 변수 {name_message}를 쓰려고 했습니다."
                        "\n\n변수가 선언 된 함수 내에서만 변수를 사용해야합니다.")
    justification = "TIFA stored to an existing variable not in this scope"

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class unconnected_blocks(TifaFeedback):
    """ Unconnected Blocks """
    title = "Unconnected Blocks"
    message_template = ("{location.line} 줄에 연결되지 않은 블록이있는 것 같습니다."
                        "\n\n프로그램을 실행하기 전에 모든 부분이 연결되어 있는지 확인해야합니다.")
    justification = "TIFA found a name equal to ___"

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class iteration_problem(TifaFeedback):
    """ Iteration Problem """
    title = "Iteration Problem"
    message_template = ("{name_message} 변수가 {location.line}번줄에서 반복되었지만 반복 변수와 동일한 변수를 사용했습니다. "
                        "\n반복 변수에 대해 다른 변수 이름을 선택해야합니다."
                        "\n\n일반적으로 반복 변수는 반복 목록의 단수 형식입니다 \n(예 : 'for a_dog in dogs :')")
    justification = "TIFA visited a loop where the iteration list and target were the same."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class initialization_problem(TifaFeedback):
    """ Initialization Problem """
    title = "Initialization Problem"
    message_template = ("{name_message} 변수가 {location.line}번줄에서 사용되었지만 이전에 값이 할당되지 않았습니다."
                        "\n\n값이 주어질 때까지 변수를 사용할 수 없습니다."
                        )
    justification = "TIFA read a variable that did not exist or was not previously set in this branch."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class possible_initialization_problem(TifaFeedback):
    """ Possible Initialization Problem """
    title = "Possible Initialization Problem"
    message_template = ("{name_message} 변수가 {location.line}번줄에서 사용되었지만 이전에 값이 할당되지 않았을수 있습니다."
                        "\n\n값이 주어질 때까지 변수를 사용할 수 없습니다."
                        "\n이 변수가 이전에 선언되었는지 확인하십시오."
                        )
    justification = "TIFA read a variable that was maybe set but not definitely set in this branch."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class unused_variable(TifaFeedback):
    """ Unused Variable """
    title = "Unused Variable"
    message_template = (" {location.line}번줄에서 {name_message} 변수가 선언되었지만 그 이후로는 사용되지 않았습니다.")
    justification = ("TIFA stored a variable but it was not read any other time "
                     "in the program.")

    def __init__(self, location, name, variable_type, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        if variable_type.is_equal('function'):
            kind, initialization = 'function', 'definition'
        else:
            kind, initialization = 'variable', 'value'
        fields = {'location': location, 'name': name, 'type': variable_type,
                  'name_message': report.format.name(name),
                  'kind': kind, 'initialization': initialization}
        if 'fields' in kwargs:
            fields.update(kwargs.pop('fields'))
        super().__init__(location=location, fields=fields, **kwargs)


class overwritten_variable(TifaFeedback):
    """ Overwritten Variable """
    title = "Overwritten Variable"
    message_template = ("변수 {name_message}에 값이 주어졌지만 {name_message} 변수가 사용되기 전에 {location.line}번줄에서 변경되었습니다."
                        "\n{name_message}에 값을 제공한 것들 중 하나가 잘못되었습니다"
                        )
    justification = ("TIFA attempted to store to a variable that was previously "
                     "stored but not read.")

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class iterating_over_non_list(TifaFeedback):
    """ Iterating over non-list """
    title = "Iterating over Non-list"
    message_template = ("{iter}는 리스트가 아닌데, {location.line}번줄의 반복에서 사용했습니다."
                        "\n\n리스트와 같은 시퀀스만 반복해야합니다.")
    justification = ("TIFA visited a loop's iteration list whose type was"
                     "not indexable.")

    def __init__(self, location, iter_name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        if iter_name is None:
            iter_list = "expression"
        else:

            iter_list = "variable " + report.format.name(iter_name)
        fields = {'location': location, 'name': iter_name, 'iter': iter_list}
        if 'fields' in kwargs:
            fields.update(kwargs.pop('fields'))
        super().__init__(location=location, fields=fields, **kwargs)


class iterating_over_empty_list(TifaFeedback):
    """ Iterating over empty list """
    title = "Iterating over empty list"
    message_template = ("{iter}가 빈 리스트로 선언된 다음 {location.line}번줄에 반복에서 사용하려고했습니다."
                        "\n\n비어 있지 않은 리스트만 반복해야합니다."
                        )
    justification = "TIFA visited a loop's iteration list that was empty."

    def __init__(self, location, iter_name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        if iter_name is None:
            iter_list = "expression"
        else:
            iter_list = "variable " + report.format.name(iter_name)
        fields = {'location': location, 'name': iter_name, 'iter': iter_list}
        super().__init__(location=location, fields=fields, **kwargs)


class incompatible_types(TifaFeedback):
    """ Incompatible types """
    title = "Incompatible types"
    # message_template = ("You used {op_name} operation with {left_name} and {right_name} on line "
    #                     "{location.line}. you can't do that with that operator. Make "
    #                     "sure both sides of the operator are the right type."
    #                     )

    message_template = ("{location.line}번줄을 확인해보세요.\n"
                    "{left_name} 타입과 {right_name}타입간에 {op_name} 연산을 하였습니다.\n"
                    "\n연산자 양쪽에 타입을 올바르게 해보세요!!"
                    )

    justification = "TIFA visited an operation with operands of the wrong type."

    def __init__(self, location, operation, left, right, **kwargs):
        op_name = OPERATION_DESCRIPTION.get(operation.__class__,
                                            str(operation))
        left_name = left.singular_name
        right_name = right.singular_name
        fields = {'location': location,
                  'operation': operation, 'op_name': op_name,
                  'left': left, 'right': right,
                  'left_name': left_name, 'right_name': right_name}
        super().__init__(location=location, fields=fields, **kwargs)


class invalid_indexing(TifaFeedback):
    """ Invalid Index """
    title = "Invalid Index"
    message_template = ("{location.line}번줄에서 {right_name}(으)로 {left_name}을(를) 인덱싱했습니다."
                        "\n\n{right_name}(으)로 {left_name}의 인덱싱을 할 수 없습니다."
                        )
    justification = ("TIFA attempted to call an .index() operation on a type"
                     " with a type that wasn't acceptable.")
    muted = True

    def __init__(self, location, left, right, **kwargs):
        left_name = left.singular_name
        right_name = right.singular_name
        fields = {'location': location,
                  'left': left, 'right': right,
                  'left_name': left_name, 'right_name': right_name}
        super().__init__(location=location, fields=fields, **kwargs)


class parameter_type_mismatch(TifaFeedback):
    """ Parameter type mismatch """
    title = "Parameter Type Mismatch"
    message_template = ("{location.line}번줄에서 {parameter_name_message} 매개변수를 {parameter_type_name}(으)로 정의했습니다. "
                        "\n\n그러나 해당 매개변수에 전달 된 인수는 {argument_type_name}입니다."
                        "\n형식 매개 변수 타입은 인자 타입과 일치해야합니다."
                        )
    justification = "TIFA visited a function definition where a parameter type and argument type were not equal."

    def __init__(self, location, parameter_name, parameter, argument, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        parameter_type_name = parameter.singular_name
        argument_type_name = argument.singular_name
        fields = {'location': location,
                  'parameter_name': parameter_name,
                  'parameter_name_message': report.format.name(parameter_name),
                  'parameter_type': parameter,
                  'argument_type': argument,
                  'parameter_type_name': parameter_type_name,
                  'argument_type_name': argument_type_name}
        super().__init__(location=location, fields=fields, **kwargs)


class read_out_of_scope(TifaFeedback):
    """ Read out of scope """
    title = "Read out of Scope"
    message_template = ("{location.line}번줄의 다른 범위에서 {name_message} 변수를 읽으려고했습니다."
                        "\n\n변수가 선언 된 함수 내에서만 변수를 사용해야합니다."
                        )
    justification = "TIFA read a variable that did not exist in this scope but existed in another."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


# TODO: Complete these
class type_changes(TifaFeedback):
    """ Type changes """
    title = "Type Changes"
    message_template = ("{name_message} 변수가 {location.line}번줄에서 타입을 {old}에서 {new}로 변경했습니다.")
    justification = ""
    muted = True

    def __init__(self, location, name, old, new, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        fields = {'location': location, 'name': name,
                  'name_message': report.format.name(name),
                  'old': old, 'new': new}
        super().__init__(location=location, fields=fields, **kwargs)


class unnecessary_second_branch(TifaFeedback):
    """ Unnecessary second branch """
    title = "Unnecessary Second Branch"
    message_template = ("{location.line}번줄에 'pass'만 있는 'if'문이 있습니다. "
                        "\n\n빈 내용은 필요하지 않습니다.")
    justification = "There is an else or if statement who's body is just pass."

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class else_on_loop_body(TifaFeedback):
    """ Else on Loop body """
    title = "Else on Loop Body"
    message_template = "TODO"
    justification = ""

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class recursive_call(TifaFeedback):
    """ recursive call """
    title = "Recursive Call"
    message_template = "TODO"
    justification = ""
    muted = True

    def __init__(self, location, name, **kwargs):
        super().__init__(location=location, name=name, **kwargs)


class not_a_function(TifaFeedback):
    """ Not a function """
    title = "Not a Function"
    message_template = ("{location.line}번줄의 함수인 것처럼 {name}을(를) 호출하려고 했습니다."
                        "\n\n하지만 함수가 아니라 {called_type}타입인 객체입니다!")
    justification = ""
    # TODO: Unmute?
    #muted = True

    def __init__(self, location, name, called_type, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        singular_name = called_type.singular_name
        fields = {'location': location, 'name': name,
                  'called_type': called_type,
                  'singular_name': singular_name}
        super().__init__(fields=fields, **kwargs)


class incorrect_arity(TifaFeedback):
    """ Incorrect arity """
    title = "Incorrect Arity"
    message_template = ("함수 {function_name_message}에 잘못된 인수가 있습니다.")
    justification = ""

    def __init__(self, location, function_name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, function_name=function_name,
                         function_name_message=report.format.name(function_name),
                         **kwargs)


class module_not_found(TifaFeedback):
    """ Module not found """
    title = "Module Not Found"
    message_template = "TODO"
    justification = ""
    muted = True

    def __init__(self, location, name, is_dynamic=False, error=None, **kwargs):
        fields = {"location": location, "name": name,
                  "is_dynamic": is_dynamic, "error": error}
        super().__init__(location=location, fields=fields, **kwargs)


class append_to_non_list(TifaFeedback):
    """ Append to non-list """
    title = "Append to non-list"
    message_template = "TODO"
    justification = ""
    muted = True

    def __init__(self, location, name, actual_type, **kwargs):
        fields = {'location': location, "name": name,
                  "actual_type": actual_type}
        super().__init__(location=location, fields=fields, **kwargs)


class nested_function_definition(TifaFeedback):
    """ Function defined not at top-level """
    message_template = ("{location.line}번 줄에 다른 블록 내에 {name_message} 함수가 정의되었습니다. "
                        "\n예를 들어, 다른 함수 정의 또는 루프 내부에 배치했을 수 있습니다."
                        "\n\n함수 정의를 중첩하지 마십시오!")
    title = "Don't Nest Functions"
    justification = "Found a FunctionDef that was not at the top-level."
    muted = True
    unscored = True

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class unused_returned_value(TifaFeedback):
    """ Expr node had a non-None value """
    title = "Did Not Use Function's Return Value"
    message_template = ("{location.line}번줄에서 {call_type} {name_message}(을)를 호출했지만 결과를 사용하지 않은 것 같습니다."
                        "\n\n리턴값 사용하는 것을 기억해야합니다!")
    justification = "Expression node calculated a non-None value."
    muted = True
    unscored = True

    def __init__(self, location, name, call_type, result_type, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        fields = {'location': location, 'name': name, 'call_type': call_type,
                  'result_type': result_type,
                  'name_message': report.format.name(name)}
        super().__init__(fields=fields, location=location, **kwargs)


'''
TODO: Finish these checks
"Empty Body": [], # Any use of pass on its own
"Malformed Conditional": [], # An if/else with empty else or if
"Unnecessary Pass": [], # Any use of pass
"Append to non-list": [], # Attempted to use the append method on a non-list
"Used iteration list": [], #
"Unused iteration variable": [], #
"Type changes": [], #
"Unknown functions": [], #
"Not a function": [], # Attempt to call non-function as function
"Recursive Call": [],
"Incorrect Arity": [],
"Aliased built-in": [], #
"Method not in Type": [], # A method was used that didn't exist for that type
"Submodule not found": [],
"Module not found": [],
"Else on loop body": [], # Used an Else on a For or While
'''

# TODO: Equality instead of assignment
