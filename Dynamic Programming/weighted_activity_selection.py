WeChat: cstutorcs
QQ: 749389476
Email: tutorcs@163.com
from typing import List

import sys
import os
sys.path.append("../Utilities")

from interval import Interval


def predecessor(intervals: List[int], cur_index: int) -> int:
    for index, interval in enumerate(intervals[:cur_index]):
        if interval.end < intervals[cur_index].start:
            return index
    else:
        return -1


def opt(intervals: List[Interval], 
        cur_index: int, 
        cache: List[Interval]) -> List[int]:
    """
    - j denotes some index in intervals.
    - v_j denotes the jth interval in intervals.
    - p(j) denotes the largest i < j such that 
      interval i is compatible with interval j.

    opt(j) = max({
        - v_j + opt(predecessor(cur_index)) 
          if cur_index in solution.
        - opt(cur_index - 1) if cur_index not in solution.
        - 0 if j = 0
    })

    Essentially, we recursively find the best of either:
        - Picking v_j and then adding onto the optimal solution 
          on the subproblem intervals[0..p(j)].
        - Not picking v_j and then finding the optimal solution
          on the subproblem intervals[0..j - 1].
    """

    if cur_index == -1:
        return 0
    elif cache[cur_index]:
        return cache[cur_index]
    else:
        with_cur_index = len(intervals[cur_index]) + opt(intervals, 
                                                         predecessor(intervals, cur_index),
                                                         cache)
        without_cur_index = opt(intervals, cur_index - 1, cache)

        cache[cur_index] = max(with_cur_index, without_cur_index)
        return cache[cur_index]


def bottom_up_opt(intervals: List[Interval]) -> int:
    dp = [0 for _ in intervals]

    for i in range(len(intervals)):
        dp[i] = max(len(intervals[i]) + dp[predecessor(intervals, i)], dp[i - 1])

    return dp[len(intervals) - 1]


if __name__ == "__main__":
    test_cases = [
        [Interval(0, 3), Interval(2, 10), Interval(5, 100), 
         Interval(10, 101), Interval(999, 10000), Interval(1000, 99999)]
    ]

    for test_case in test_cases:
        cache = [None for _ in test_case]
        print(f"Intervals: {[(interval.start, interval.end) for interval in test_case]}")
        print(f"Maximum Weight (Top Down):"
              f" {opt(test_case, len(test_case) - 1, cache)}")
        print(f"Maximum Weight (Bottom Up):"
              f" {bottom_up_opt(test_case)}")