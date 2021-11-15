import io, sys
import pytest
import json
from flask import g, session

sys.path.append("..")
from src.restapi.tasks.tasks import task_compute_critical_reactions, task_compute_growth_dependent_reactions

DATA_MODEL_FILE = "tests/data/MODEL1507180056_url.xml"

@pytest.mark.parametrize("filename", [DATA_MODEL_FILE])
def test_compute_critical_reactions(client, filename):
    task_compute_critical_reactions(
        filename,
        "output_path.xls",
        objective=None,
        fraction_of_optimum=None,
        model_uuid=None)


@pytest.mark.parametrize("filename", [DATA_MODEL_FILE])
def test_compute_growth_dependent_reactions(client, filename):
    task_compute_growth_dependent_reactions(
        filename,
        "output_path.xls",
        objective=None,
        model_uuid=None)