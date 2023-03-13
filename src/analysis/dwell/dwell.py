import math
from typing import List

import numpy as np
from scipy import signal
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup
import itertools

NO_EVENT = 0
COUNTING = 1
EVENT = 2
b = [1 / 3, 1 / 3, 1 / 3]
a = 1
MOV_AVG_LENGTH_MONO_SCALE_FACTOR = 20

# TODO Add checks on input
def detect_events_from_data_group(data_group: DataGroup, sampling_rate: float, min_event_length,
                                  max_event_length) -> List[BasicData]:
    events = [detect_events_from_basic_data(bd, sampling_rate, min_event_length, max_event_length)
              for bd in data_group.basic_data]
    return list(itertools.chain(*[e for e in events if len(e) != 0]))


def detect_events_from_basic_data(basic_data: BasicData, sampling_rate: float, min_event_length, max_event_length) -> \
List[BasicData]:
    mov_avg_length_mono = max_event_length * MOV_AVG_LENGTH_MONO_SCALE_FACTOR
    mov_avg_length = mov_avg_length_mono * 2 + 1
    max_event_length_mono = math.floor(max_event_length / 2)
    max_std = 0.2e-9
    mov_avg_den = mov_avg_length - max_event_length

    raw = basic_data.y
    if mov_avg_length > len(raw):
        # todo Handle this one better
        print("mov_avg troppo grossa")
        return []

    smoothed = signal.filtfilt(b, a, raw)
    smoothed = smoothed[mov_avg_length_mono + 1:len(smoothed) - mov_avg_length_mono]
    cs = np.cumsum(raw)
    cs2 = np.cumsum(np.power(raw, 2))

    center = np.array(range(mov_avg_length_mono + 1, len(raw) - mov_avg_length_mono))
    if len(center) == 0:
        return []
    m = (cs[center + mov_avg_length_mono] - cs[center + max_event_length_mono] + cs[
        center - 1 - max_event_length_mono] - cs[center - 1 - mov_avg_length_mono]) / mov_avg_den

    s = np.sqrt((cs2[center + mov_avg_length_mono] - cs2[center + max_event_length_mono] + cs2[
        center - 1 - max_event_length_mono] - cs2[center - 1 - mov_avg_length_mono]) / mov_avg_den - np.power(m, 2))
    # TODO this 3 could be taken from input
    th = m + 3 * s

    status = NO_EVENT
    count = 0
    events = []
    begin_of_event = 0
    end_of_event = 0
    # print("analyzing")
    for i in range(len(center)):
        if status == NO_EVENT:
            if s[i] > max_std:
                continue
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
                events.append([begin_of_event, end_of_event])
                status = NO_EVENT
    # print("done, found events are: ", len(events))
    list_of_basic_data_to_return = []
    for event in events:
        start, end = event
        start += mov_avg_length_mono
        end += mov_avg_length_mono
        ev_range = (end - start) * 2
        start = start - ev_range if start - ev_range > 0 else 0
        end = end + ev_range if end + ev_range < len(raw) - 1 else len(raw) - 1
        list_of_basic_data_to_return.append(
            BasicData(ch=basic_data.ch, y=raw[start:end], sweep_number=basic_data.sweep_number,
                      measuring_unit=basic_data.measuring_unit, file_path=basic_data.filepath, name=basic_data.name,
                      axis=basic_data.axis))
    return list_of_basic_data_to_return
