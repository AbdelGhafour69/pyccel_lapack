import json


with open('subroutines.json') as json_file:
    data = json.load(json_file)

subroutines = data.keys()

mapper = {
    'real': 'float32',
    'double precision': 'double',
    'integer': 'int32',
    'character': 'char',
    'logical': 'bool',
    ', dimension( * )': '[:]',
    'else': '[:,:](order=F)'
}
headers = ''
for routine in subroutines:
    #print('Im in routine ', routine, '\n')
    types = data[routine].values()
    starter = '#$ header function ' + routine+'('
    for t in types:
        ss = t.split(',')
        starter += mapper[ss[0]]
        if len(ss) > 1:
            # print(ss)
            if ss[1] == ' dimension( * )':
                starter += mapper[','+ss[1]]
            else:
                starter += mapper['else']
        starter += ','
    starter = list(starter)
    starter[-1] = ')'
    str = ''.join(starter)
    headers += str + '\n'

with open('lapack.pyh', 'w') as fp:
    fp.write(headers)

fp.close()
