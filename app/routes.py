from flask import Flask, request, jsonify, render_template_string
import json
import os
import logging
import markdown2
from app.evaluation_metrics import evaluation

app = Flask(__name__)

# Configure logging

logging.basicConfig(level=logging.INFO)

def is_valid_json(my_json):
    try:
        json.loads(my_json)
    except ValueError as e:
        logging.error(f"Invalid JSON format: {e}")
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def get_data_file():
    if request.method == 'POST':
        logging.debug("Received POST request")

        if request.files:
            f1 = request.files['file1']
            f2 = request.files['file2']

            eval = evaluation()

            f1.save(f1.filename)
            logging.debug(f"Saved file 1 as: {f1.filename}")
            with open(f1.filename, 'r') as ff1:
                loaded1 = json.load(ff1)
            data1 = {}
            data1['AIF'] = loaded1['AIF']
            data1['text'] = loaded1['text']
            data1['OVA'] = loaded1['OVA']
            

            f2.save(f2.filename)
            logging.debug(f"Saved file 2 as: {f2.filename}")
            with open(f2.filename, 'r') as ff2:
                data2 = json.load(ff2)

            os.remove(f1.filename)
            os.remove(f2.filename)

            all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                data1, data2)
            kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
            Text_similarity = eval.text_similarity(data1, data2)
            cass = eval.CASS_calculation(Text_similarity, kappa)
            cassi = eval.CASSi_calculation(Text_similarity, kappa)
            f1_score = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
            Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
            U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)

            results = {
                "Macro F1": f1_score,
                "Accuracy": Acc,
                "CASS": cass,
                # "CASSi": cassi,
                "Text Similarity": Text_similarity,
                "U-Alpha": U_Alpha,
                "Kappa": kappa
            }

            return jsonify(results)

        if request.values:

            data1 = request.values.get('json1')
            data2 = request.values.get('json2')

            # print("Received data1:", data1)
            # print("Received data2:", data2)

            if is_valid_json(json.dumps(data1)) and is_valid_json(json.dumps(data2)):

                # print("Both data1 and data2 are valid JSON")

                data1 = json.loads(data1)

                data2 = json.loads(data2)

                # print("Parsed data1:", data1)
                # print("Parsed data2:", data2)


                eval = evaluation()

                all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm = eval.matching_calculation(
                    data1, data2)
                kappa = eval.kappa_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
                Text_similarity = eval.text_similarity(data1, data2)
                cass = eval.CASS_calculation(Text_similarity, kappa)
                cassi = eval.CASSi_calculation(Text_similarity, kappa)
                f1_score = eval.F1_Macro_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
                Acc = eval.accuracy_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)
                U_Alpha = eval.u_alpha_calculation(all_s_a_cm, prop_rels_comp_cm, loc_ya_rels_comp_cm, prop_ya_comp_cm, loc_ta_cm, prop_ya_cm)

                results = {
                    "Macro F1": f1_score,
                    "Accuracy": Acc,
                    "CASS": cass,
                    # "CASSi": cassi,
                    "Text Similarity": Text_similarity,
                    "U-Alpha": U_Alpha,
                    "Kappa": kappa
                }

                return jsonify(results)
            else:
                # logging.error("Invalid JSON data provided")
                return jsonify({"error": "Invalid JSON data"}), 400
        else:
            # logging.error("No files or JSON data provided")
            return jsonify({"error": "No files or JSON data provided"}), 400

    elif request.method == 'GET':
        # Read the markdown file
        with open('/home/AMF_Evaluation_Metrics/README.md', 'r') as file:
            md_content = file.read()
            print(md_content)

        # Convert to HTML
        html_content = markdown2.markdown(md_content)#, extensions=['fenced_code'])

        # Render the HTML content as a template
        html_content = f"<html><head></head><body>{html_content}</body></html>"
        return render_template_string(html_content)


if __name__ == '__main__':
    app.run(debug=True)
