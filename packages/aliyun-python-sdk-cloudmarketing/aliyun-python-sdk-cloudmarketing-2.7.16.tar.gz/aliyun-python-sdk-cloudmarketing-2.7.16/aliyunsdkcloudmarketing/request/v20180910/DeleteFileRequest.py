# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest

class DeleteFileRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'cloudmarketing', '2018-09-10', 'DeleteFile')
		self.set_method('POST')

	def get_FileId(self):
		return self.get_query_params().get('FileId')

	def set_FileId(self,FileId):
		self.add_query_param('FileId',FileId)