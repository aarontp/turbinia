# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc.
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
"""Interface for Jobs."""
import uuid

import logging

from turbinia.evidence import EvidenceCollection
from turbinia import config

log = logging.getLogger('turbinia')


class TurbiniaJob:
  """Base class for Turbinia Jobs.

  Attributes:
    name (str): Name of Job
    id (str): ID of job
    is_finalize_job (bool): True if this is a Job for finalizing the request.
    is_finalized (bool): True if the request has been finalized.
    request_id (str): ID of the request
    priority (int): Job priority from 0-100, lowest == highest priority
    tasks (list): A list of Tasks generated by this Job
    docker_image (str): Docker image to run for this job or None if unavailable.
    completed_task_count (int): The number of Tasks that have been removed.
    evidence (EvidenceCollection): The Evidence returned by Tasks from this Job.
    timeout (int): The amount of seconds to wait before timing out.
  """

  NAME = 'name'

  def __init__(self, request_id=None, evidence_config=None):
    self.name = self.NAME
    self.id = uuid.uuid4().hex
    self.is_finalize_job = False
    self.is_finalized = False
    self.priority = 100
    self.request_id = request_id
    self.tasks = []
    self.docker_image = None
    self.completed_task_count = 0
    self.evidence = EvidenceCollection()
    self.evidence.request_id = request_id
    self.evidence.config = evidence_config if evidence_config else {}
    self.timeout = None

  def check_done(self):
    """Check to see if all Tasks for this Job have completed.

    Returns:
      bool: True if all Tasks have completed, else False.
    """
    if self.completed_task_count and not self.tasks:
      return True
    else:
      return False

  def create_tasks(self, evidence):
    """Create Turbinia tasks to be run.

    Args:
      evidence: A list of evidence objects

    Returns:
      list[TurbiniaTask]: The newly created Tasks.
    """
    raise NotImplementedError

  # pylint: disable=unused-argument
  def create_final_task(self):
    """Create Final Turbinia task to finalize the Job.

    This Task will be run after all of the main Tasks for the Job have been
    completed.  This can be used to "join" or "reduce" all of the output
    Evidence generated by the other Tasks.  These can also generate new
    Evidence, and so these Evidence types should be added to the
    `output_evidence` class variable.

    Returns:
      TurbiniaTask: The Task to run
    """
    return None

  def remove_task(self, task_id):
    """Removes a Task from the Job.

    Args:
      task_id (str): The ID of the task to remove.

    Returns:
      bool: True for success, else False.
    """
    remove_task = None
    for task in self.tasks:
      if task_id == task.id:
        remove_task = task
        break

    if remove_task:
      self.tasks.remove(remove_task)
      log.debug('Removed task {0:s} from Job {1:s}'.format(task_id, self.name))
      self.completed_task_count += 1
    else:
      log.debug(
          'Could not find task {0:s} to remove from Job {1:s}'.format(
              task_id, self.name))
    return bool(remove_task)
