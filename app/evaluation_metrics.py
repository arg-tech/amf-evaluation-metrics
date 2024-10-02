from app.matching import match
from pycm import *
import json
import os


class evaluation:


    @staticmethod
    def matching_calculation(data1, data2):
        json1 = data1['AIF']
        json2 = data2['AIF']
        # Graph construction
        graph1,graph2= match.get_graphs(json1, json2)
        # creating proposition similarity matrix relations
        prop_rels = match.get_prop_sim_matrix(graph1, graph2)
        # print(prop_rels)
        # print('prop_rels',prop_rels)

        # creating locution similarity matrix relations
        loc_rels = match.get_loc_sim_matrix(graph1, graph2)
        # anchoring on s-nodes (RA/CA/MA) and combining them
        ra_a = match.ra_anchor(graph1, graph2)
        ma_a = match.ma_anchor(graph1, graph2)
        ca_a = match.ca_anchor(graph1, graph2)
        all_a = match.combine_s_node_matrix(ra_a, ca_a, ma_a)
        all_s_a_dict = match.convert_to_dict(all_a)
        # propositional relation comparison
        prop_rels_comp_conf = match.prop_rels_comp(prop_rels,graph1, graph2)
        # print('prop_rels_comp_conf',prop_rels_comp_conf)
        prop_rels_comp_dict = match.convert_to_dict(prop_rels_comp_conf)
        # print('prop_rels_comp_dict',prop_rels_comp_dict)
       # getting all YAs anchored in Locutions
        loc_ya_rels_comp_conf = match.loc_ya_rels_comp(loc_rels, graph1, graph2)
        loc_ya_rels_comp_dict = match.convert_to_dict(loc_ya_rels_comp_conf)
        # getting all YAs in propositions
        prop_ya_comp_conf = match.prop_ya_comp(prop_rels, graph1, graph2)
        prop_ya_comp_dict = match.convert_to_dict(prop_ya_comp_conf)
        # getting all TAs anchored in Locutions
        loc_ta_conf = match.loc_ta_rels_comp(loc_rels, graph1, graph2)
        loc_ta_dict = match.convert_to_dict(loc_ta_conf)
        # getting all YAs anchored in propositions
        prop_ya_conf = match.prop_ya_anchor_comp(prop_rels, graph1, graph2)
        prop_ya_dict = match.convert_to_dict(prop_ya_conf)


        # creating confusion matrix for s-nodes/YA/TA
        all_s_a_cm = ConfusionMatrix(matrix=all_s_a_dict)
        prop_rels_comp_cm = ConfusionMatrix(matrix=prop_rels_comp_dict)
        loc_ya_rels_comp_cm = ConfusionMatrix(matrix=loc_ya_rels_comp_dict)
        prop_ya_comp_cm = ConfusionMatrix(matrix=prop_ya_comp_dict)
        loc_ta_cm = ConfusionMatrix(matrix=loc_ta_dict)
        prop_ya_cm = ConfusionMatrix(matrix=prop_ya_dict)


        return all_s_a_cm,prop_rels_comp_cm,loc_ya_rels_comp_cm,prop_ya_comp_cm,loc_ta_cm,prop_ya_cm



    # Kappa range from -1 to +1
    @staticmethod
    def kappa_calculation(all_s_a_cm,prop_rels_comp_cm,loc_ya_rels_comp_cm,prop_ya_comp_cm,loc_ta_cm,prop_ya_cm):
        # kappa calculation
        s_node_kapp = all_s_a_cm.Kappa
        prop_rel_kapp = prop_rels_comp_cm.Kappa
        loc_rel_kapp = loc_ya_rels_comp_cm.Kappa
        prop_ya_kapp = prop_ya_comp_cm.Kappa
        loc_ta_kapp = loc_ta_cm.Kappa
        prop_ya_an_kapp = prop_ya_cm.Kappa


        if match.check_none(s_node_kapp):
            s_node_kapp = all_s_a_cm.KappaNoPrevalence
        if match.check_none(prop_rel_kapp):
            prop_rel_kapp = prop_rels_comp_cm.KappaNoPrevalence
        if match.check_none(loc_rel_kapp):
            loc_rel_kapp = loc_ya_rels_comp_cm.KappaNoPrevalence
        if match.check_none(prop_ya_kapp):
            prop_ya_kapp = prop_ya_comp_cm.KappaNoPrevalence
        if match.check_none(loc_ta_kapp):
            loc_ta_kapp = loc_ta_cm.KappaNoPrevalence
        if match.check_none(prop_ya_an_kapp):
            prop_ya_an_kapp = prop_ya_cm.KappaNoPrevalence


        score_list = [s_node_kapp, prop_rel_kapp, loc_rel_kapp, prop_ya_kapp, loc_ta_kapp, prop_ya_an_kapp]
        k_graph = sum(score_list) / float(len(score_list))

        return k_graph
        # CASS calculation

    @staticmethod
    def text_similarity(data1, data2):
        text1 = data1['text']
        text2 = data2['text']
        # Check if text1 is a dictionary with 'txt' key
        if isinstance(text1, dict) and 'txt' in text1:
            text1 = text1['txt']

        # Check if text2 is a dictionary with 'txt' key
        if isinstance(text2, dict) and 'txt' in text2:
            text2 = text2['txt']
        # Similarity between two texts
        ss = match.get_similarity(text1, text2)
        if ss == 'Error Text Input Is Empty' or ss == 'None:Error! Source Text Was Different as Segmentations differ in length':
            return ss
        else:
         return ss

    @staticmethod
    def CASS_calculation(text_sim_ss,k_graph):
            if text_sim_ss == 'Error Text Input Is Empty' or text_sim_ss == 'None:Error! Source Text Was Different as Segmentations differ in length':
                overall_sim='None'
            else:
                overall_sim = 2((float(k_graph)*float(text_sim_ss))/(float(k_graph)+float(text_sim_ss)))

            return overall_sim

    @staticmethod
    def CASSi_calculation(text_sim_ss,k_graph):
            if text_sim_ss == 'Error Text Input Is Empty' or text_sim_ss == 'None:Error! Source Text Was Different as Segmentations differ in length':
                overall_sim='None'
            else:
                overall_sim = (float(k_graph) + float(text_sim_ss)) / 2
            return overall_sim


    # f1 0-1
    @staticmethod
    def F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm):
        # Get F1 macro scores from confusion matrices for each category/class
        s_node_F1_macro = all_s_a_cm.F1_Macro
        prop_rel_F1_macro = prop_rels_comp_cm.F1_Macro
        loc_rel_F1_macro = loc_ya_rels_comp_cm.F1_Macro
        prop_ya_F1_macro = prop_ya_comp_cm.F1_Macro
        loc_ta_F1_macro = loc_ta_cm.F1_Macro
        prop_ya_an_F1_macro = prop_ya_cm.F1_Macro

        if match.check_none(s_node_F1_macro):
            s_node_F1_macro = 1.0
        if match.check_none(prop_rel_F1_macro):
            prop_rel_F1_macro = 1.0
        if match.check_none(loc_rel_F1_macro):
            loc_rel_F1_macro = 1.0
        if match.check_none(prop_ya_F1_macro):
            prop_ya_F1_macro = 1.0
        if match.check_none(loc_ta_F1_macro):
            loc_ta_F1_macro = 1.0
        if match.check_none(prop_ya_an_F1_macro):
            prop_ya_an_F1_macro = 1.0
        score_list = [s_node_F1_macro, prop_rel_F1_macro, loc_rel_F1_macro, prop_ya_F1_macro, loc_ta_F1_macro, prop_ya_an_F1_macro]

        F1_macro = sum(score_list) / float(len(score_list))

        return F1_macro
    #  accuracy 0-1
    @staticmethod
    def accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                             prop_ya_cm):
        # Get accuracy scores from confusion matrices for each category/class
        s_node_accuracy = all_s_a_cm.ACC
        prop_rel_accuracy = prop_rels_comp_cm.ACC
        loc_rel_accuracy = loc_ya_rels_comp_cm.ACC
        prop_ya_accuracy = prop_ya_comp_cm.ACC
        loc_ta_accuracy = loc_ta_cm.ACC
        prop_ya_an_accuracy = prop_ya_cm.ACC


        # Handle cases where accuracy is None
        def handle_accuracy(acc_dict):
            acc_dict = {k: v if v is not None else 1 for k, v in acc_dict.items()}
            return acc_dict

        s_node_accuracy = handle_accuracy(s_node_accuracy)
        prop_rel_accuracy = handle_accuracy(prop_rel_accuracy)
        loc_rel_accuracy = handle_accuracy(loc_rel_accuracy)
        prop_ya_accuracy = handle_accuracy(prop_ya_accuracy)
        loc_ta_accuracy = handle_accuracy(loc_ta_accuracy)
        prop_ya_an_accuracy = handle_accuracy(prop_ya_an_accuracy)

        # Calculate the average accuracy for each class
        def calculate_average_accuracy(acc_dict):
            values = list(acc_dict.values())
            return sum(values) / len(values) if len(values) > 0 else 0

        s_node_accuracy = calculate_average_accuracy(s_node_accuracy)
        prop_rel_accuracy = calculate_average_accuracy(prop_rel_accuracy)
        loc_rel_accuracy = calculate_average_accuracy(loc_rel_accuracy)
        prop_ya_accuracy = calculate_average_accuracy(prop_ya_accuracy)
        loc_ta_accuracy = calculate_average_accuracy(loc_ta_accuracy)
        prop_ya_an_accuracy = calculate_average_accuracy(prop_ya_an_accuracy)


        score_list = [s_node_accuracy, prop_rel_accuracy, loc_rel_accuracy, prop_ya_accuracy, loc_ta_accuracy,
                      prop_ya_an_accuracy]

        Accuracy = sum(score_list) / float(len(score_list))

        return Accuracy

    # U-Alpha range from 0 to 1
    @staticmethod
    def u_alpha_calculation(all_s_a_cm,prop_rels_comp_cm,loc_ya_rels_comp_cm,prop_ya_comp_cm,loc_ta_cm,prop_ya_cm):
        # u-alpha calculation
        s_node_u_alpha = all_s_a_cm.Alpha
        prop_rel_u_alpha = prop_rels_comp_cm.Alpha
        loc_rel_u_alpha = loc_ya_rels_comp_cm.Alpha
        prop_ya_u_alpha = prop_ya_comp_cm.Alpha
        loc_ta_u_alpha = loc_ta_cm.Alpha
        prop_ya_an_u_alpha = prop_ya_cm.Alpha

        if match.check_none(s_node_u_alpha):
            s_node_u_alpha = 1.0
        if match.check_none(prop_rel_u_alpha):
            prop_rel_u_alpha = 1.0
        if match.check_none(loc_rel_u_alpha):
            loc_rel_u_alpha  = 1.0
        if match.check_none(prop_ya_u_alpha):
            prop_ya_u_alpha = 1.0
        if match.check_none(loc_ta_u_alpha):
            loc_ta_u_alpha = 1.0
        if match.check_none(prop_ya_an_u_alpha):
            prop_ya_an_u_alpha = 1.0


        score_list = [s_node_u_alpha, prop_rel_u_alpha, loc_rel_u_alpha, prop_ya_u_alpha, loc_ta_u_alpha, prop_ya_an_u_alpha]
        u_alpha = sum(score_list) / float(len(score_list))

        return u_alpha


# Debugging

def is_valid_json(my_json):
    try:
        json.loads(my_json)
    except ValueError:
        return False
    return True

if __name__ == "__main__":
        true = True
        null = None
        false = False
        eval=evaluation()
        file1={"AIF": {"nodes": [{"nodeID": 3, "text": "We should go eat", "type": "L"}, {"nodeID": 4, "text": "We should go eat", "type": "I"}, {"nodeID": 5, "text": "Default Illocuting", "type": "YA"}, {"nodeID": 6, "text": "|Wilma: Why", "type": "L"}, {"nodeID": 7, "text": "|Wilma: Why", "type": "I"}, {"nodeID": 8, "text": "Default Illocuting", "type": "YA"}, {"nodeID": 9, "text": "Bob: Because I'm hungry Wilma: Yeah me too", "type": "L"}, {"nodeID": 10, "text": "Bob: Because I'm hungry Wilma: Yeah me too", "type": "I"}, {"nodeID": 11, "text": "Default Illocuting", "type": "YA"}, {"nodeID": 12, "text": "Bob: So let's eat", "type": "L"}, {"nodeID": 13, "text": "Bob: So let's eat", "type": "I"}, {"nodeID": 14, "text": "Default Illocuting", "type": "YA"}, {"text": "Default Inference", "type": "RA", "nodeID": 15}, {"text": "Default Inference", "type": "RA", "nodeID": 16}, {"text": "Default Conflict", "type": "CA", "nodeID": 17}, {"text": "Default Inference", "type": "RA", "nodeID": 18}], "edges": [{"edgeID": 2, "fromID": 3, "toID": 5}, {"edgeID": 3, "fromID": 5, "toID": 4}, {"edgeID": 4, "fromID": 6, "toID": 8}, {"edgeID": 5, "fromID": 8, "toID": 7}, {"edgeID": 6, "fromID": 9, "toID": 11}, {"edgeID": 7, "fromID": 11, "toID": 10}, {"edgeID": 8, "fromID": 12, "toID": 14}, {"edgeID": 9, "fromID": 14, "toID": 13}, {"fromID": 4, "toID": 15, "edgeID": 10}, {"fromID": 15, "toID": 10, "edgeID": 11}, {"fromID": 4, "toID": 16, "edgeID": 12}, {"fromID": 16, "toID": 13, "edgeID": 13}, {"fromID": 7, "toID": 17, "edgeID": 14}, {"fromID": 17, "toID": 13, "edgeID": 15}, {"fromID": 10, "toID": 18, "edgeID": 16}, {"fromID": 18, "toID": 13, "edgeID": 17}], "locutions": [{"nodeID": 3, "personID": 0}, {"nodeID": 6, "personID": 0}, {"nodeID": 9, "personID": 0}, {"nodeID": 12, "personID": 0}], "schemefulfillments": null, "descriptorfulfillments": null, "participants": [{"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}]}, "OVA": [], "dialog": true, "text": {"txt": " Bob None <span class=\"highlighted\" id=\"0\">We should go eat. |Wilma: Why? Bob: Because I'm hungry Wilma: Yeah me too. Bob: So let's eat.</span>.<br><br>"}}
        file2={"AIF": {"nodes": [{"nodeID": 3, "text": "We should go eat", "type": "L"}, {"nodeID": 4, "text": "We should go eat", "type": "I"}, {"nodeID": 5, "text": "Default Illocuting", "type": "YA"}, {"nodeID": 6, "text": "|Wilma: Why", "type": "L"}, {"nodeID": 7, "text": "|Wilma: Why", "type": "I"}, {"nodeID": 8, "text": "Default Illocuting", "type": "YA"}, {"nodeID": 9, "text": "Bob: Because I'm hungry Wilma: Yeah me too", "type": "L"}, {"nodeID": 10, "text": "Bob: Because I'm hungry Wilma: Yeah me too", "type": "I"}, {"nodeID": 11, "text": "Default Illocuting", "type": "YA"}, {"nodeID": 12, "text": "Bob: So let's eat", "type": "L"}, {"nodeID": 13, "text": "Bob: So let's eat", "type": "I"}, {"nodeID": 14, "text": "Default Illocuting", "type": "YA"}, {"text": "Default Inference", "type": "RA", "nodeID": 15}, {"text": "Default Inference", "type": "RA", "nodeID": 16}, {"text": "Default Conflict", "type": "CA", "nodeID": 17}, {"text": "Default Inference", "type": "RA", "nodeID": 18}], "edges": [{"edgeID": 2, "fromID": 3, "toID": 5}, {"edgeID": 3, "fromID": 5, "toID": 4}, {"edgeID": 4, "fromID": 6, "toID": 8}, {"edgeID": 5, "fromID": 8, "toID": 7}, {"edgeID": 6, "fromID": 9, "toID": 11}, {"edgeID": 7, "fromID": 11, "toID": 10}, {"edgeID": 8, "fromID": 12, "toID": 14}, {"edgeID": 9, "fromID": 14, "toID": 13}, {"fromID": 4, "toID": 15, "edgeID": 10}, {"fromID": 15, "toID": 10, "edgeID": 11}, {"fromID": 4, "toID": 16, "edgeID": 12}, {"fromID": 16, "toID": 13, "edgeID": 13}, {"fromID": 7, "toID": 17, "edgeID": 14}, {"fromID": 17, "toID": 13, "edgeID": 15}, {"fromID": 10, "toID": 18, "edgeID": 16}, {"fromID": 18, "toID": 13, "edgeID": 17}], "locutions": [{"nodeID": 3, "personID": 0}, {"nodeID": 6, "personID": 0}, {"nodeID": 9, "personID": 0}, {"nodeID": 12, "personID": 0}], "schemefulfillments": null, "descriptorfulfillments": null, "participants": [{"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}, {"firstname": "Bob", "participantID": 0, "surname": "None"}]}, "OVA": [], "dialog": true, "text": {"txt": " Bob None <span class=\"highlighted\" id=\"0\">We should go eat. |Wilma: Why? Bob: Because I'm hungry Wilma: Yeah me too. Bob: So let's eat.</span>.<br><br>"}}
        # file1='../28037.json'
        # file2='../28038.json'
        if isinstance(file1, (str, bytes, bytearray)) and isinstance(file2, (str, bytes, bytearray)):
            if os.path.isfile(file1) and os.path.isfile(file2):

                file1 = open(file1, 'r')
                file2 = open(file2, 'r')
                data1 = json.load(file1)
                data2 = json.load(file2)

                all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm=eval.matching_calculation(data1,data2)

                kappa=eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
                print('kappa',kappa)

                        # Text Similarity and CASS
                Text_similarity=eval.text_similarity(data1,data2)
                print('text similarity',Text_similarity)

                CASS = eval.CASS_calculation(Text_similarity, kappa)
                print('CASS',CASS)


                        # F1
                F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
                print('F1', F1)
                        # accuracy
                Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                                                  prop_ya_cm)
                print('Accuracy', Acc)

                        # U-Alpha
                U_Alpha= eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm,
                                                   prop_ya_cm)
                print('U-Alpha', U_Alpha)
            else:
                print("invalid files")

        elif is_valid_json(json.dumps(file1)) and is_valid_json(json.dumps(file2)):

            data1 = file1
            data2 = file2

            all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                data1, data2)

            kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                           loc_ta_cm, prop_ya_cm)
            print('kappa', kappa)

            # Text Similarity and CASS
            Text_similarity = eval.text_similarity(data1, data2)
            print('text similarity', Text_similarity)

            CASS = eval.CASS_calculation(Text_similarity, kappa)
            print('CASS', CASS)

            # F1
            F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                           loc_ta_cm, prop_ya_cm)
            print('F1', F1)
            # accuracy
            Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                            loc_ta_cm,
                                            prop_ya_cm)
            print('Accuracy', Acc)

            # U-Alpha
            U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm,
                                               prop_ya_cm)
            print('U-Alpha', U_Alpha)




        else:
            print("invalid files")



