#!/usr/bin/python3
# ******************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2022-2022. All rights reserved.
# licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN 'AS IS' BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# ******************************************************************************/
"""
Time:
Author:
Description: It's a statistic diagnose.
"""
import heapq
from typing import Dict, List, Tuple, Optional

from diana.core.experiment.algorithm import Algorithm

metric_score = {}


class StatisticDiag(Algorithm):
    """
    It's a statistic diagnose, its steps are shown as belows:
    1. count number of abnormal metric in each host.
    2. select the top-K hosts as the candidates.
    3. count the fault score according to weighted abnormal.
    4. choose the top-1 host and metric.
    """

    __slots__ = ['__candidate_num', "__min_candidate_num"]

    def __init__(self, candidate_num: int = 5):
        self.__candidate_num = candidate_num
        self.__min_candidate_num = 1
        self.__verify_args()

    def __verify_args(self):
        if self.__candidate_num <= self.__min_candidate_num:
            raise ValueError(
                f"candidate num {self.__candidate_num} is inappropriate, \
                it should be larger than {self.__min_candidate_num}"
            )

    @property
    def candidate_num(self) -> int:
        return self.__candidate_num

    @property
    def min_candidate_num(self) -> int:
        return self.__min_candidate_num

    @property
    def info(self) -> Dict[str, str]:
        data = {
            "algo_name": "statistics_diag",
            "field": "diag",
            "description": "It's a statistic diagnose method",
            "path": "diana.core.experiment.algorithm.diag.statistic_diag.StatisticDiag",
        }
        return data

    def get_root(self, candidate: List[str], check_result: Dict[str, List[Dict[str, str]]]) -> str:
        root = ""
        max_score = 0
        for host_id in candidate:
            fault_score = self.count_fault_score(check_result[host_id])
            if fault_score > max_score:
                max_score = fault_score
                root = host_id
        return root

    @staticmethod
    def count_fault_score(failure_info: List[Dict[str, str]], score_map: Optional[Dict] = metric_score) -> int:
        score = 0
        for failure in failure_info:
            score += score_map.get(failure['metric_name'], 0.5)

        return score

    def count_person_coefficient(self):
        ...

    def get_candidate(self, check_result: Dict[str, List[Dict[str, str]]]) -> List[str]:
        # # all hosts are candidates
        if len(check_result) <= self.candidate_num:
            return list(check_result.keys())

        topk_list = []
        for host_id, metric_list in check_result.items():
            if len(topk_list) < self.candidate_num:
                heapq.heappush(topk_list, (len(metric_list), host_id))
            else:
                metric_list_len = len(metric_list)
                if topk_list[0][0] < metric_list_len:
                    heapq.heappop(topk_list)
                    heapq.heappush(topk_list, (metric_list_len, host_id))

        return [data[1] for data in topk_list]

    def calculate(self, check_result: Dict[str, List[Dict[str, str]]]) -> Tuple[str, str, str]:
        """
        Execute entry.

        Args:
            check_result: e.g.
                {
                    "host1": [{"metric_name": "metric1", "metric_label": "label1"],
                    "host2": [{"metric_name": "metric1", "metric_label": "label1"],
                    "host3": [{"metric_name": "metric1", "metric_label": "label1"]
                }

        Returns:
            tuple: 'host1', 'metric1', 'label1
        """
        candidate = self.get_candidate(check_result)
        root_host = self.get_root(candidate, check_result)
        return root_host, "", ""
