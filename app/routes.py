from flask import request, render_template, jsonify
from . import application
import json
from app.evaluation_metrics import evaluation
import os


def is_valid_json(my_json):
    try:
        json.loads(my_json)
    except ValueError:
        return False
    return True


@application.route('/file', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':

        f1 = request.files['file1']
        f2 = request.files['file2']

        true = True
        null = None
        false = False

        eval = evaluation()

        if isinstance(f1, (str, bytes, bytearray)) and isinstance(f2, (str, bytes, bytearray)):
            if os.path.isfile(f1) and os.path.isfile(f2):

                f1.save(f1.filename)
                ff1 = open(f1.filename, 'r')


                f2.save(f2.filename)
                ff2 = open(f2.filename, 'r')

                data1 = json.load(ff1)
                data2 = json.load(ff2)

                all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                    data1, data2)

                kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm, prop_ya_cm)


                # Text Similarity and CASS
                Text_similarity = eval.text_similarity(data1, data2)


                CASS = eval.CASS_calculation(Text_similarity, kappa)


                # F1
                F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm, prop_ya_cm)
                print('F1', F1)
                # accuracy
                Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                loc_ta_cm,
                                                prop_ya_cm)


                # U-Alpha
                U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                   loc_ta_cm,
                                                   prop_ya_cm)


                results = {
                    "Macro F1": F1,
                    "Accuracy": Acc,
                    "CASS": CASS,
                    "Text Similarity": Text_similarity,
                    "U-Alpha": U_Alpha,
                    "Kappa": kappa
                }

                return jsonify(results)

            else:
                return None

        elif is_valid_json(json.dumps(f1)) and is_valid_json(json.dumps(f2)):

            data1 = f1
            data2 = f2

            all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                data1, data2)

            kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                           loc_ta_cm, prop_ya_cm)


            # Text Similarity and CASS
            Text_similarity = eval.text_similarity(data1, data2)


            CASS = eval.CASS_calculation(Text_similarity, kappa)


            # F1
            F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                           loc_ta_cm, prop_ya_cm)

            # accuracy
            Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                            loc_ta_cm,
                                            prop_ya_cm)


            # U-Alpha
            U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm,
                                               prop_ya_cm)

            results = {
                "Macro F1": F1,
                "Accuracy": Acc,
                "CASS": CASS,
                "Text Similarity": Text_similarity,
                "U-Alpha": U_Alpha,
                "Kappa": kappa
            }

            return jsonify(results)



        else:
            return None






    elif request.method == 'GET':

        return render_template('docs.html')

    @application.route('/file', methods=['GET', 'POST'])
    def get_data():
        if request.method == 'POST':

            f1 = request.files['file1']
            f2 = request.files['file2']

            true = True
            null = None
            false = False

            eval = evaluation()

            if isinstance(f1, (str, bytes, bytearray)) and isinstance(f2, (str, bytes, bytearray)):
                if os.path.isfile(f1) and os.path.isfile(f2):

                    f1.save(f1.filename)
                    ff1 = open(f1.filename, 'r')

                    f2.save(f2.filename)
                    ff2 = open(f2.filename, 'r')

                    data1 = json.load(ff1)
                    data2 = json.load(ff2)

                    all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                        data1, data2)

                    kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                   loc_ta_cm, prop_ya_cm)

                    # Text Similarity and CASS
                    Text_similarity = eval.text_similarity(data1, data2)

                    CASS = eval.CASS_calculation(Text_similarity, kappa)

                    # F1
                    F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                   loc_ta_cm, prop_ya_cm)
                    print('F1', F1)
                    # accuracy
                    Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                    loc_ta_cm,
                                                    prop_ya_cm)

                    # U-Alpha
                    U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm,
                                                       prop_ya_comp_cm,
                                                       loc_ta_cm,
                                                       prop_ya_cm)

                    results = {
                        "Macro F1": F1,
                        "Accuracy": Acc,
                        "CASS": CASS,
                        "Text Similarity": Text_similarity,
                        "U-Alpha": U_Alpha,
                        "Kappa": kappa
                    }

                    return jsonify(results)

                else:
                    return None

            elif is_valid_json(json.dumps(f1)) and is_valid_json(json.dumps(f2)):

                data1 = f1
                data2 = f2

                all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                    data1, data2)

                kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm, prop_ya_cm)

                # Text Similarity and CASS
                Text_similarity = eval.text_similarity(data1, data2)

                CASS = eval.CASS_calculation(Text_similarity, kappa)

                # F1
                F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm, prop_ya_cm)

                # accuracy
                Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                loc_ta_cm,
                                                prop_ya_cm)

                # U-Alpha
                U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                   loc_ta_cm,
                                                   prop_ya_cm)

                results = {
                    "Macro F1": F1,
                    "Accuracy": Acc,
                    "CASS": CASS,
                    "Text Similarity": Text_similarity,
                    "U-Alpha": U_Alpha,
                    "Kappa": kappa
                }

                return jsonify(results)



            else:
                return None






        elif request.method == 'GET':

            return render_template('docs.html')

@application.route('/json', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':

        f1 = request.files['file1']
        f2 = request.files['file2']

        request.args.get('')

        true = True
        null = None
        false = False

        eval = evaluation()

        if isinstance(f1, (str, bytes, bytearray)) and isinstance(f2, (str, bytes, bytearray)):
            if os.path.isfile(f1) and os.path.isfile(f2):

                f1.save(f1.filename)
                ff1 = open(f1.filename, 'r')


                f2.save(f2.filename)
                ff2 = open(f2.filename, 'r')

                data1 = json.load(ff1)
                data2 = json.load(ff2)

                all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                    data1, data2)

                kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm, prop_ya_cm)


                # Text Similarity and CASS
                Text_similarity = eval.text_similarity(data1, data2)


                CASS = eval.CASS_calculation(Text_similarity, kappa)


                # F1
                F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm, prop_ya_cm)
                print('F1', F1)
                # accuracy
                Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                loc_ta_cm,
                                                prop_ya_cm)


                # U-Alpha
                U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                                   loc_ta_cm,
                                                   prop_ya_cm)


                results = {
                    "Macro F1": F1,
                    "Accuracy": Acc,
                    "CASS": CASS,
                    "Text Similarity": Text_similarity,
                    "U-Alpha": U_Alpha,
                    "Kappa": kappa
                }

                return jsonify(results)

            else:
                return None

        elif is_valid_json(json.dumps(f1)) and is_valid_json(json.dumps(f2)):

            data1 = f1
            data2 = f2

            all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                data1, data2)

            kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                           loc_ta_cm, prop_ya_cm)


            # Text Similarity and CASS
            Text_similarity = eval.text_similarity(data1, data2)


            CASS = eval.CASS_calculation(Text_similarity, kappa)


            # F1
            F1 = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                           loc_ta_cm, prop_ya_cm)

            # accuracy
            Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                            loc_ta_cm,
                                            prop_ya_cm)


            # U-Alpha
            U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm,
                                               loc_ta_cm,
                                               prop_ya_cm)

            results = {
                "Macro F1": F1,
                "Accuracy": Acc,
                "CASS": CASS,
                "Text Similarity": Text_similarity,
                "U-Alpha": U_Alpha,
                "Kappa": kappa
            }

            return jsonify(results)



        else:
            return None






    elif request.method == 'GET':

        return render_template('docs.html')
