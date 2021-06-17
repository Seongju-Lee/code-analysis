from pedal import *
# ########################
# # 함수 매칭 유무 확인
# ########################
# match = find_match("""
# def summate():
#     __expr__
# """)

# if not match:
#     explain("함수가 정의되지 않았습니다.", label="function_missing")


# ########################
# # sum VS count
# ########################

# assert_equal(call('summate', [1,3,5]), 9) # 임의로 backend에서 인자를 넣어서 맞으면 True, 틀리면 False




# ########################
# # 다음으로 할 내용은...?
# ########################


# # Make sure they don't embed the answer
# prevent_literal(10)
# # Make sure they DO use these integers
# ensure_literal(7)
# ensure_literal(3)
# # Make sure they print
# ensure_function_call('print')
# # Make sure they used addition operator
# ensure_operation("+")
# # Give message if they try to use strings instead of numbers
# prevent_ast("Str")
# # Check the actual output
# assert_output(student, "7")


# Partial credit for good progress
if find_asts("For"):
    compliment("Good, you have a `for` loop!", score="+10%")

# Give feedback by finding a common problem-specific mistake
matches = find_matches("for _expr_ in _list_:\n"
                       "    ___ = ____ + _list_")
if matches:
    explain("You shouldn't use the list inside the for loop.",
            label="list_inside_loop", title="List Inside Loop")

# Check they defined the function with the right type
# 함수 정의와 리턴 타입 올바른 지 확인
# ensure_function('add_prices', returns=int)
# Unit test their function

# 함수 결과가 입력과 출력과 같은지 확인 -> 메시지 출력
# assert_equal(call('add_prices', [1,2,3]), 6)
# ensure_function_call('add_prices')