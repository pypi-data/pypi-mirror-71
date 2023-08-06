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

class BindMFADeviceRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ims', '2019-08-15', 'BindMFADevice','ims')

	def get_UserPrincipalName(self):
		return self.get_query_params().get('UserPrincipalName')

	def set_UserPrincipalName(self,UserPrincipalName):
		self.add_query_param('UserPrincipalName',UserPrincipalName)

	def get_SerialNumber(self):
		return self.get_query_params().get('SerialNumber')

	def set_SerialNumber(self,SerialNumber):
		self.add_query_param('SerialNumber',SerialNumber)

	def get_AuthenticationCode2(self):
		return self.get_query_params().get('AuthenticationCode2')

	def set_AuthenticationCode2(self,AuthenticationCode2):
		self.add_query_param('AuthenticationCode2',AuthenticationCode2)

	def get_AuthenticationCode1(self):
		return self.get_query_params().get('AuthenticationCode1')

	def set_AuthenticationCode1(self,AuthenticationCode1):
		self.add_query_param('AuthenticationCode1',AuthenticationCode1)