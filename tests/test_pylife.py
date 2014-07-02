#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pylife.main

import pytest
from pathlib import Path
from kivy.lang import Builder
from itertools import chain

file_path = Path(__file__).resolve().parents[1] / 'pylife' / 'lifegame.kv'
Builder.load_file(str(file_path))


class TestPyLife:
    @pytest.fixture
    def cell_grid(self, request):
        return pylife.main.CellGrid()

    @pytest.fixture
    def mini_grid(self, request):
        return [[pylife.main.Cell() for i in range(3)] for j in range(3)]

    def test_cellgrid_build(self, cell_grid):
        cell_grid.build()
        assert len(cell_grid.children) == cell_grid.rows * cell_grid.cols

    def test_set_neighborhood(self, mini_grid):
        center = mini_grid[1][1]
        center.set_neighborhood((1, 1), mini_grid)
        result = set(chain(*mini_grid)) - set(center.neighborhood)
        assert result == set((center,))
