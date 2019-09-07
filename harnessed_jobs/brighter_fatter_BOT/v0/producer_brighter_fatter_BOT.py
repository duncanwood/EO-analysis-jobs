#!/usr/bin/env python
"""
Producer script for BOT brighter-fatter analysis.
"""
import os
from bf_jh_task import bf_jh_task
from bot_eo_analyses import get_analysis_types, run_jh_tasks

if 'brighterfatter' in get_analysis_types():
    if os.environ.get('LCATR_USE_PARSL', False) != 'True':
        # Run the python version.
        run_jh_tasks(bf_jh_task)
    else:
        # Run the command-line version.
        bf_jh_task_script \
            = os.path.join(os.environ['EOANALYSISJOBSDIR'], 'harnessed_jobs',
                           'brighter_fatter_BOT', 'v0', 'bf_jh_task.py')
        run_jh_tasks(bf_jh_task_script)
