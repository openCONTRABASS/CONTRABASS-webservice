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

from math import isnan
import cobra
from cobra.flux_analysis import *
import logging
from flask import current_app

from contrabass.core import *
from src.restapi.util.model_utils import *
from src.restapi.beans.OptimizationEnum import *
from src.restapi.beans.MediumEnum import *
from src.restapi.socket_util import send_message_client

PROCESSES = 1
INFEASIBLE = "infeasible"

DEFAULT_COBRA_LOWER_BOUND = float(-1000)
DEFAULT_COBRA_UPPER_BOUND = float(1000)

LOGGER = logging.getLogger(__name__)


def read_config_model(model_path, config):
    model = CobraMetabolicModel(model_path)
    model.processes = PROCESSES

    if config.objective is not None:
        model.set_objective(config.objective)

    if config.medium == MediumEnum.COMPLETE:
        for r in model.reactions():
            if len(r.reactants) == 0 or len(r.products) == 0:
                r.upper_bound = DEFAULT_COBRA_UPPER_BOUND
                r.lower_bound = DEFAULT_COBRA_LOWER_BOUND

    return model


def generate_sets_report(model_path, output_path, model_uuid, config):
    def verbose_f(text, args1=None, args2=None):
        """
        args1 = room name
        args2 = None
        """
        LOGGER.info(text)
        send_message_client(args1, text)

    # process config info
    fraction_of_optimum = 1.0
    if config.fraction_of_optimum is not None:
        fraction_of_optimum = config.fraction_of_optimum

    MODEL = model_path

    # compute essential reactions
    verbose_f("Computing essential reactions", model_uuid)
    model = read_config_model(MODEL, config)
    model.find_essential_reactions_1()
    ER = set([])
    for r, g in model.essential_reactions().items():
        if isnan(g) or g < CONST_EPSILON:
            ER.add(r.id)

    if config.optimization == OptimizationEnum.FBA:
        verbose_f("Computing Flux Balance Analysis", model_uuid)
        MAX_GROWTH = model.model().slim_optimize()
    elif config.optimization == OptimizationEnum.pFBA:
        verbose_f("Computing pFBA", model_uuid)
        MAX_GROWTH = cobra.flux_analysis.pfba(model.model()).objective_value
    else:
        raise RuntimeError("Unexpected optimization parameter")
    MGER = set([])
    for r, g in model.essential_reactions().items():
        if isnan(g) or g < CONST_EPSILON or g + CONST_EPSILON < MAX_GROWTH:
            MGER.add(r.id)
    print("MAX GROWTH essential reactions: ", len(MGER))

    ####################################################################################################################

    cpmodel = read_config_model(MODEL, config)
    cpmodel.print_model_info()

    state = State()
    state.set_id(cpmodel.id())
    state.set_objective(cpmodel.objective())
    state.set_reactions(list(cpmodel.model().reactions))
    state.set_metabolites(list(cpmodel.model().metabolites))
    state.set_genes(list(cpmodel.model().genes))

    s = Spreadsheet()
    s.spreadsheet_init()
    book = s.get_workbook()
    info = book.add_sheet("submit info")
    s.spreadsheet_write_reactions(state, "reactions", ordered=True)
    s.spreadsheet_write_metabolites(
        state, "metabolites", ordered=True, print_reactions=True
    )

    chokepoints = set(
        [r.reaction.id for r in cpmodel.find_chokepoints(exclude_dead_reactions=True)]
    )
    model = cpmodel.model()

    # FBA
    if config.optimization == OptimizationEnum.FBA:
        verbose_f("Computing Flux Balance Analysis", model_uuid)
        sol_fba = model.optimize()
    elif config.optimization == OptimizationEnum.pFBA:
        verbose_f("Computing pFBA", model_uuid)
        sol_fba = cobra.flux_analysis.pfba(model)
    MAX_GROWTH = sol_fba.objective_value

    sheetcr = book.add_sheet("CR (subop)")
    sheetcrer = book.add_sheet("CR (ER)")
    sheetor = book.add_sheet("OR")
    sheetorer = book.add_sheet("OR (ER)")
    sheetorsubop = book.add_sheet("OR (subop)")

    counters = {}

    for sheet in [sheetcr, sheetcrer, sheetor, sheetorer, sheetorsubop]:
        sheet.write(0, 0, "reaction id")
        sheet.write(0, 1, "CP = chokepoint")
        sheet.write(0, 2, "CP_0 = chokepoint FVA gamma = 0")
        sheet.write(0, 3, "CP_1 = chokepoint FVA gamma = 1")
        sheet.write(0, 4, "ER = essential reaction")
        sheet.write(0, 5, "r in MGER = essential reactions for maximum growth")
        sheet.write(0, 6, "r in MGR")
        sheet.write(0, 7, "growth")
        sheet.write(0, 8, "sum fluxes")
        sheet.write(0, 9, "reactions changed")
        sheet.write(0, 10, "MGR' = reactions with flux > 0")
        sheet.write(0, 11, "Y = rections included from dead reactions")
        sheet.write(0, 12, "X = reactions that become dead reactions")
        sheet.write(0, 13, "upper bound")
        sheet.write(0, 14, "lower bound")
        counters[sheet] = 1

    # FVA
    MGR = alive_flux(model, sol_fba)
    if config.optimization == OptimizationEnum.FBA:
        verbose_f("Computing Flux Variability Analysis", model_uuid)
        fba_fva = flux_variability_analysis(
            model, processes=PROCESSES, fraction_of_optimum=fraction_of_optimum
        )
    elif config.optimization == OptimizationEnum.pFBA:
        verbose_f("Computing parsimonious Flux Variability Analysis", model_uuid)
        fba_fva = flux_variability_analysis(
            model,
            pfba_factor=1.0,
            processes=PROCESSES,
            fraction_of_optimum=fraction_of_optimum,
        )
    else:
        pass

    fluxes_fva = fva_fluxes(model, fba_fva)
    NR_PLUS_RR = alive_reactions(model, fba_fva)

    verbose_f("Computing suboptimal Flux Variability Analysis", model_uuid)
    cpmodel = read_config_model(MODEL, config)
    cpmodel.fva(update_flux=True, threshold=0.0)
    DR_0 = set([r.id for r in cpmodel.dead_reactions()])
    cpmodel.find_chokepoints(exclude_dead_reactions=True)
    CP_0 = set([r.id for r, m in cpmodel.chokepoints()])

    verbose_f("Computing optimal Flux Variability Analysis", model_uuid)
    cpmodel = read_config_model(MODEL, config)
    cpmodel.fva(update_flux=True, threshold=1.0)
    DR_1 = set([r.id for r in cpmodel.dead_reactions()])
    cpmodel.find_chokepoints(exclude_dead_reactions=True)
    CP_1 = set([r.id for r, m in cpmodel.chokepoints()])

    verbose_f("Computing suboptimal Flux Variability Analysis", model_uuid)
    cpmodel = read_config_model(MODEL, config)
    cpmodel.fva(update_flux=True, threshold=0.9)
    DR_09 = set([r.id for r in cpmodel.dead_reactions()])

    cpmodel = read_config_model(MODEL, config)
    model = cpmodel.model()

    info.write(0, 0, "MODEL ID")
    info.write(0, 1, model.id)
    info.write(1, 0, "REACTIONS")
    info.write(1, 1, len(model.reactions))
    info.write(2, 0, "METABOLITES")
    info.write(2, 1, len(model.metabolites))
    info.write(3, 0, "GENES")
    info.write(3, 1, len(model.genes))
    info.write(4, 0, "OBJECTIVE")
    info.write(4, 1, str(model.objective.expression))

    info.write(6, 0, "DR gamma = 1.0")
    info.write(6, 1, len(DR_1))
    info.write(7, 0, "SOR = sub-optimal reactions")
    info.write(7, 1, len(DR_1.difference(DR_09)))
    info.write(8, 0, "ER = essential reactions")
    info.write(8, 1, len(ER))
    info.write(9, 0, "MGER = essential reactions for maximum growth")
    info.write(9, 1, len(MGER))

    wider_count = 0
    tight_count = 0
    initial_flux_count = 0

    non_coped_reactions = []

    i_cr = 1
    i_or = 1
    i_or_er = 1
    i_or_subop = 1

    cpmodel = read_config_model(MODEL, config)
    model = cpmodel.model()

    for r in NR_PLUS_RR:

        print(r)
        try:
            # with submit:
            cpmodel = read_config_model(MODEL, config)
            model = cpmodel.model()

            knock_reaction = model.reactions.get_by_id(r)
            knock_reaction.upper_bound = float(0.0)
            knock_reaction.lower_bound = float(0.0)

            verbose_f(
                "Computing results for reaction: " + knock_reaction.id, model_uuid
            )

            aux_sol = 0
            if config.optimization == OptimizationEnum.FBA:
                aux_sol = model.optimize()
            elif config.optimization == OptimizationEnum.pFBA:
                aux_sol = cobra.flux_analysis.pfba(model)
            else:
                pass

            MGR_prima = set([r for r in alive_flux(model, aux_sol)])

            if not config.skip_knockout_computation:
                if config.optimization == OptimizationEnum.FBA:
                    prima_fva_sol = flux_variability_analysis(
                        model,
                        processes=PROCESSES,
                        fraction_of_optimum=fraction_of_optimum,
                    )
                elif config.optimization == OptimizationEnum.pFBA:
                    prima_fva_sol = flux_variability_analysis(
                        model,
                        pfba_factor=1.0,
                        processes=PROCESSES,
                        fraction_of_optimum=fraction_of_optimum,
                    )
                else:
                    pass

                NR_PLUS_RR_prima = alive_reactions(model, prima_fva_sol)
                DR_prima = set([r.id for r in model.reactions]).difference(
                    set(NR_PLUS_RR_prima)
                )
                Y = DR_prima.difference(DR_1)

            if r in chokepoints:
                is_choke = "TRUE"
            else:
                is_choke = ""

            if r in CP_0:
                isCP0 = "TRUE"
            else:
                isCP0 = ""

            if r in CP_1:
                isCP1 = "TRUE"
            else:
                isCP1 = ""

            if r in ER:
                inER = "TRUE"
            else:
                inER = ""

            if aux_sol.objective_value >= MAX_GROWTH - CONST_EPSILON:
                inMGER = ""
            else:
                inMGER = "TRUE"
                non_coped_reactions.append(r)

            if abs(sol_fba[r]) >= CONST_EPSILON:
                initial_flux_count = initial_flux_count + 1
                initial_flux = "TRUE"
            else:
                initial_flux = ""

            up, low = fluxes_fva[r]
            if up - low < CONST_EPSILON:
                if r in ER:
                    sheet = sheetcrer
                else:
                    sheet = sheetcr
            else:
                if r in ER:
                    sheet = sheetorer
                elif in_range_zero(up, low):
                    sheet = sheetor
                else:
                    sheet = sheetorsubop

            changed = set([])
            for rr in model.reactions:
                if abs(aux_sol[rr.id] - sol_fba[rr.id]) > CONST_EPSILON:
                    changed.add(rr.id)

            i = counters[sheet]

            if not config.skip_knockout_computation:
                cell_X = "{}: {}".format(
                    len(set(MGR_prima).intersection(DR_1)),
                    str(set(MGR_prima).intersection(DR_1)),
                )
                cell_Y = "{}: {}".format(len(Y), str(Y))
            else:
                cell_X = " "
                cell_Y = " "
            cell_MGR = "{}: {}".format(len(MGR_prima), str(MGR_prima))
            cell_changed = "{}: {}".format(len(changed), str(changed))
            cell_sum_flux = sum([abs(jj) for jj in aux_sol])
            cell_objective = aux_sol.objective_value

            sheet.write(i, 0, r)
            sheet.write(i, 1, is_choke)
            sheet.write(i, 2, isCP0)
            sheet.write(i, 3, isCP1)
            sheet.write(i, 4, inER)
            sheet.write(i, 5, inMGER)
            sheet.write(i, 6, initial_flux)
            sheet.write(i, 7, cell_objective)
            sheet.write(i, 8, cell_sum_flux)
            sheet.write(i, 9, cell_changed)
            sheet.write(i, 10, cell_MGR)
            sheet.write(i, 11, cell_X)
            sheet.write(i, 12, cell_Y)
            sheet.write(i, 13, up)
            sheet.write(i, 14, low)

            counters[sheet] = counters[sheet] + 1

        except Exception as err:
            non_coped_reactions.append(r)
            print(err)

            sheet.write(i, 0, r)
            sheet.write(i, 1, INFEASIBLE)
            sheet.write(i, 2, INFEASIBLE)
            sheet.write(i, 3, INFEASIBLE)
            sheet.write(i, 4, INFEASIBLE)
            sheet.write(i, 5, INFEASIBLE)
            sheet.write(i, 6, INFEASIBLE)
            sheet.write(i, 7, INFEASIBLE)
            sheet.write(i, 8, INFEASIBLE)
            sheet.write(i, 9, INFEASIBLE)
            sheet.write(i, 10, INFEASIBLE)
            sheet.write(i, 11, INFEASIBLE)
            sheet.write(i, 12, INFEASIBLE)
            sheet.write(i, 13, INFEASIBLE)
            sheet.write(i, 14, INFEASIBLE)

    book.save(output_path)

    print("tight count: ", tight_count)
    print("wider count: ", wider_count)
    print("flux with pfba: ", initial_flux_count)
