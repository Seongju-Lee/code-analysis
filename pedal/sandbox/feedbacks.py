"""
Generic runtime exception feedback class.
"""
from pedal.core.location import Location
from pedal.core.report import MAIN_REPORT
from pedal.sandbox.data import format_contexts
from pedal.utilities.exceptions import KeyError, get_exception_name
from pedal.core.feedback import FeedbackResponse
from pedal.sandbox import TOOL_NAME
from pedal.utilities.text import add_indefinite_article

RUNTIME_ERROR_MESSAGE_HEADER = (
    "{exception_name}가 발생:\n\n"
    "{exception_message}\n\n"
    "{context_message}\n"
    "에러발생 부분은 아래와 같습니다:\n{traceback_message}\n"
)
# lsj

class runtime_error(FeedbackResponse):
    """
    Used to create all runtime errors.

    Attributes:
        exception (Exception): The original exception.
        exception_name (str): The original name of the exception.
        exception_message (str): the original error message from the exception.
        traceback (:py:class:`~pedal.utilities.exceptions.ExpandedTraceback`):
            An enhanced version of the builtin Traceback object. Has a number
            of additional fields.
        traceback_message (str): A nicely formatted version of the traceback.
        context (list[:py:class:`~pedal.sandbox.data.SandboxContext`]): The
            history of inputs, outputs, executed code, and other information
            from when this runtime error occurred. Usually just a single
            element, but sometimes longer if created in a grouping context.
            If the code was run from a file, then the filename is given.

    """
    tool = TOOL_NAME
    category = FeedbackResponse.CATEGORIES.RUNTIME
    kind = FeedbackResponse.KINDS.MISTAKE
    justification = "A runtime error occurred during execution of some code."
    version = '1.1.0'
    message_template = RUNTIME_ERROR_MESSAGE_HEADER

    def __init__(self, exception, context, traceback, location, **kwargs):
        report = kwargs.get('report', MAIN_REPORT)
        exception_name = get_exception_name(exception)
        exception_name_proper = add_indefinite_article(exception_name)
        exception_message = str(exception).capitalize()
        if type(exception) not in EXCEPTION_FF_MAP:
            title = exception_name
        else:
            title = EXCEPTION_FF_MAP[type(exception)].title
        location = Location(location)
        traceback_stack = traceback.build_traceback()
        traceback_message = traceback.format_traceback(traceback_stack,
                                                       report.format)
        context_message = format_contexts(context, report.format)
        fields = {'exception': exception,
                  'exception_name': exception_name_proper,
                  'exception_message': report.format.exception(exception_message),
                  'location': location,
                  'traceback': traceback,
                  'traceback_stack': traceback_stack,
                  'traceback_message': traceback_message,
                  'context': context,
                  'context_message': context_message}
        super().__init__(fields=fields, title=title,
                         location=location, **kwargs)



class type_error(runtime_error):
    """ Type Error """
    title = "Type Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "타입 에러는 연산할때나 잘못된 값의 함수를 사용할 때 발생합니다\n"
                        "예를 들어, '+'를 이용하여 리스트에 값을 더하거나(append 대신에)\n "
                        "문자열을 숫자로 나눌 때 발생합니다."
                        "\n\n"
                        "피드백 내용: 타입에러를 고치기 위해서 코드를 쭉 보세요."
                        "각 식에 올바른 타입이 들어갔는지 천천히 살펴보세요!")


class name_error(runtime_error):
    """ Runtime NameError """
    title = "Name Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "name error는 변수가 없는 것을 의미합니다.\n"
                        "변수 철자를 확인해보거나 다시 입력해보세요."
                        "또는 변수 초기화를 하지 않았는지도 확인해보세요\n"
                        "\n"
                        "피드백 내용: 코드를 처음부터 잘 살펴보면서 틀린 부분을 확인해보세요!!")



class value_error(runtime_error):
    """ Runtime ValueError """
    title = "Value Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "ValueError는 잘못된 타입의 값을 함수에 전달할 때 발생합니다.\n"
                        "예를 들어, 문자를 숫자형으로 바꾼다고 시도하는 경우입니다.("
                        "`int('Five')`).\n\n"
                        "피드백 내용: 에러메시지를 잘 읽어보세요."
                        "타입과 관련돼서 잘못되게 함수를 호출하지 않았는지 확인해보세요!!"
                        )


class attribute_error(runtime_error):
    """ Runtime AttributeError """
    title = "Attribute Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "AttributeError는 속성이나 메소드가 존재하지 않는 것입니다."
                        "예를 들어, `delete`라는 메소드는 없는데, `text.delete()`라는 코드를 입력했을 때입니다.\n"
                        "\n\n"
                        "피드백 내용: 메소드나 속성을 올바르게 입력했는지 확인해보세요\n"
                        "메소드 호출을 위한 `.`도 올바르게 쓰여졌는지도 확인해보세요!!")


class index_error(runtime_error):
    """ Runtime IndexError """
    title = "Index Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "IndexError는 문자열이나 리스트에서 없는 자리를 인덱싱한 것입니다.\n"
                        "예를 들어, 3개의 값이 들어있는 리스트에서 5번 자리를 인덱싱하는 것입니다.\n\n"
                        "피드백 내용: 인덱스 번호는 맨 첫자리가 0이라는 것을 반드시 기억하세요!!")


class zero_division_error(runtime_error):
    """ Runtime ZeroDivisionError """
    title = "Division by Zero Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "ZeroDivisionError는 0으로 나누었을 때 나타나는 것입니다.\n"
                        "\n\n"
                        "피드백 내용: 나눗셈을 정확한 값으로 했는 지 확인해보세요!!")


class indentation_error(runtime_error):
    """ Syntax IndentationError """
    title = "Indentation Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "IndentationError는 들여쓰기가 올바르지 않은 것입니다."
                        "공백이 너무 많거나 적은지 확인해보세요\n\n"
                        "피드백 내용: 줄 번호를 확인하고 앞줄, 뒷줄을 잘 살펴보세요.\n"
                        "그리고, 각 함수의 정의나 부분도 잘 보세요."
                        "참고로 모든 하나의 구문(if, for등)은 같은 들여쓰기여야 합니다!!")


class import_error(runtime_error):
    """ Runtime ImportError """
    title = "Import Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "ImportError는 불러올 모듈이 존재하지 않다는 것입니다."
                        "올바르게 임포트할 내용을 적었는 지 확인하세요.\n\n"
                        "피드백 내용: 모듈의 이름을 잘 확인해보거나, 위에 존재하는 라이브러리 추가를 했는지 확인하세요.\n"
                        "만약 다 정확하다면, 파일의 경로 중 폴더가 있는 폴더인지 확인해보세요!!")


class io_error(runtime_error):
    """ Runtime IOError """
    title = "Input/Output Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "IOError는 존재하지 않는 파일을 열려고 할 때 발생됩니다."
                        "\n\n"
                        "피드백 내용: 파일이 정확한 폴더에 있는 지 확인하고,\n파일명이나 폴더명도 꼭 확인해보세요!")

class key_error(runtime_error):
    """ Runtime KeyError """
    title = "Key Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "KeyError는 딕셔너리에서 존재하지 않는 키를 조회할 때 발생합니다."
                        "\n\n"
                        "피드백 내용: 첫째, 키의 이름을 올바르게 입력했는 지 확이하세요.\n"
                        "이름이 맞다면, 딕셔너리에 그 키가 있는 지 직접 확인해보세요!!")


class memory_error(runtime_error):
    """ Runtime MemoryError """
    title = "Memory Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "MemoryError는 현재 프로그램이 너무 힘든 것입니다.\n\n"
                        "피드백 내용: 무한 반복문이 있는 지 확인해보세요\n"
                        "없다면, 데이터를 충분히 가공하고 사용해보세요!")


class timeout_error(runtime_error):
    """ Runtime TimeoutError """
    title = "Timeout Error"
    message_template = (RUNTIME_ERROR_MESSAGE_HEADER + "\n" +
                        "A TimeoutError means your program took too long to "
                        "run.\n\n"
                        "Suggestion: Check that you do not have an infinite "
                        "loop.")


EXCEPTION_FF_MAP = {
    TypeError: type_error,
    NameError: name_error,
    ValueError: value_error,
    AttributeError: attribute_error,
    IndexError: index_error,
    ZeroDivisionError: zero_division_error,
    IndentationError: indentation_error,
    ImportError: import_error,
    IOError: io_error,
    KeyError: key_error,
    MemoryError: memory_error,
    TimeoutError: timeout_error,
}
