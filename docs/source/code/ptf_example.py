'''
Loading PTF files
'''

from melkit.ptf import PTF, compare_ptf

PATH_A = 'calcA/MELPTF'
PATH_B = 'calcB/MELPTF'
PATH_C = 'calcC/MELPTF'

# create ptf objects
ptf_a = PTF(PATH_A)
ptf_b = PTF(PATH_B)
ptf_c = PTF(PATH_C)

# list of columns in PTF file
cols = ptf_a.columns
print(cols)

# load subset of columns (first 5) and convert it to pandas DataFrame
df = ptf_a.to_DataFrame(cols[:5])
df.to_csv("ptf_a_col0to4.csv")


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
