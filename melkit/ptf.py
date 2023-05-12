'''
Module for handling PTF files
'''


import numpy as np
import os
import typing
from struct import unpack
from pathlib import Path

import pandas as pd


def MCRBin(ptf_path: typing.Union[str, os.PathLike], vars_to_search: list):
    """
    Read column names and values from MELCOR PTF file
    Taken from https://github.com/mattdon/MELCOR_pyPlot, commit 35a2503,
    modified

    This method is called to collect the variables to be used
    in the postprocess

    @ In, fileDirectory, string, the file directory. This is the directory
    of the MELCOR plot file
    @ In, variableSearch, list, list of variables to be collected
    @ Out, Data, tuple (numpy.ndarray,numpy.ndarray,numpy.ndarray),
    this contains the extracted data for each declare variable
    """
    HdrList = []
    BlkLenBef = []
    BlkLenAft = []
    DataPos = []
    cntr = 0
    Var_dict = {}
    with open(ptf_path, 'rb') as ptf:
        while True:
            BlkLenBefSlave = ptf.read(4)
            if not BlkLenBefSlave:
                break
            BlkLenBef.append(unpack('I', BlkLenBefSlave)[0])
            if BlkLenBef[cntr] == 4:
                HdrList.append(str(unpack('4s', ptf.read(4))[0], 'utf-8'))
            elif HdrList[cntr - 1] == 'TITL':
                probemTitle = str(
                    unpack('%d' % BlkLenBef[cntr] + 's',
                           ptf.read(BlkLenBef[cntr]))[0], 'utf-8')
                HdrList.append([])
            elif HdrList[cntr - 1] == 'KEY ':
                VarName = unpack('2I', ptf.read(8))
                HdrList.append([])
            elif HdrList[cntr - 2] == 'KEY ':
                a = BlkLenBef[-1]/VarName[0]
                stringa = str(int(a))+"s"
                VarNam = [str(i, 'utf-8') for i in unpack(
                    stringa * VarName[0], ptf.read(BlkLenBef[cntr]))]
                HdrList.append([])
            elif HdrList[cntr - 3] == 'KEY ':
                VarPos = unpack(
                    '%d' % VarName[0] + 'I', ptf.read(BlkLenBef[cntr]))
                HdrList.append([])
            elif HdrList[cntr - 4] == 'KEY ':
                VarUdm = [str(i, 'utf-8') for i in unpack(
                    '16s' * VarName[0], ptf.read(BlkLenBef[cntr]))]
                HdrList.append([])
            elif HdrList[cntr - 5] == 'KEY ':
                VarNum = unpack(
                    '%d' % VarName[1] + 'I', ptf.read(BlkLenBef[cntr]))
                available_vars = []
                VarUdmFull = []
                NamCntr = 0
                VarPos = VarPos + (VarName[1]+1,)
                VarSrchPos = [0]
                itm_x_Var = []
                for k in range(0, len(VarNam)):
                    itm_x_Var.append(VarPos[k+1]-VarPos[k])
                if len(itm_x_Var) != len(VarNam):
                    print("Number of variables different from number "
                          "of items of offset array")
                    print(itm_x_Var)
                    print(len(VarNam))
                    break
                Items_Tot = sum(itm_x_Var)
                if Items_Tot != len(VarNum):
                    print("Sum of items to be associated with each variable "
                          "is different from the sum of all items id VarNum")
                VarNum_Cntr = 0
                Var_dict = {}
                for i, Var in enumerate(VarNam):
                    NumOfItems = itm_x_Var[i]
                    end = VarNum_Cntr + NumOfItems
                    Var_dict[Var] = list(VarNum[VarNum_Cntr:end])
                    VarNum_Cntr = VarNum_Cntr+NumOfItems
                for key in Var_dict.keys():
                    for element in Var_dict[key]:
                        if element == 0:
                            available_vars.append(str(key).strip())
                        else:
                            available_vars.append(key.strip()+'_%d' % element)
                for i, item in enumerate(itm_x_Var):
                    for k in range(0, item):
                        VarUdmFull.append(VarUdm[i].strip())
                available_vars = ['TIME', 'CPU',
                                  'DT', 'UNKN03'] + available_vars
                VarUdmFull = ['sec', '', '', ''] + VarUdmFull

                for var in vars_to_search:
                    VarSrchPos.append(available_vars.index(var.strip()))
                VarUdmFull = [VarUdmFull[i] for i in VarSrchPos]
                SwapPosVarSrch = sorted(range(len(VarSrchPos)),
                                        key=lambda k: VarSrchPos[k])
                SwapPosVarSrch = sorted(range(len(SwapPosVarSrch)),
                                        key=lambda k: SwapPosVarSrch[k])
                VarSrchPos.sort()
                VarSrchPos.append(VarName[1]+4)
                HdrList.append([])
            elif HdrList[cntr - 1] == '.TR/':
                DataPos.append(ptf.tell())
                ptf.seek(BlkLenBef[cntr], 1)
                HdrList.append([])
            else:
                HdrList.append([])
            BlkLenAft.append(unpack('I', ptf.read(4))[0])

            cntr += 1

    data = np.empty([len(DataPos), len(vars_to_search)+1])*np.nan
    with open(ptf_path, 'rb') as ptf:
        for i, Pos in enumerate(DataPos):
            ptf.seek(Pos, 0)
            for j in range(len(VarSrchPos)-1):
                data[i, j] = unpack('f', ptf.read(4))[0]
                ptf.seek((VarSrchPos[j+1]-VarSrchPos[j])*4-4, 1)
    data = data[:, SwapPosVarSrch]
    return data[:, 0], data[:, 1:], VarUdmFull[1:], available_vars, probemTitle


def inspect_ptf(ptf_path: typing.Union[str, os.PathLike]):
    HdrList = []
    BlkLenBef = []
    BlkLenAft = []
    DataPos = []
    cntr = 0
    Var_dict = {}
    with open(ptf_path, 'rb') as ptf:
        while True:
            BlkLenBefSlave = ptf.read(4)
            if not BlkLenBefSlave:
                break
            BlkLenBef.append(unpack('I', BlkLenBefSlave)[0])
            if BlkLenBef[cntr] == 4:
                HdrList.append(str(unpack('4s', ptf.read(4))[0], 'utf-8'))
            elif HdrList[cntr - 1] == 'TITL':
                probemTitle = str(
                    unpack('%d' % BlkLenBef[cntr] + 's',
                           ptf.read(BlkLenBef[cntr]))[0], 'utf-8')
                HdrList.append([])
            elif HdrList[cntr - 1] == 'KEY ':
                VarName = unpack('2I', ptf.read(8))
                HdrList.append([])
            elif HdrList[cntr - 2] == 'KEY ':
                a = BlkLenBef[-1]/VarName[0]
                stringa = str(int(a))+"s"
                VarNam = [str(i, 'utf-8') for i in unpack(
                    stringa * VarName[0], ptf.read(BlkLenBef[cntr]))]
                HdrList.append([])
            elif HdrList[cntr - 3] == 'KEY ':
                VarPos = unpack(
                    '%d' % VarName[0] + 'I', ptf.read(BlkLenBef[cntr]))
                HdrList.append([])
            elif HdrList[cntr - 4] == 'KEY ':
                VarUdm = [str(i, 'utf-8') for i in unpack(
                    '16s' * VarName[0], ptf.read(BlkLenBef[cntr]))]
                HdrList.append([])
            elif HdrList[cntr - 5] == 'KEY ':
                VarNum = unpack(
                    '%d' % VarName[1] + 'I', ptf.read(BlkLenBef[cntr]))
                available_vars = []
                VarUdmFull = []
                NamCntr = 0
                VarPos = VarPos + (VarName[1]+1,)
                VarSrchPos = [0]
                itm_x_Var = []
                for k in range(0, len(VarNam)):
                    itm_x_Var.append(VarPos[k+1]-VarPos[k])
                if len(itm_x_Var) != len(VarNam):
                    print("Number of variables different from number "
                          "of items of offset array")
                    print(itm_x_Var)
                    print(len(VarNam))
                    break
                Items_Tot = sum(itm_x_Var)
                if Items_Tot != len(VarNum):
                    print("Sum of items to be associated with each variable "
                          "is different from the sum of all items id VarNum")
                VarNum_Cntr = 0
                Var_dict = {}
                for i, Var in enumerate(VarNam):
                    NumOfItems = itm_x_Var[i]
                    end = VarNum_Cntr + NumOfItems
                    Var_dict[Var] = list(VarNum[VarNum_Cntr:end])
                    VarNum_Cntr = VarNum_Cntr+NumOfItems
                for key in Var_dict.keys():
                    for element in Var_dict[key]:
                        if element == 0:
                            available_vars.append(str(key).strip())
                        else:
                            available_vars.append(key.strip()+'_%d' % element)
                for i, item in enumerate(itm_x_Var):
                    for k in range(0, item):
                        VarUdmFull.append(VarUdm[i].strip())
                available_vars = ['TIME', 'CPU',
                                  'DT', 'UNKN03'] + available_vars
                VarUdmFull = ['sec', '', '', ''] + VarUdmFull

                # TODO: this seems quite useless, i.e. VarSrchPos is just
                # list(range(len(available_vars)))
                for var in available_vars:
                    VarSrchPos.append(available_vars.index(var.strip()))
                VarUdmFull = [VarUdmFull[i] for i in VarSrchPos]
                SwapPosVarSrch = sorted(range(len(VarSrchPos)),
                                        key=lambda k: VarSrchPos[k])
                SwapPosVarSrch = sorted(range(len(SwapPosVarSrch)),
                                        key=lambda k: SwapPosVarSrch[k])
                VarSrchPos.sort()
                VarSrchPos.append(VarName[1]+4)
                HdrList.append([])
            elif HdrList[cntr - 1] == '.TR/':
                DataPos.append(ptf.tell())
                ptf.seek(BlkLenBef[cntr], 1)
                HdrList.append([])
            else:
                HdrList.append([])
            BlkLenAft.append(unpack('I', ptf.read(4))[0])

            cntr += 1
    return available_vars, probemTitle


class Ptf:
    """ Class to extract, plot and compare data in PTF files """
    def __init__(self, path: typing.Union[str, os.PathLike]):
        self.path = path
        variables, title = inspect_ptf(path)
        self._title = title.strip()
        self._columns = variables

    @property
    def title(self):
        """Get the PTF file title."""
        return self._title

    @property
    def columns(self):
        """Get the list of variables in PTF file."""
        return self._columns

    def __str__(self) -> str:
        return f"PTF file of title {self.title}"

    def to_DataFrame(self, columns: list):
        desired_cols = set(columns)
        available_cols = set(self.columns)
        if not desired_cols.issubset(available_cols):
            raise KeyError(f"Desired columns {desired_cols - available_cols} "
                           f"are not available in PTF {self.title}")
        time, data, units, _, _ = MCRBin(self.path, columns)
        df = pd.DataFrame(
            index=time,
            columns=columns,
            data=data,
        )
        return df
    
    def plot(self, variables, output_path=None, **kwargs):
        """ Plot variables of PTF file against time. Optionally save plot fig
        """
        df = self.to_DataFrame(variables)
        ax = df.plot(**kwargs)
        fig = ax.get_figure()
        fig.show()
        if output_path:
            out_dir = os.path.dirname(output_path)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            fig.savefig(output_path)


def compare_ptf(ptf_lst: list[Ptf], variables: list[str], save_dir=None,
                plot=True, ret_df=True, **kwargs):
    """ Compare data from PTF files by plotting variables """
    df_list = [ptf.to_DataFrame(variables) for ptf in ptf_lst]
    titles = [ptf.title for ptf in ptf_lst]
    for variable in variables:
        var_list = [df[variable] for df in df_list]
        var_df = pd.concat(var_list, axis=1)
        var_df.columns = titles
        ax = var_df.plot(title=variable, **kwargs)
        fig = ax.get_figure()
        if plot:
            fig.show()
        if save_dir:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            fig.savefig(Path(save_dir, f"{variable}.png"))
    if ret_df:
        return pd.concat(df_list)
