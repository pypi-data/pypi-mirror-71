import datetime
import importlib

from celery import shared_task
from django.conf import settings
from infi.clickhouse_orm.utils import import_submodules

from django_clickhouse.clickhouse_models import ClickHouseModel
from .configuration import config
from .utils import get_subclasses


@shared_task(queue=config.CELERY_QUEUE)
def sync_clickhouse_model(model_cls) -> None:
    """
    Syncs one batch of given ClickHouseModel
    :param model_cls: ClickHouseModel subclass
    :return: None
    """
    model_cls.get_storage().set_last_sync_time(model_cls.get_import_key(), datetime.datetime.now())
    model_cls.sync_batch_from_storage()


@shared_task(queue=config.CELERY_QUEUE)
def clickhouse_auto_sync():
    """
    Plans syncing models
    :return: None
    """
    # Import all model modules
    for app in settings.INSTALLED_APPS:
        package_name = "%s.%s" % (app, config.MODELS_MODULE)
        try:
            module = importlib.import_module(package_name)
            if hasattr(module, '__path__'):
                import_submodules(package_name)
        except ImportError:
            pass

    # Start
    for cls in get_subclasses(ClickHouseModel, recursive=True):
        if cls.need_sync():
            # Даже если синхронизация вдруг не выполнится, не страшно, что мы установили период синхронизации
            # Она выполнится следующей таской через интервал.
            sync_clickhouse_model.delay(cls)
