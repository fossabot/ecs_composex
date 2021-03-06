﻿#  -*- coding: utf-8 -*-
#   ECS ComposeX <https://github.com/lambda-my-aws/ecs_composex>
#   Copyright (C) 2020-2021  John Mille <john@lambda-my-aws.io>
#  #
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from troposphere import Not, Ref, Equals

from ecs_composex.dns import dns_params

CREATE_PUBLIC_NAMESPACE_CON_T = "CreatePublicServicesNamespaceCondition"
CREATE_PUBLIC_NAMESPACE_CON = Not(
    Equals(
        Ref(dns_params.PUBLIC_DNS_ZONE_NAME), dns_params.PUBLIC_DNS_ZONE_NAME.Default
    )
)
CREATE_PUBLIC_ZONE_CON_T = "CreatePublicServicesZoneCondition"
CREATE_PUBLIC_ZONE_CON = Not(
    Equals(
        Ref(dns_params.PUBLIC_DNS_ZONE_NAME), dns_params.PUBLIC_DNS_ZONE_NAME.Default
    )
)
CREATE_PRIVATE_NAMESPACE_CON_T = "CreatePrivateServicesNamespaceCondition"
CREATE_PRIVATE_NAMESPACE_CON = Equals(
    Ref(dns_params.PRIVATE_DNS_ZONE_ID), dns_params.PRIVATE_DNS_ZONE_ID.Default
)

USE_DEFAULT_ZONE_NAME_CON_T = "UseDefaultPrivateZoneName"
USE_DEFAULT_ZONE_NAME_CON = Equals(
    Ref(dns_params.PRIVATE_DNS_ZONE_NAME), dns_params.PRIVATE_DNS_ZONE_NAME.Default
)

PRIVATE_ZONE_ID_CON_T = "PrivateNamespaceCondition"
PRIVATE_ZONE_ID_CON = Not(
    Equals(Ref(dns_params.PRIVATE_DNS_ZONE_ID), dns_params.PRIVATE_DNS_ZONE_ID.Default)
)
