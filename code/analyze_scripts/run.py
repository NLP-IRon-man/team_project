from analyze_scripts.character_emotional_change_analyzer import CharacterEmotionalChangeAnalyzer
from analyze_scripts.graph_plotter import GraphPlotter
from analyze_scripts.main_character_finder import MainCharacterFinder
from analyze_scripts.script_preprocessor import ScriptPreprocessor

MainCharacterFinder("data/scripts/",
                    "data/csv_main_character_figured_out/").run()
ScriptPreprocessor("data/csv_main_character_figured_out/",
                   "data/csv_preprocessed/").run()
CharacterEmotionalChangeAnalyzer("data/emotion_dataset.csv",
                                 "data/csv_preprocessed/",
                                 "data/csv_emotion_analyzed/", 5).run()
graph_plotter = GraphPlotter("data/csv_emotion_analyzed/",
                             "data/graph_emotion_change/",
                             "../backend/static/graph_emotion_change/")
graph_plotter.run()
graph_plotter.copy_graph_folder_to_static_folder()
