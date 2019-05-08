#!/usr/bin/env python3
# [LICENSE]
# Copyright (c) 2018, Alliance for Sustainable Energy.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, 
# with or without modification, are permitted provided 
# that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above 
# copyright notice, this list of conditions and the 
# following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the 
# above copyright notice, this list of conditions and the 
# following disclaimer in the documentation and/or other 
# materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the 
# names of its contributors may be used to endorse or 
# promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# [/LICENSE]

import argparse
import logging
import os

import gdxpds
import pandas as pd
import json

logger = logging.getLogger(__name__)


def convert_gdx_to_csv(in_gdx, out_dir, gams_dir=None, wide=False, frmt=None):
    # check inputs
    if not os.path.exists(os.path.dirname(out_dir)):
        raise RuntimeError("Parent directory of output directory '{}' does not exist.".format(out_dir))
        
    # convert to pandas.DataFrames
    dataframes = gdxpds.to_dataframes(in_gdx, gams_dir)

    # write to files
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for symbol_name, df in dataframes.items():
        csv_path = os.path.join(out_dir, symbol_name + ".csv")
        if os.path.exists(csv_path):
            logger.info("Overwriting '{}'".format(csv_path))
        if wide:
            idx=list(df.columns[:-1])
            logger.info('Setting index {}'.format(idx))
            df=df.set_index(idx).unstack()
            if isinstance(df,pd.DataFrame) and df.columns.nlevels>1:
                df.columns=df.columns.droplevel(0)
            while df.index.nlevels>1:
                df.index = df.index.droplevel(0)

        if frmt and symbol_name in frmt:
            logger.info("Format symbol {}".format(symbol_name))
            frmt_symbol=frmt[symbol_name]
            if 'columns' in frmt_symbol:
                columns=frmt_symbol['columns']
                for c in columns:
                    if c not in df:
                        df[c]=0
                df=df[columns]
            if 'index_name' in frmt_symbol:
                df.index.name=frmt_symbol['index_name']
            if 'sort' in frmt_symbol:
                df=df.sort_values(by=frmt_symbol['sort'])
        df.to_csv(csv_path)

if __name__ == "__main__":

    # define and execute the command line interface
    parser = argparse.ArgumentParser(description='''Reads a gdx file into
        pandas dataframes, and then writes them out as csv files.''')
    parser.add_argument('-i', '--in_gdx', help='''Input gdx file to be read
                        and exported as one csv per symbol.''')
    parser.add_argument('-o', '--out_dir', default='./gdx_data/',
                        help='''Directory to which csvs are to be written.''')
    parser.add_argument('-g', '--gams_dir', help='''Path to GAMS installation
                        directory.''', default = None)
    parser.add_argument('-w', '--wide', help='''Transform to wide format''', action='store_true', default = False)
    parser.add_argument('-f', '--format', help='''Format dataset definitions''', default = "/var/task/format.json")
        
    args = parser.parse_args()
    
    if not args.gams_dir and 'GAMSPATH' in os.environ:
        args.gams_dir=os.environ['GAMSPATH']

    if args.format:
        with open(args.format,'r') as infile:
            frmt_data=json.load(infile)
    else:
        frmt_data={}

    convert_gdx_to_csv(args.in_gdx, os.path.realpath(args.out_dir), args.gams_dir, wide=args.wide,frmt=frmt_data)
