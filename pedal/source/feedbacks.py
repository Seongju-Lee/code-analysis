"""
Feedback functions of the Source module
"""

from pedal.core.commands import feedback
from pedal.core.feedback import FeedbackResponse
from pedal.core.location import Location
from pedal.core.report import MAIN_REPORT
from pedal.utilities.exceptions import ExpandedTraceback
from pedal.source.constants import TOOL_NAME


class SourceFeedback(FeedbackResponse):
    """ Base class of all Feedback functions for Source Tool """
    category = feedback.CATEGORIES.SYNTAX
    kind = feedback.KINDS.MISTAKE
    tool = TOOL_NAME


class blank_source(SourceFeedback):
    """ Source code file was blank. """
    title = "빈 소스코드"
    message_template = "소스코드가 비어있습니다.\n\n 코드를 입력하세요!!"
    justification = "After stripping the code, there were no characters."


class not_enough_sections(SourceFeedback):
    """ Didn't have all the needed sections. """
    title = "충분하지 않는 섹션"
    message_template = ("Tried to advance to next section but the "
                        "section was not found. Tried to load section "
                        "{count}, but there were only {found} sections.")
    justification = ("Section index exceeded the length of the separated "
                     "sections list.")

    def __init__(self, section_number, found, **kwargs):
        fields = {'count': section_number, 'found': found}
        super().__init__(fields=fields, **kwargs)


class source_file_not_found(SourceFeedback):
    """ No source file was given. """
    title = '소스파일 없음'
    message_template = ("'{name:filename}'이라는 파일 이름은 없거나, 열 수 없습니다"
                        "\n\n파일이 이용 가능한지 확실히 확인해주세요!")
    version = '0.0.1'
    justification = "IOError while opening file to set_source"

    def __init__(self, name, sections, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        fields = {'name': name, 'sections': sections}
        group = 0 if sections else kwargs.get('group')
        super().__init__(fields=fields, group=group, **kwargs)


class syntax_error(SourceFeedback):
    """ Generic feedback for any kind of syntax error. """
    muted = False
    title = "구문에러"
    message_template = ("{lineno:line}번줄의 구문이 잘못되었습니다.\n\n"
                        "에러메시지:\n{traceback_message}\n\n"
                        "해결 피드백: {lineno:line}번줄을 잘 확인하세요"
                        "전 줄이나 다음 줄도 잘 확인해보세요!")
    version = '0.0.1'
    justification = "Syntax error was triggered while calling ast.parse"

    def __init__(self, line, filename, code, col_offset,
                 exception, exc_info, **kwargs):
        report = kwargs.get('report', MAIN_REPORT)
        files = report.submission.get_files_lines()
        if filename not in files:
            files[filename] = code.split("\n")
        if report.submission is not None:
            lines = report.submission.get_lines()
            line_offsets = report.submission.line_offsets
        else:
            lines = code.split("\n")
            line_offsets = {}
        line_offset = line_offsets.get(filename, 0)
        traceback = ExpandedTraceback(exception, exc_info, False,
                                      [report.submission.instructor_file],
                                      line_offsets, [filename], lines, files)
        traceback_stack = traceback.build_traceback()
        traceback_message = traceback.format_traceback(traceback_stack,
                                                       report.format)
        line_offset = line_offsets.get(filename, 0)
        fields = {'lineno': line+line_offset,
                  'filename': filename, 'offset': col_offset,
                  'exception': exception,
                  'traceback': traceback,
                  'traceback_stack': traceback_stack,
                  'traceback_message': traceback_message}
        location = Location(line=line+line_offset, col=col_offset, filename=filename)
        super().__init__(fields=fields, location=location, **kwargs)


class incorrect_number_of_sections(SourceFeedback):
    """ Incorrect number of sections """
    title = "섹션의 수 틀림"
    message_template = ("섹션 수가 올바르지 않습니다."
                     "필요한 수: {count}, 현재 개수: {found}")
    justification = ""

    def __init__(self, count, found, **kwargs):
        fields = {'count': count, 'found': found}
        super().__init__(fields=fields, **kwargs)

# TODO: IndentationError
# TODO: TabError
