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
from flask import jsonify

from diana.database import SESSION
from diana.database.dao.algo_dao import AlgorithmDao
from diana.utils.schema.algorithm import QueryAlgorithmListSchema, QueryAlgorithmSchema
from vulcanus.restful.response import BaseResponse


class QueryAlgorithmList(BaseResponse):
    """
        Interface for get algorithm list.
        Restful API: GET
    """

    def get(self):
        """
            Get algorithm info list
        Returns:
            Response:
                {
                    'code': int,
                    'msg': string,
                    'total_count': int,
                    'total_page': int,
                    'algo_list':[
                            {
                            'algo_id': 'xxx',
                            'algo_name': 'xxx',
                            "description": 'xxx',
                            'field': 'xxx'
                            }
                            ...
                    ]
                }
        """
        return jsonify(self.handle_request_db(QueryAlgorithmListSchema,
                                              AlgorithmDao(),
                                              'query_algorithm_list',
                                              SESSION))


class QueryAlgorithm(BaseResponse):
    """
        Interface for get algorithm list.
        Restful API: GET
    """

    def get(self):
        """
            Get algorithm info
        Returns:
            Response:
                    {
                        "code": int,
                        "msg": "string",
                        "result": {
                            "algo_id": "string",
                            "algo_name": "string",
                            "description": "string",
                            "field": "string"
                        }
                    }
        """
        return jsonify(self.handle_request_db(QueryAlgorithmSchema,
                                              AlgorithmDao(),
                                              'query_algorithm',
                                              SESSION))
