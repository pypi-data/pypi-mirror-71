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

class SetSecurityPreferenceRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ims', '2019-08-15', 'SetSecurityPreference','ims')

	def get_AllowUserToManageAccessKeys(self):
		return self.get_query_params().get('AllowUserToManageAccessKeys')

	def set_AllowUserToManageAccessKeys(self,AllowUserToManageAccessKeys):
		self.add_query_param('AllowUserToManageAccessKeys',AllowUserToManageAccessKeys)

	def get_AllowUserToManageMFADevices(self):
		return self.get_query_params().get('AllowUserToManageMFADevices')

	def set_AllowUserToManageMFADevices(self,AllowUserToManageMFADevices):
		self.add_query_param('AllowUserToManageMFADevices',AllowUserToManageMFADevices)

	def get_EnableSaveMFATicket(self):
		return self.get_query_params().get('EnableSaveMFATicket')

	def set_EnableSaveMFATicket(self,EnableSaveMFATicket):
		self.add_query_param('EnableSaveMFATicket',EnableSaveMFATicket)

	def get_LoginNetworkMasks(self):
		return self.get_query_params().get('LoginNetworkMasks')

	def set_LoginNetworkMasks(self,LoginNetworkMasks):
		self.add_query_param('LoginNetworkMasks',LoginNetworkMasks)

	def get_AllowUserToChangePassword(self):
		return self.get_query_params().get('AllowUserToChangePassword')

	def set_AllowUserToChangePassword(self,AllowUserToChangePassword):
		self.add_query_param('AllowUserToChangePassword',AllowUserToChangePassword)

	def get_LoginSessionDuration(self):
		return self.get_query_params().get('LoginSessionDuration')

	def set_LoginSessionDuration(self,LoginSessionDuration):
		self.add_query_param('LoginSessionDuration',LoginSessionDuration)