"""Test the CST2020 scripting library.
    Requires Python 3.6 or newer.
"""

import sys
import cst
import cst.interface as interface
import cst.results as results

def probe_interface():
    """test the cst.interface features.
    Note: PID = 1 for cst run from docker cli
    """
    print("[probe_interface]")
    design_environment = interface.DesignEnvironment(mode=interface.DesignEnvironment.StartMode.ExistingOrNew)
    
    return design_environment

def probe_project(cst_project):
    """query the current project.
    """
    print("[probe_project] Project filename: ", cst_project.filename())
    print("[probe_project] Project modeler: ", cst_project.modeler)
    print("[probe_project] Project type: ", cst_project.project_type())

def probe_results(cst_project_file):
    """query the simulations results of the project.
    cst_project_file: path to cst project file 
    """
    print("[probe_results] attempting to access cst project: ", cst_project_file)
    print("[probe_results] version: ", results.print_version_info())
    project = results.ProjectFile(cst_project_file)
    print(project.filename)
    # 3d result module
    print(project.list_subprojects())
    rm3d = project.get_3d()
    print(type(rm3d))
    print("[probe_results] Run IDs: ")
    run_ids = rm3d.get_all_run_ids()
    print(run_ids)
    print("[probe_results] Run parameters: ")
    
    for run in run_ids:
        run_params = rm3d.get_parameter_combination(run)
        print(run_params)
        print(rm3d.get_tree_items())



if __name__ == "__main__":
    print("CST: ")
    print(dir(cst))
    print("CST Interface: ")
    print(dir(interface))
    a = probe_interface()
    a.print_version()
    print("Is connected?", a.is_connected())
    open_project_files = a.list_open_projects()
    print("PID: ", a.pid())
    print("has_active_project? ", a.has_active_project())
    open_projects = a.get_open_projects()
    print(open_projects)
    if len(open_projects) > 0:
        probe_project(open_projects[0])
    probe_results(r'D:\CST_Projects\RF_Components\Interdigital_Cap.cst')

