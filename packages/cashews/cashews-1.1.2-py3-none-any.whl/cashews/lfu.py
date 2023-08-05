from collections import Counter
from datetime import datetime


class SnapShotLfu:
    def __init__(self, size=10, timeframe=60, snapshots=10):
        self._size = size
        self._shapshots_timeframe = timeframe  # sec
        self._shapshots = [Counter() for _ in range(snapshots)]

    def _get_bucket(self) -> int:
        return int(datetime.utcnow().timestamp() / self._shapshots_timeframe) % len(self._shapshots)

    def _get_snapshot(self):
        return self._shapshots[self._get_bucket()]

    def trim(self):
        for index, _ in enumerate(self._shapshots):
            self._trim(index)

    def _trim(self, snapshot_index):
        if len(self._shapshots[snapshot_index]) > self._size:
            self._shapshots[snapshot_index] = Counter(self._shapshots[snapshot_index].most_common(self._size))

    def hit(self, key):
        snapshot_index = self._get_bucket()
        prev = len(self._shapshots) - snapshot_index - 1
        self._trim(prev)
        self._shapshots[snapshot_index][key] += 1

    def check(self, key) -> int:
        pass
