#!/usr/bin/env python

import os

if __name__ == "__main__":
    cst_project_dir = os.path.join(r'/export', r'data2', r'jerahmie-data', r'PTx_Knee_7T',
            r'Knee_pTx_7T_DB_Siemens_Duke_One_Legs_Fields_retune_20230124_9')
    assert os.path.exists(cst_project_dir), "Could not find: " + cst_project_dir
