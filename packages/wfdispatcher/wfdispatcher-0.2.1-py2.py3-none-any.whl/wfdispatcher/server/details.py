from jupyterhubutils import LoggableChild
from argo.workflows.sdk._utils import sanitize_for_serialization
from eliot import log_call
from falcon import HTTPNotFound
from ..objects.workflowmanager import LSSTWorkflowManager


class Details(LoggableChild):

    @log_call
    def on_get(self, req, resp, wf_id, pod_id):
        self.log.debug("Getting details for pod '{}' in workflow '{}'".format(
            pod_id, wf_id))
        wm = LSSTWorkflowManager(req=req)
        wf = wm.get_workflow(wf_id)
        if not wf:
            raise HTTPNotFound()
        nd = wf.status.nodes
        if not nd:
            raise HTTPNotFound()
        pod = nd.get(pod_id)
        if not pod:
            raise HTTPNotFound()
        resp.media = sanitize_for_serialization(pod)
