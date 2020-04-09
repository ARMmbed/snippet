#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path

tmp_test_dirname = "tmp_test_dir"
tmp_test_dir = Path(__file__).parent.joinpath(tmp_test_dirname).absolute()
sample_input_dir = Path(__file__).parent.joinpath("samples").absolute()
