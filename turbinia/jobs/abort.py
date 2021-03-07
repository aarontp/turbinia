# -*- coding: utf-8 -*-
# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Job to create abort tasks for graceful job termination."""

from turbinia.workers.abort import AbortTask
from turbinia.jobs import interface
from turbinia.jobs import manager


class AbortJob(interface.TurbiniaJob):
  """Produces abort tasks."""
  
  evidence_input = []

  NAME = 'AbortJob'


  def create_tasks(self, evidence=None):
    """Create task for Plaso.

    Args:
      evidence: None expected for this kind of job.

    Returns:
        A task to accurately report on the reason for job termination.
    """
    #Returning a single task every time in this case.
    abort_task = AbortTask()
    abort_task.task_config['reason'] = evidence[0].config['abort_message']
    return [abort_task]


manager.JobsManager.RegisterJob(AbortJob)
