"""
کلاس پایه برای تمام Task های Celery پروژه
"""

import logging
import time

from celery import Task

# Logger اختصاصی Celery
logger = logging.getLogger("celery")


class BaseTask(Task):
    """
    کلاس پایه برای تمام Task های Celery پروژه

    وظایف:
        - ثبت شروع اجرای Task
        - ثبت پایان موفق Task
        - ثبت خطاهای Task
        - ثبت مدت زمان اجرای Task
    """

    abstract = True

    # زمان شروع اجرای هر Task
    _task_start_times: dict[str, float] = {}

    def before_start(
        self,
        task_id,
        args,
        kwargs,
    ):
        """
        ثبت اطلاعات قبل از اجرای Task
        """

        self._task_start_times[task_id] = time.monotonic()

        logger.info(
            "Task started.",
            extra={
                "task_name": self.name,
                "task_id": task_id,
            },
        )

    def on_success(
        self,
        retval,
        task_id,
        args,
        kwargs,
    ):
        """
        ثبت اجرای موفق Task
        """

        duration = self._get_duration(task_id)

        logger.info(
            "Task completed successfully.",
            extra={
                "task_name": self.name,
                "task_id": task_id,
                "duration": duration,
            },
        )

    def on_failure(
        self,
        exc,
        task_id,
        args,
        kwargs,
        einfo,
    ):
        """
        ثبت خطاهای Task
        """

        duration = self._get_duration(task_id)

        logger.error(
            "Task failed.",
            exc_info=einfo,
            extra={
                "task_name": self.name,
                "task_id": task_id,
                "duration": duration,
            },
        )

    def after_return(
        self,
        status,
        retval,
        task_id,
        args,
        kwargs,
        einfo,
    ):
        """
        پاکسازی اطلاعات Task پس از پایان اجرا
        """

        self._task_start_times.pop(
            task_id,
            None,
        )

    def _get_duration(
        self,
        task_id,
    ) -> float | None:
        """
        محاسبه مدت زمان اجرای Task
        """

        start_time = self._task_start_times.get(
            task_id,
        )

        if start_time is None:
            return None

        return round(
            time.monotonic() - start_time,
            3,
        )