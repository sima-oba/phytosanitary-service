from application.kafka.consumer.consumer import Consumer, ConsumerGroup
from domain.service import PhytosanitaryService, OrdinanceService
from infrastructure import database
from infrastructure.repository import (
    VisitRepository,
    FarmRepository,
    OrdinanceRepository,
    FileRepository
)
from ..schema import PhytosanitarySchema, AnnualOrdinanceSchema


def start_consumer(config):
    db = database.get_database(config.MONGODB_SETTINGS)
    group = ConsumerGroup({
        'bootstrap.servers': config.KAFKA_SERVER,
        'group.id': 'PHYTOSANITARY',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })

    farm_repo = FarmRepository(db)
    visit_repo = VisitRepository(db)
    phytosan_svc = PhytosanitaryService(visit_repo, farm_repo)
    phytosan_consumer = Consumer(PhytosanitarySchema(), phytosan_svc.save)
    group.add(phytosan_consumer, 'PHYTOSANITARY')

    file_repo = FileRepository(db)
    ord_repo = OrdinanceRepository(db)
    ord_svc = OrdinanceService(ord_repo, file_repo)
    ord_consumer = Consumer(AnnualOrdinanceSchema(), ord_svc.save)
    group.add(ord_consumer, 'ANNUAL_ORDINANCE')

    group.wait()
