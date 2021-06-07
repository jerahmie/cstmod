import os
from win32com.client.gencache import EnsureDispatch


def open_cst():
    """Creates a COM object for CSTStudio.Applicaton
    """
    try:
        cst = EnsureDispatch("CSTStudio.Application")
    except Exception as e:
        print("Unable to open CST Microwave Studio.")

    return cst

def probe_results(cst, project_file):
    """Probe the results of a cst project:
    cst: win32com client CSTStudio.Application
    project_file: cst project file path
    """
    pass


if __name__ == "__main__":
    project_file = os.path.join(r'D:\\', 'CST_Projects', 'RF_Components', 'Interdigital_Cap.cst')
    #print(os.path.exists(project_file))
    cst = open_cst()
    #proj = cst.OpenFile(project_file)
    mws = cst.NewMWS()
    print(mws)