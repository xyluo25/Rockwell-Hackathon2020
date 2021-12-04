import sys
import os.path
sys.path.append('I:/FB_Coding/BDT')
import matplotlib
matplotlib.use('SVG')
import sweetviz.series_analyzer as sa
#from sweetviz.config import config
import pickle
import time

#temp_folder = config["Files"].get("temp_folder")

# full_path_to_pickled = "../sweetviz-temp/5e52a452__click_id.pkl"
full_path_to_pickled = sys.argv[1]
with open(full_path_to_pickled, 'rb') as handle:
    feature_to_process = pickle.load(handle)
# start = time.perf_counter()

# print("OHHHHH:" + str(feature_to_process))
#print("OHHHHH:")
analysis_dictionary = sa.analyze_feature_to_dictionary(feature_to_process)
#analysis_dictionary = dict()
#print(analysis_dictionary)


split_source_path = os.path.split(full_path_to_pickled)
full_path_to_pickled_out = os.path.join(split_source_path[0],
                                        os.path.splitext(
                                            split_source_path[1])[0]
                                        + "_out.pkl")

with open(full_path_to_pickled_out, 'wb') as handle:
   pickle.dump(analysis_dictionary, handle)
# print(f"PROCESS------> {feature_to_process.source.name}"
#       f" {time.perf_counter() - start}")
