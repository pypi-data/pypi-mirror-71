import logging
from .logging import logger
from typing import Set, Dict, Callable, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from sentry_sdk import capture_exception
from broccoli_server.worker import WorkerCache, WorkerMetadata, WorkerConfigStore, MetadataStoreFactory, \
    WorkContextFactory
from broccoli_server.content import ContentStore
from broccoli_server.interface.worker import Worker
from broccoli_server.executor import ApsNativeExecutor


class Reconciler(object):
    RECONCILE_JOB_ID = "broccoli.worker_reconcile"

    def __init__(self,
                 worker_config_store: WorkerConfigStore,
                 content_store: ContentStore,
                 metadata_store_factory: MetadataStoreFactory,
                 work_context_factory: WorkContextFactory,
                 worker_cache: WorkerCache,
                 sentry_enabled: bool,
                 pause_workers: bool
                 ):
        self.worker_config_store = worker_config_store
        self.content_store = content_store
        self.metadata_store_factory = metadata_store_factory
        self.work_context_factory = work_context_factory
        self.worker_cache = worker_cache
        self.sentry_enabled = sentry_enabled
        self.pause_workers = pause_workers
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.reconcile,
            id=self.RECONCILE_JOB_ID,
            trigger='interval',
            seconds=10
        )
        self.aps_native_executor = ApsNativeExecutor(
            self.scheduler,
            self.wrap_work,
            self.work_context_factory
        )

    def start(self):
        # Less verbose logging from apscheduler
        apscheduler_logger = logging.getLogger("apscheduler")
        apscheduler_logger.setLevel(logging.ERROR)

        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown(wait=False)

    def reconcile(self):
        if not self.aps_native_executor:
            logger.error("ApsNativeExecutor is not set!")
            return
        actual_job_ids = set(self.aps_native_executor.get_job_ids()) - {self.RECONCILE_JOB_ID}  # type: Set[str]
        desired_jobs = self.worker_config_store.get_all()
        desired_job_ids = set(desired_jobs.keys())  # type: Set[str]

        self.remove_jobs(actual_job_ids=actual_job_ids, desired_job_ids=desired_job_ids)
        self.add_jobs(actual_job_ids=actual_job_ids, desired_job_ids=desired_job_ids, desired_jobs=desired_jobs)
        self.configure_jobs(actual_job_ids=actual_job_ids, desired_job_ids=desired_job_ids, desired_jobs=desired_jobs)

    def remove_jobs(self, actual_job_ids: Set[str], desired_job_ids: Set[str]):
        removed_job_ids = actual_job_ids - desired_job_ids
        if not removed_job_ids:
            logger.debug(f"No job to remove")
            return
        logger.info(f"Going to remove jobs with id {removed_job_ids}")
        for removed_job_id in removed_job_ids:
            self.aps_native_executor.remove_job(removed_job_id)

    def add_jobs(self, actual_job_ids: Set[str], desired_job_ids: Set[str], desired_jobs: Dict[str, WorkerMetadata]):
        added_job_ids = desired_job_ids - actual_job_ids
        if not added_job_ids:
            logger.debug(f"No job to add")
            return
        logger.info(f"Going to add jobs with id {added_job_ids}")
        for added_job_id in added_job_ids:
            self.add_job(added_job_id, desired_jobs)

    def add_job(self, added_job_id: str, desired_jobs: Dict[str, WorkerMetadata]):
        worker_metadata = desired_jobs[added_job_id]

        self.aps_native_executor.add_job(added_job_id, worker_metadata)

    def configure_jobs(self,
                       actual_job_ids: Set[str],
                       desired_job_ids: Set[str],
                       desired_jobs: Dict[str, WorkerMetadata]
                       ):
        # todo: configure job if worker.work bytecode changes..?
        same_job_ids = actual_job_ids.intersection(desired_job_ids)
        for job_id in same_job_ids:
            desired_interval_seconds = desired_jobs[job_id].interval_seconds
            actual_interval_seconds = self.aps_native_executor.get_job_interval_seconds(job_id)
            if desired_interval_seconds != actual_interval_seconds:
                logger.info(f"Going to reconfigure job interval with id {job_id} to {desired_interval_seconds} seconds")
                self.aps_native_executor.set_job_interval_seconds(job_id, desired_interval_seconds)

    def wrap_work(self, worker_metadata: WorkerMetadata, work_context_factory: WorkContextFactory) \
            -> Optional[Callable]:
        module, class_name, args, error_resiliency = \
            worker_metadata.module, worker_metadata.class_name, worker_metadata.args, worker_metadata.error_resiliency
        status, worker_or_message = self.worker_cache.load(module, class_name, args)
        if not status:
            logger.error("Fails to load worker", extra={
                'module': module,
                'class_name': class_name,
                'args': args,
                'message': worker_or_message
            })
            return None
        worker = worker_or_message  # type: Worker
        worker_id = f"broccoli.worker.{worker.get_id()}"
        work_context = work_context_factory.build(worker_id)
        worker.pre_work(work_context)

        def work_wrap():
            try:
                if self.pause_workers:
                    logger.info("Workers have been globally paused")
                    return

                worker.work(work_context)
                # always reset error count
                ok, err = self.worker_config_store.reset_error_count(worker_id)
                if not ok:
                    logger.error("Fails to reset error count", extra={
                        'worker_id': worker_id,
                        'reason': err
                    })
            except Exception as e:
                report_ex = True
                if error_resiliency != -1:
                    ok, error_count, err = self.worker_config_store.get_error_count(worker_id)
                    if not ok:
                        logger.error("Fails to get error count", extra={
                            'worker_id': worker_id,
                            'reason': err
                        })
                    if error_count < error_resiliency:
                        # only not to report exception when error resiliency is set and error count is below resiliency
                        report_ex = False

                if report_ex:
                    if self.sentry_enabled:
                        capture_exception(e)
                    else:
                        print(str(e))
                        logger.exception("Fails to execute work", extra={
                            'worker_id': worker_id,
                        })
                else:
                    print(str(e))
                    logger.info("Not reporting exception because of error resiliency", extra={
                        'worker_id': worker_id
                    })

                if error_resiliency != -1:
                    # only to touch error count if error resiliency is set
                    ok, err = self.worker_config_store.increment_error_count(worker_id)
                    if not ok:
                        logger.error('Fails to increment error count', extra={
                            'worker_id': worker_id,
                            'reason': err
                        })

        return work_wrap
