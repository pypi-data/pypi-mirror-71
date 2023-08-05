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

class DescribeFabricChaincodeLogsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Baas', '2018-07-31', 'DescribeFabricChaincodeLogs')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_PeerName(self):
		return self.get_query_params().get('PeerName')

	def set_PeerName(self,PeerName):
		self.add_query_param('PeerName',PeerName)

	def get_Lines(self):
		return self.get_query_params().get('Lines')

	def set_Lines(self,Lines):
		self.add_query_param('Lines',Lines)

	def get_Offset(self):
		return self.get_query_params().get('Offset')

	def set_Offset(self,Offset):
		self.add_query_param('Offset',Offset)

	def get_OrganizationId(self):
		return self.get_query_params().get('OrganizationId')

	def set_OrganizationId(self,OrganizationId):
		self.add_query_param('OrganizationId',OrganizationId)

	def get_ChaincodeId(self):
		return self.get_query_params().get('ChaincodeId')

	def set_ChaincodeId(self,ChaincodeId):
		self.add_query_param('ChaincodeId',ChaincodeId)