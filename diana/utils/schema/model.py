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
Description:
"""
from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate


class ModelListFilterSchema(Schema):
    """
    filter schema of model list getting interface
    """
    tag = fields.String(required=False, validate=lambda s: len(s) != 0)
    field = fields.String(required=False, validate=validate.OneOf(["singlecheck", "multicheck", "diag"]))
    model_name = fields.String(required=False, validate=lambda s: len(s) != 0)
    algo_name = fields.List(fields.String(validate=lambda s: len(s) != 0), required=True)


class QueryModelListSchema(Schema):
    """
    schema of query model list interface
    """
    sort = fields.String(required=False, validate=validate.OneOf(["precision"]))
    direction = fields.String(required=False, validate=validate.OneOf(["asc", "desc"]))
    page = fields.Integer(required=False, validate= lambda s: s > 0)
    per_page = fields.Integer(required=False, validate=lambda s: 0 < s < 50)
    filter = fields.Nested(ModelListFilterSchema, required=False)
