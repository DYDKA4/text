import re

parenthesis_1 = r'((\(%\))|({%})|(\[%\]))*'
result = r'^((\(\))*|({})*|(\[\])*)*$'
for _ in range(8):
    to_change = parenthesis_1
    result = result.replace('\(\)', '\(' + to_change + '\)').replace('{}', '{' + to_change + '}').replace('\[\]', '\[' + to_change + '\]')
    result = result.replace('%', '')
    #print(result)
# print(result)
PARENTHESIS_REGEXP = result
SENTENCES_REGEXP = r'(?P<sentence>[A-Я][^.!?]*[.!?])'
PERSONS_REGEXP = r'(?P<person>([А-Я][а-я]+\s[А-Я][а-я]+))'
NAME = r'<td><h1 class="level2"><a class="all" href="\/series\/\d+\/">(?P<name>().+)<\/a>'
EPISODES_COUNT = r'<td class="news">(?P<episodes_count>(\d+))<\/td>'
SEASON = r'<td class="news" colspan="2" style="color:#777;padding:10px 0px;border-bottom:3px solid #ccc">' \
         r'<h1 class="moviename-big" style="font-size:21px;padding:0px;margin:0px;color:#f60">Сезон ' \
         r'(?P<season>(\d+))<\/h1>\n\s+(?P<season_year>(\d{4})),\s[а-я]+:\s(?P<season_episodes>\d+)'
SERIES = r'<span style="color:#777">Эпизод (?P<episode_number>(\d+))<\/span><br\/>\n|<h1 class="moviename-big" ' \
         r'style="font-size:16px;padding:0px;color:#444"><b>(?P<episode_name>.+)<\/b><\/h1>\n|<span ' \
         r'class="episodesOriginalName">(?P<episode_original_name>(.+))<\/span> ' \
         r'<\/td>\n|<td align="left" class="news" style="border-bottom:1px dotted #ccc;padding:15px ' \
         r'0px;font-size:12px" valign="bottom" width="20%">(?P<episode_date>(.+))<\/td>'
SERIES_REGEXP = fr'{NAME}|{EPISODES_COUNT}|{SEASON}|{SERIES}'

# print(SERIES)
# entities = set()
# regexp = re.compile(SERIES_REGEXP)
# file = open('series/77164.html', 'r')
# file = file.read()
# for match in regexp.finditer(file):
#     for key, value in match.groupdict().items():
#         if value is not None:
#             start, end = match.span(key)
#             entities.add((start, end, key))
# file = open('out.txt', 'w')
# entities = list(entities)
# entities.sort()
# for i in entities:
#     file.write(str(i)+'\n')
# file.close()
