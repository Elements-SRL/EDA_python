from dataclasses import dataclass


@dataclass
class FilterArguments:
    """A data class which represents the arguments to pass to a filter

    Attributes
    ---------
    fs: float
        Sampling frequency
    filter_type: {'butter', 'bessel' 'cheby1'}
        Specify the type of filter
    order: int
        Filter order
    b_type:  {'lowpass', 'highpass', 'bandpass', 'bandstop'}
        Band type.
    cutoff_frequency: float
        The critical frequency. For a Butterworth filter, this is the point
        at which the gain drops to 1/sqrt(2) that of the passband (the '-3 dB point').
    other_cutoff_frequency: float | None = None
        Another cutoff frequency needed when b_type is 'bandpass' or 'bandstop'.
    analog: bool = False
        When True return an analog filter. Default is false.
    """

    fs: float
    filter_type: str
    order: int
    b_type: str
    cutoff_frequency: float
    other_cutoff_frequency: float | None = None
    analog: bool = False
