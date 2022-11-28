import re

COLOR_REGEXP = r'^(#(?:[0-9a-fA-F]{3}){1,2}|hsl\((\s){0,}(\d|[1-9]\d|[12]\d{2}|3[0-5]\d|360){1,3}(\s){0,},(\s){0,}([0-9]|[1-9][0-9]|100)%(\s){0,},(\s){0,}([0-9]|[1-9][0-9]|100)%(\s){0,}\)|rgb\((\s){0,}([0-9]|[1-9][0-9]|100)%(\s){0,},(\s){0,}([0-9]|[1-9][0-9]|100)%(\s){0,},(\s){0,}([0-9]|[1-9][0-9]|100)%(\s){0,}\)|rgb\((\s){0,}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\s){0,},(\s){0,}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\s){0,},(\s){0,}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\s){0,}\))$'
PASSWORD_REGEXP = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^$%@#&*!?])\b(([A-Za-z\d^$%@#&*!?])((?!\2))){8,}'
OPERATOR = r'(?P<operator>[\^*\/\-+])'
PARENTHESIS = r'(?P<left_parenthesis>\()|(?P<right_parenthesis>\))'
FUNCTION = r'(?P<function>\b(sin|cos|tg|ctg|tan|cot|sinh|cosh|th|cth|tanh|coth|ln|lg|log|exp|sqrt|cbrt|abs|sign)\b)'
CONSTANT = r'(?P<constant>\b(pi|e|sqrt2|ln2|ln10)\b)'
NUMBER = r'(?P<number>((\d+\.\d+)|\d+))'
VARIABLE = r'(?P<variable>[a-zA-Z_][0-9a-zA-Z_]*)'
EXPRESSION_REGEXP = fr'{OPERATOR}|{PARENTHESIS}|{FUNCTION}|{CONSTANT}|{NUMBER}|{VARIABLE}'
# regexp = re.compile(EXPRESSION_REGEXP)
# for match in regexp.finditer("pi e pie 111.111.111 11 11.11"):
#     print(f'type: {match.lastgroup}, span: {match.span()}')
DAY1_30 = r'(((0|\b)[1-9])|[12][0-9]|30)'
MONTH1_30 = r'((0|\b)(4|6|9)|11)'
DAY1_31 = r'(((0|\b)[1-9])|[12][0-9]|3[01])'
MONTH1_31 = r'((0|\b)(1|3|5|7|8)|10|12)'
DAY1_28 = r'(((0|\b)[1-9])|1[0-9]|2[0-8])'
MONTH1_28 = r'(0|\b)2'
YEAR = r'\d{1,}'
MONTH1_30_RU = r'(апреля|июня|сентября|ноября)'
MONTH1_31_RU = r'(января|марта|мая|июля|августа|октября|декабря)'
MONTH1_28_RU = r'февраля'
MONTH1_30_ENG = r'(April|Apr|June|Jun|September|Sep|November|Nov)'
MONTH1_31_ENG = r'(January|Jan|March|Mar|May|July|Jul|August|Aug|October|Oct|December|Dec)'
MONTH1_28_ENG = r'(Feb|February)'
DATES_REGEXP = fr'^({DAY1_30}\/{MONTH1_30}\/|{DAY1_31}\/{MONTH1_31}\/|{DAY1_28}\/{MONTH1_28}\/){YEAR}$|' \
               fr'^({DAY1_30}-{MONTH1_30}-|{DAY1_31}-{MONTH1_31}-|{DAY1_28}-{MONTH1_28}-){YEAR}$|' \
               fr'^({DAY1_30}\.{MONTH1_30}\.|{DAY1_31}\.{MONTH1_31}\.|{DAY1_28}\.{MONTH1_28}\.){YEAR}$|' \
               fr'^{YEAR}(\.{MONTH1_30}\.{DAY1_30}|\.{MONTH1_31}\.{DAY1_31}|\.{MONTH1_28}\.{DAY1_28}$)|' \
               fr'^{YEAR}(\/{MONTH1_30}\/{DAY1_30}|\/{MONTH1_31}\/{DAY1_31}|\/{MONTH1_28}\/{DAY1_28}$)|' \
               fr'^{YEAR}(-{MONTH1_30}-{DAY1_30}|-{MONTH1_31}-{DAY1_31}|-{MONTH1_28}-{DAY1_28}$)|' \
               fr'^({DAY1_30}\s+{MONTH1_30_RU}\s+|{DAY1_31}\s+{MONTH1_31_RU}\s+|{DAY1_28}\s+{MONTH1_28_RU}\s+){YEAR}$|' \
               fr'^({MONTH1_30_ENG}\s+{DAY1_30},\s*|{MONTH1_31_ENG}\s+{DAY1_31},\s*|{MONTH1_28_ENG}\s+{DAY1_31},\s*){YEAR}$|' \
               fr'^{YEAR}(.\s*{MONTH1_30_ENG}\s+{DAY1_30}|,\s*{MONTH1_31_ENG}\s+{DAY1_31}|,\s*{MONTH1_28_ENG}\s+{DAY1_31})$'
print(DATES_REGEXP)
