import numpy as np
import os
import typing
from struct import unpack

import pandas as pd


def MCRBin(ptf_path: typing.Union[str, os.PathLike], vars_to_search: list):
    """
    # Taken from https://github.com/mattdon/MELCOR_pyPlot
    # Commit 35a2503b49617622dec6ea8138c556697f6dd263
    # modified
    original header
    MELCOR FORMAT SUPPORT MODULE
    Created on March 28, 2017
    Last update on October 14, 2022
    @authors:
             Matteo D'Onorio (University of Rome La Sapienza)
             Paolo Balestra (University of Rome La Sapienza)

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
                # print(VarSrch)
                # print(VarNameFull)
                # for var in VarNameFull:
                #     if "COR-MEJEC" in var:
                #         print(var)

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


class Ptf:
    def __init__(self, path: typing.Union[str, os.PathLike]):
        self.path = path
        # TODO: ugly temporary solution
        #       rewrite MCRBin into different functions
        time_range, _, _, variables, title = MCRBin(path, ["TIME"])
        self._time_range = time_range
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

    @property
    def time_range(self):
        """Get the time range from PTF file data."""
        return self._time_range

    def __str__(self) -> str:
        text = f"PTF file of title {self.title}\n"
        text += f"From {np.min(self.time_range)} s "
        text += f"to {np.max(self.time_range)} s."
        return text

    def to_DataFrame(self, columns: list):
        if not set(columns).issubset(set(self.columns)):
            # TODO: Print which ones
            raise ValueError("One or more desired columns are not contained "
                             "the PTF file")
        time, data, units, _, _ = MCRBin(self.path, columns)
        df = pd.DataFrame(
            index=time,
            columns=columns,
            data=data,
        )
        return df


def compare_ptf(ptf_lst: list[Ptf], variables: list[str]):
    """ Compare data from PTF files by plotting variables """
    df_list = [ptf.to_DataFrame(variables) for ptf in ptf_lst]
    titles = [ptf.title for ptf in ptf_lst]
    for variable in variables:
        var_list = [df[variable] for df in df_list]
        var_df = pd.concat(var_list, axis=1)
        var_df.columns = titles
        var_df.plot(title=variable)
