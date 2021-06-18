"""
Extract a list of results for a given project.
Note: This is a Windows-only python script.
"""
import os
from cstmod.dllreader import ResultReaderDLL

def get_results(file_name):
    print('in get_results...')
    with ResultReaderDLL(file_name, '2020') as results:
        tree_names = results.item_names('2D/3D Results')
        print(tree_names[0])
        a = results._get_3d_hex_result_info(r'2D/3D Results/H-field', 0)
        print(type(a), a)

if __name__ == "__main__":
    file_name = os.path.join('D:\\', 'workspace', 'cstmod','test_data','Simple_Cosim','Simple_Cosim.cst')
    if os.path.exists(file_name):
        get_results(file_name)
    print('Done.')