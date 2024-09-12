'''
Loading PTF files

THIS IS LEGACY CODE THAT MAY NOT WORK. For more details, see: https://github.com/manjavacas/melkit/pull/21
'''

from melkit._ptf import Ptf, compare_ptf

PATH_A = 'calcA/MELPTF'
PATH_B = 'calcB/MELPTF'
PATH_C = 'calcC/MELPTF'

# create ptf objects
ptf_a = Ptf(PATH_A)
ptf_b = Ptf(PATH_B)
ptf_c = Ptf(PATH_C)

# list of columns in PTF file
cols = ptf_a.columns

# load subset of columns (first 5) and convert it to pandas DataFrame
ptf_a.to_DataFrame([cols[:5]])

# compare the first 2 varibles between files
# only show plot
compare_ptf([ptf_a, ptf_b, ptf_c],
            ["RN2-DFBBT-10-cls_7", "RN2-DFBBT-10-cls_8"])

# compare, show plot and save them as png
compare_ptf([ptf_a, ptf_b, ptf_c],
            ["RN2-DFBBT-10-cls_7", "RN2-DFBBT-10-cls_8"], save_dir="out")

# plot some variables from one file
ptf_a.plot(["RN2-DFBBT-10-cls_7", "RN2-DFBBT-10-cls_8"],
           output_path="out/RN2_cl78.png")