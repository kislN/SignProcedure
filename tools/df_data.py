from copy import deepcopy


def for_normal(data):
    tuples = []
    for meth in data['20_obs']:
        if meth == 'pearson' or meth == 'sign':
            tuples.append([meth, '-', '-'])
            continue
        d_1 = [meth]
        for alpha in data['20_obs'][meth]:
            d_1.append(alpha.split('_')[0])
            for algo in data['20_obs'][meth][alpha]:
                d_1.append(algo)
                tuples.append(deepcopy(d_1))
                d_1.pop()
            d_1.pop()
    values = []
    for obj in tuples:
        l = []
        for obs in data:
            if obj[0] == 'pearson' or obj[0] == 'sign':
                l.append(data[obs][obj[0]])
            else:
                l.append(data[obs][obj[0]][obj[1]+'_alpha'][obj[2]])
        values.append(l)
    return tuples, values


def for_stud(data):
    tuples = []
    for dof in data['20_obs']:
        for meth in data['20_obs'][dof]:
            if meth == 'pearson' or meth == 'sign':
                tuples.append([dof.split('_')[0], meth, '-', '-'])
                continue
            d_1 = [dof.split('_')[0], meth]
            for alpha in data['20_obs'][dof][meth]:
                d_1.append(alpha.split('_')[0])
                for algo in data['20_obs'][dof][meth][alpha]:
                    d_1.append(algo)
                    tuples.append(deepcopy(d_1))
                    d_1.pop()
                d_1.pop()
    values = []
    for obj in tuples:
        l = []
        for obs in data:
                if obj[1] == 'pearson' or obj[1] == 'sign':
                    l.append(data[obs][obj[0]+'_dof'][obj[1]])
                else:
                    l.append(data[obs][obj[0]+'_dof'][obj[1]][obj[2]+'_alpha'][obj[3]])
        values.append(l)
    return tuples, values

def for_mix(data):
    tuples = []
    for rate in data['20_obs']:
        for dof in data['20_obs'][rate]:
            for meth in data['20_obs'][rate][dof]:
                if meth == 'pearson' or meth == 'sign':
                    tuples.append([rate.split('_')[0], dof.split('_')[0], meth, '-', '-'])
                    continue
                d_1 = [rate.split('_')[0], dof.split('_')[0], meth]
                for alpha in data['20_obs'][rate][dof][meth]:
                    d_1.append(alpha.split('_')[0])
                    for algo in data['20_obs'][rate][dof][meth][alpha]:
                        d_1.append(algo)
                        tuples.append(deepcopy(d_1))
                        d_1.pop()
                    d_1.pop()
    values = []
    for obj in tuples:
        l = []
        for obs in data:
                if obj[2] == 'pearson' or obj[2] == 'sign':
                    l.append(data[obs][obj[0]+'_nRate'][obj[1]+'_dof'][obj[2]])
                else:
                    l.append(data[obs][obj[0]+'_nRate'][obj[1]+'_dof'][obj[2]][obj[3]+'_alpha'][obj[4]])
        values.append(l)
    return tuples, values

