import math
from typing import List, Tuple

import numpy as np
from numpy import ndarray
from scipy import signal
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup
import itertools
from enum import Enum

ThresholdModality = Enum('ThresholdModality', ['ABSOLUTE', 'RELATIVE', 'STD_DEV_BASED'])

NO_EVENT = 0
COUNTING = 1
EVENT = 2
b = [1 / 3, 1 / 3, 1 / 3]
a = 1
MOV_AVG_LENGTH_MONO_SCALE_FACTOR = 15


# TODO Add checks on input
# TODO min_event_length, max_event_length dovrebbero prendere delle durate
def detect_events(data_group: DataGroup, min_event_length, max_event_length, threshold: float,
                  threshold_modality: ThresholdModality) -> Tuple[List[ndarray], List[Tuple[int, int]]]:
    tuples = [_detect_events_from_basic_data(bd, data_group.sampling_rate, min_event_length, max_event_length,
                                             threshold, threshold_modality) for bd in data_group.basic_data if bd.axis==0]
    tuples = list(itertools.chain(*[t for t in tuples if len(t) != 0]))
    return [t[0] for t in tuples], [t[1] for t in tuples]


def extract_amplitudes(raws: List[ndarray]) -> ndarray | None:
    if len(raws) == 0:
        return None
    return np.array([abs(raw.max() - raw.min()) for raw in raws])


def extract_durations(raws: List[ndarray], sr: float) -> ndarray | None:
    if len(raws) == 0:
        return None
    return np.array([_get_duration_at_50_percent_amplitude(raw, sr) for raw in raws])


def _get_duration_at_50_percent_amplitude(raw: ndarray, sr: float) -> float:
    a50 = (raw.max() - raw.min())/2
    event_50 = np.nonzero(raw >= raw.min() + a50)[0]
    return len(event_50) / sr


def _detect_events_from_basic_data(basic_data: BasicData, sampling_rate: float, min_event_length, max_event_length,
                                   threshold: float, threshold_modality: ThresholdModality) -> \
        List[Tuple[ndarray, Tuple[int, int]]]:
    # passing from time to samples
    min_event_length = round(sampling_rate * min_event_length)
    max_event_length = round(sampling_rate * max_event_length)
    mov_avg_length_mono = max_event_length * MOV_AVG_LENGTH_MONO_SCALE_FACTOR
    mov_avg_length = mov_avg_length_mono * 2 + 1
    max_event_length_mono = math.floor(max_event_length / 2)
    mov_avg_den = mov_avg_length - max_event_length

    raw = basic_data.y
    if mov_avg_length > len(raw):
        # todo Handle this one better
        print("mov_avg troppo grossa")
        return []

    smoothed = signal.filtfilt(b, a, raw)
    smoothed = smoothed[round(mov_avg_length_mono + 1): round(len(smoothed) - mov_avg_length_mono)]
    cs = np.cumsum(raw, dtype="float64")
    cs2 = np.cumsum(np.power(raw, 2), dtype="float64")

    center = np.array(range(round(mov_avg_length_mono + 1), round(len(raw) - mov_avg_length_mono)), dtype=int)
    if len(center) == 0:
        return []
    first_part = np.array(center + mov_avg_length_mono, dtype=int)
    second_part = np.array(center + max_event_length_mono, dtype=int)
    third_part = np.array(center - 1 - max_event_length_mono, dtype=int)
    fourth_part = np.array(center - 1 - mov_avg_length_mono, dtype=int)
    m = np.array((cs[first_part] - cs[second_part] + cs[third_part] - cs[fourth_part]) / mov_avg_den, dtype="float64")
    s = np.sqrt(np.array((cs2[first_part] - cs2[second_part] + cs2[third_part] - cs2[fourth_part]) / mov_avg_den -
                         np.power(m, 2), dtype="float64"))
    th = np.repeat(threshold, len(m))
    if threshold_modality == ThresholdModality.RELATIVE:
        th = m + threshold
    elif threshold_modality == ThresholdModality.STD_DEV_BASED:
        th = m + threshold * s

    status = NO_EVENT
    count = 0
    events = []
    begin_of_event = 0
    end_of_event = 0
    # print("analyzing")
    for i in range(len(center)):
        if status == NO_EVENT:
            if smoothed[i] > th[i]:
                begin_of_event = i
                count = 1
                status = COUNTING
        elif status == COUNTING:
            if smoothed[i] > th[i]:
                count += 1
                end_of_event = i
                if count >= min_event_length:
                    status = EVENT
            else:
                status = NO_EVENT
        elif status == EVENT:
            if count > max_event_length:
                status = NO_EVENT
                continue
            count += 1
            if smoothed[i] > th[i]:
                end_of_event = i
            if smoothed[i] < m[i] and end_of_event > begin_of_event and count > min_event_length:
                events.append((begin_of_event, end_of_event))
                status = NO_EVENT
    # print("done, found events are: ", len(events))
    return [_create_list_of_events(raw, e, mov_avg_length_mono) for e in events]

    # return [_create_basic_data_from_events(raw, basic_data, e, mov_avg_length_mono) for e in events]


def _create_list_of_events(raw: ndarray, event: Tuple[int, int], mov_avg_length_mono: int) -> \
        Tuple[ndarray, Tuple[int, int]]:
    start, end = event
    start += mov_avg_length_mono
    end += mov_avg_length_mono
    ev_range = (end - start) * 2
    start = start - ev_range if start - ev_range > 0 else 0
    end = end + ev_range if end + ev_range < len(raw) - 1 else len(raw) - 1
    return np.array(raw[int(start):int(end)]), (int(start), int(end))


def _create_basic_data_from_events(raw: ndarray, basic_data: BasicData, event: List[int],
                                   mov_avg_length_mono: int) -> BasicData:
    start, end = event
    start += mov_avg_length_mono
    end += mov_avg_length_mono
    ev_range = (end - start) * 2
    start = start - ev_range if start - ev_range > 0 else 0
    end = end + ev_range if end + ev_range < len(raw) - 1 else len(raw) - 1
    return BasicData(ch=basic_data.ch, y=np.array(raw[int(start):int(end)]), sweep_number=basic_data.sweep_number,
                     measuring_unit=basic_data.measuring_unit, file_path=basic_data.filepath, name=basic_data.name,
                     axis=basic_data.axis)
