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
from aliyunsdkbaas.endpoint import endpoint_data

class CreateAccessTokenRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Baas', '2018-07-31', 'CreateAccessToken')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_AccessTokenLifetime(self):
		return self.get_body_params().get('AccessTokenLifetime')

	def set_AccessTokenLifetime(self,AccessTokenLifetime):
		self.add_body_params('AccessTokenLifetime', AccessTokenLifetime)

	def get_Scope(self):
		return self.get_body_params().get('Scope')

	def set_Scope(self,Scope):
		self.add_body_params('Scope', Scope)

	def get_RefreshTokenLifetime(self):
		return self.get_body_params().get('RefreshTokenLifetime')

	def set_RefreshTokenLifetime(self,RefreshTokenLifetime):
		self.add_body_params('RefreshTokenLifetime', RefreshTokenLifetime)

	def get_OrganizationId(self):
		return self.get_body_params().get('OrganizationId')

	def set_OrganizationId(self,OrganizationId):
		self.add_body_params('OrganizationId', OrganizationId)