import itertools
class DetectSilence:
    def __init__(self) -> None:
        pass
    def db_to_amp(self,db):
        db = float(db)
        return 10 ** (db / 20)

    def detect_silence(self,audio_segment, min_silence_len=1000, silence_thresh=-16, seek_step=1):
        seg_len = len(audio_segment)

        # you can't have a silent portion of a sound that is longer than the sound
        if seg_len < min_silence_len:
            return []

        # convert silence threshold to a float value (so we can compare it to rms)
        silence_thresh = self.db_to_amp(silence_thresh) * audio_segment.max_possible_amplitude

        # find silence and add start and end indicies to the to_cut list
        silence_starts = []

        # check successive (1 sec by default) chunk of sound for silence
        # try a chunk at every "seek step" (or every chunk for a seek step == 1)
        last_slice_start = seg_len - min_silence_len
        slice_starts = range(0, last_slice_start + 1, seek_step)

        # guarantee last_slice_start is included in the range
        # to make sure the last portion of the audio is searched
        if last_slice_start % seek_step:
            slice_starts = itertools.chain(slice_starts, [last_slice_start])

        for i in slice_starts:
            audio_slice = audio_segment[i:i + min_silence_len]
            if audio_slice.rms <= silence_thresh:
                silence_starts.append(i)

        # short circuit when there is no silence
        if not silence_starts:
            return []

        # combine the silence we detected into ranges (start ms - end ms)
        silent_ranges = []

        prev_i = silence_starts.pop(0)
        current_range_start = prev_i

        for silence_start_i in silence_starts:
            continuous = (silence_start_i == prev_i + seek_step)

            # sometimes two small blips are enough for one particular slice to be
            # non-silent, despite the silence all running together. Just combine
            # the two overlapping silent ranges.
            silence_has_gap = silence_start_i > (prev_i + min_silence_len)

            if not continuous and silence_has_gap:
                silent_ranges.append([current_range_start,
                                    prev_i + min_silence_len])
                current_range_start = silence_start_i
            prev_i = silence_start_i

        silent_ranges.append([current_range_start,
                            prev_i + min_silence_len])

        return silent_ranges

    def max_possible_amplitude(self):
        bits = self.sample_width * 8
        max_possible_val = (2 ** bits)