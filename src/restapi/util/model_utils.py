"""
    This file is part of CONTRABASS-webservice project.
    Copyright (C) 2020-2021  Alex Oarga  <718123 at unizar dot es> (University of Zaragoza)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import cobra

from contrabass.core import CobraMetabolicModel

CONST_EPSILON = 0.000005


def read_model(path):
    try:
        # check if file exists
        open(path, "r")

        # Default interface
        cobra.core.model.configuration.solver = 'glpk'

        # read submit
        if path[-4:] == ".xml":
            cobra_model = cobra.io.read_sbml_model(path)
        elif path[-5:] == ".json":
            cobra_model = cobra.io.load_json_model(path)
        elif path[-4:] == ".yml":
            cobra_model = cobra.io.load_yaml_model(path)
        else:
            raise RuntimeError("Model file must be either .xml .json .yml")
    except FileNotFoundError:
        raise FileNotFoundError("File not found: '{}'".format(path))

    return cobra_model

def read_model_url(model_string):
    # Default interface
    cobra.core.model.configuration.solver = 'glpk'

    return cobra.io.read_sbml_model(model_string)


def compute_chokepoints(mdoel_path, exclude_dead_reations=True):
    cpmodel = CobraMetabolicModel(mdoel_path)
    cpmodel.find_chokepoints(exclude_dead_reactions=exclude_dead_reations)
    return [(r.id, m.id) for r, m in cpmodel.chokepoints()]


def in_range_zero(up, low):
    return up + CONST_EPSILON >= 0 and low - CONST_EPSILON <= 0


def alive_flux(cobra_model, cobra_summary):
    result = []
    for r in cobra_model.reactions:
        if abs(cobra_summary[r.id]) > CONST_EPSILON:
            result.append(r.id)
    return result


def alive_reactions(cobra_model, fva_solution):
    result = []
    i = 0
    for reaction_id in fva_solution.index:
        reaction = cobra_model.reactions.get_by_id(reaction_id)
        fva_lower = float(fva_solution.values[i][0])
        fva_upper = float(fva_solution.values[i][1])
        if abs(fva_lower) > CONST_EPSILON or abs(fva_upper) > CONST_EPSILON:
            result.append(reaction.id)
        i = i + 1

    return result


def reaction_reversible(reaction):
    return (
        reaction.upper_bound > CONST_EPSILON
        and abs(reaction.lower_bound) > CONST_EPSILON
    )


def reversible_alive_flux(cobra_model, cobra_summary):
    result = []
    for r in cobra_model.reactions:
        if abs(cobra_summary[r.id]) > CONST_EPSILON:
            if reaction_reversible(r):
                result.append(r.id)
    return result


def reversible_alive_reactions(cobra_model, fva_solution):
    result = []
    i = 0
    for reaction_id in fva_solution.index:
        reaction = cobra_model.reactions.get_by_id(reaction_id)
        fva_lower = float(fva_solution.values[i][0])
        fva_upper = float(fva_solution.values[i][1])
        if abs(fva_lower) > CONST_EPSILON or abs(fva_upper) > CONST_EPSILON:
            if fva_upper > CONST_EPSILON and fva_lower < -CONST_EPSILON:
                result.append(reaction.id)
        i = i + 1

    return result


def fva_fluxes(cobra_model, fva_solution):
    result = {}
    i = 0
    for reaction_id in fva_solution.index:
        reaction = cobra_model.reactions.get_by_id(reaction_id)
        fva_lower = float(fva_solution.values[i][0])
        fva_upper = float(fva_solution.values[i][1])
        result[reaction_id] = (fva_upper, fva_lower)

        i = i + 1

    return result


def ordered_reactions_list(cobra_model):
    reactions_list = sorted([r.id for r in cobra_model.reactions])
    biomass = _get_biomass_reaction(cobra_model)
    if biomass is not None and biomass.id in reactions_list:
        reactions_list.remove(biomass.id)
        # move it to the top
        reactions_list = [biomass.id] + reactions_list
    return reactions_list


def _get_biomass_reaction(cobra_model):
    # NOTE: We dont expect to have more than one objective reaction
    try:
        return list(cobra.util.solver.linear_reaction_coefficients(cobra_model).keys())[0]
    except Exception:
        return None
