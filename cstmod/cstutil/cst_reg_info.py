"""
Interact with Windows registry to obtain info about local CST Installation
"""

import os.path
import winreg

class CSTRegInfo(object):
    """
    Collection of methods to provide information about local CST installation.
    """
    cst_de_reg_str = "SOFTWARE\WOW6432Node\CST AG\CST DESIGN ENVIRONMENT\\"
    @staticmethod
    def find_cst_reg_version():
        """Returns the CST verion(s) installed on the host system.
        """
        wr_handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        try:
            rkey = winreg.OpenKey(wr_handle, CSTRegInfo.cst_de_reg_str)
        except FileNotFoundError: 
            print("\n[ERROR] Could not find CST installed on this system.\n")
        except:
            print("\n[ERROR] An unanticipated error has occurred.")
            raise

        return [winreg.EnumKey(rkey, i) for i in range(winreg.QueryInfoKey(rkey)[0])]

    @staticmethod
    def find_result_reader_dll(cst_version):
        """Returns the path of ResultReaderDLL for the given cst version.
        """
        wr_handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        try:
            rkey = winreg.OpenKey(wr_handle, CSTRegInfo.cst_de_reg_str+str(cst_version))
        except FileNotFoundError:
            print("\n[ERROR] Could not find CST Design Environment " 
                + str(cst_version) + ". Installed on this system.\n")
        except:
            print("\n[ERROR] An unanticipated error has occurred.\n")
            raise

        cst_result_reader_path = winreg.QueryValueEx(rkey, "INSTALLPATH")[0]+"CSTResultReader.dll"
        if os.path.exists(cst_result_reader_path):
            return cst_result_reader_path
        else:
            raise FileNotFoundError

if __name__ == "__main__":
    cst_versions = CSTRegInfo.find_cst_reg_version()  
    print("CST VERSIONS: ", cst_versions )
    for cst_version in cst_versions:
        cst_result_reader_path = CSTRegInfo.find_result_reader_dll(cst_version)
        print("CSTResultReader: ", cst_result_reader_path)
