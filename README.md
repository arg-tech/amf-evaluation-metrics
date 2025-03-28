# Evaluation Metrics
This module computes the following evaluation metrics for two JSON xAIF files: CASS [1], Text Similarity, Kappa, U-Alpha, Macro F1, Accuracy. It is primarily intended for assessing the results of argument mining systems relative to gold standard data, or for calculating inter-annotator agreement between manually annotated files.

The module accepts two xAIF files. Apart from markup for where text spans have been highlighted, which can differ depending on how the original text is segmented, the files must have identical content in their _text_ fields to be comparable.

**Sample usage:**

```
curl -X POST -F "file1=@my_1st_file.json" -F "file2=@my_2nd_file.json" http://amf-evaluation-metrics.amfws.arg.tech
```

The docker container may also be built and run locally, in which case the service is available on port 0.0.0.0:8000:

```
curl -X POST -F "file1=@my_1st_file.json" -F "file2=@my_2nd_file.json" http://0.0.0.0:8000
```


**Sample output:**

```
{"Accuracy":0.5988725079634171,"CASS":0.10259149819921817,"Kappa":0.05453840852022301,"Macro F1":0.6051444934688377,"Text Similarity":0.8627450980392157,"U-Alpha":-0.15569660910965552}
```

----
### References

[1] R. Duthie, J. Lawrence, K. Budzynska, and C. Reed, ‘The CASS Technique for Evaluating the Performance of Argument Mining’, in Proceedings of the Third Workshop on Argument Mining (ArgMining2016), Berlin, Germany: Association for Computational Linguistics, 2016, pp. 40–49. doi: [10.18653/v1/W16-2805](https://doi.org/10.18653/v1/W16-2805).
