import sys

import pytest

from stormevents.usgs import usgs_highwatermark_events
from stormevents.usgs.highwatermarks import (
    EventStatus,
    EventType,
    HighWaterMarks,
    StormHighWaterMarks,
    usgs_highwatermark_storms,
)
from tests import check_reference_directory, OUTPUT_DIRECTORY, REFERENCE_DIRECTORY


def test_usgs_highwatermark_events():
    reference_directory = REFERENCE_DIRECTORY / 'test_usgs_highwatermark_events'
    output_directory = OUTPUT_DIRECTORY / 'test_usgs_highwatermark_events'

    if not output_directory.exists():
        output_directory.mkdir(parents=True, exist_ok=True)

    usgs_highwatermark_events(event_status=EventStatus.COMPLETED)

    events = usgs_highwatermark_events(
        event_type=EventType.HURRICANE,
        year=tuple(range(2003, 2020 + 1)),
        event_status=EventStatus.COMPLETED,
    )

    events.to_csv(output_directory / 'events.csv')

    check_reference_directory(output_directory, reference_directory)


def test_usgs_highwatermark_storms():
    reference_directory = REFERENCE_DIRECTORY / 'test_usgs_highwatermark_storms'
    output_directory = OUTPUT_DIRECTORY / 'test_usgs_highwatermark_storms'

    if not output_directory.exists():
        output_directory.mkdir(parents=True, exist_ok=True)

    storms = usgs_highwatermark_storms(year=tuple(range(2003, 2020 + 1)))

    storms.to_csv(output_directory / 'storms.csv')

    check_reference_directory(output_directory, reference_directory)


@pytest.mark.skipif(
    sys.version_info < (3, 10), reason='floating point differences before python 3.10',
)
def test_HighWaterMarks():
    reference_directory = REFERENCE_DIRECTORY / 'test_HighWaterMarks'
    output_directory = OUTPUT_DIRECTORY / 'test_HighWaterMarks'

    if not output_directory.exists():
        output_directory.mkdir(parents=True, exist_ok=True)

    hwm_florence2018 = HighWaterMarks.from_csv(reference_directory / 'florence2018.csv')
    hwm_irma2017 = HighWaterMarks.from_name('Irma September 2017')

    with pytest.raises(ValueError):
        StormHighWaterMarks.from_name('nonexistent')

    hwm_florence2018.data.to_csv(output_directory / 'florence2018.csv')

    assert hwm_irma2017.data.shape == (221, 52)
    assert hwm_florence2018 != hwm_irma2017

    check_reference_directory(output_directory, reference_directory)


def test_HighWaterMarks_data():
    hwm_1 = HighWaterMarks(182)
    hwm_2 = HighWaterMarks(23, hwm_quality='EXCELLENT')
    hwm_3 = HighWaterMarks('nonexistent')

    assert len(hwm_1.data) == 221
    assert len(hwm_2.data) == 83

    with pytest.raises(ValueError):
        hwm_3.data

    hwm_1.hwm_quality = 'EXCELLENT', 'GOOD'
    hwm_2.hwm_quality = 'EXCELLENT', 'GOOD'
    hwm_3.hwm_quality = 'EXCELLENT', 'GOOD'

    assert len(hwm_1.data) == 138
    assert len(hwm_2.data) == 519

    with pytest.raises(ValueError):
        hwm_3.data

    hwm_3.event_id = 189

    assert len(hwm_3.data) == 10
