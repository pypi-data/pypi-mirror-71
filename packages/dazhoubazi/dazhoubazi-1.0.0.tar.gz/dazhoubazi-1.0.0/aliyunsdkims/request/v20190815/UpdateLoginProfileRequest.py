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

class UpdateLoginProfileRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ims', '2019-08-15', 'UpdateLoginProfile','ims')

	def get_UserPrincipalName(self):
		return self.get_query_params().get('UserPrincipalName')

	def set_UserPrincipalName(self,UserPrincipalName):
		self.add_query_param('UserPrincipalName',UserPrincipalName)

	def get_Password(self):
		return self.get_query_params().get('Password')

	def set_Password(self,Password):
		self.add_query_param('Password',Password)

	def get_GenerateRandomPassword(self):
		return self.get_query_params().get('GenerateRandomPassword')

	def set_GenerateRandomPassword(self,GenerateRandomPassword):
		self.add_query_param('GenerateRandomPassword',GenerateRandomPassword)

	def get_PasswordResetRequired(self):
		return self.get_query_params().get('PasswordResetRequired')

	def set_PasswordResetRequired(self,PasswordResetRequired):
		self.add_query_param('PasswordResetRequired',PasswordResetRequired)

	def get_MFABindRequired(self):
		return self.get_query_params().get('MFABindRequired')

	def set_MFABindRequired(self,MFABindRequired):
		self.add_query_param('MFABindRequired',MFABindRequired)

	def get_Status(self):
		return self.get_query_params().get('Status')

	def set_Status(self,Status):
		self.add_query_param('Status',Status)