def prop_rels_comp(prop_matrix):

    conf_matrix = [[0, 0], [0, 0]]

    for rel_dict in prop_matrix:
        ID1 = rel_dict['ID1']
        ID2 = rel_dict['ID2']
        text1 = rel_dict['text1']
        text2 = rel_dict['text2']

        if ID1 != 0 and ID2 != 0:

            ras1 = [0, 1]  # Assuming ras values for ID1
            cas1 = [0, 0]  # Assuming cas values for ID1
            mas1 = [0, 0]  # Assuming mas values for ID1
            ras2 = [0, 1]  # Assuming ras values for ID2
            cas2 = [0, 0]  # Assuming cas values for ID2
            mas2 = [0, 0]  # Assuming mas values for ID2

            if ras1 == ras2:
                conf_matrix[0][0] += 1
            elif ras1 > ras2:
                conf_matrix[1][0] += 1
            elif ras2 > ras1:
                conf_matrix[0][1] += 1

            if cas1 == cas2:
                conf_matrix[0][0] += 1
            elif cas1 > cas2:
                conf_matrix[1][0] += 1
            elif cas2 > cas1:
                conf_matrix[0][1] += 1

            if mas1 == mas2:
                conf_matrix[0][0] += 1
            elif mas1 > mas2:
                conf_matrix[1][0] += 1
            elif mas2 > mas1:
                conf_matrix[0][1] += 1
        elif ID1 == 0 and ID2 == 0:
            conf_matrix[1][1] += 1
        elif ID1 == 0:
            conf_matrix[0][1] += 1
        elif ID2 == 0:
            conf_matrix[1][0] += 1

    overallRelations = len(prop_matrix) * len(prop_matrix)

    total_agreed_none = overallRelations - conf_matrix[0][0] - conf_matrix[0][1] - conf_matrix[1][0]

    if total_agreed_none < 0:
        total_agreed_none = 0
    conf_matrix[1][1] = total_agreed_none

    # conf_matrix[1][1] = total_agreed_none

    return conf_matrix


prob_matrix = [{'ID1': 4, 'ID2': 4, 'text1': '50 years ago finishing high was seen as the standard of education and was somewhat expected of people', 'text2': '50 years ago finishing high was seen as the standard of education and was somewhat expected of people'}, {'ID1': 7, 'ID2': 7, 'text1': '|Wilma: a college degree today is the equivalent of what a high school degree was 50 years ago', 'text2': '|Wilma: a college degree today is the equivalent of what a high school degree was 50 years ago'}]

result = prop_rels_comp(prob_matrix)
print(result)
