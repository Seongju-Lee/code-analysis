from pedal import *


########################
# 함수 매칭 유무 확인
########################
match = find_match("""
def summate():
    __expr__
""")

if not match:
    explain("함수가 정의되지 않았습니다.", label="function_missing")


########################
# sum VS count
########################

assert_equal(call('summate', [1,3,5]), 9) # 임의로 backend에서 인자를 넣어서 맞으면 True, 틀리면 False




########################
# 다음으로 할 내용은...?
########################

