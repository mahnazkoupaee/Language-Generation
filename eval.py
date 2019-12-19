import pyrouge

r = pyrouge.Rouge155('pyrouge-master/tools/ROUGE-1.5.5')
r.model_filename_pattern = '#ID#_reference.txt'
r.system_filename_pattern = '(\d+)_decoded.txt'
r.model_dir = 'ref'
r.system_dir = 'dec'
rouge_results = r.convert_and_evaluate()
print(rouge_results)