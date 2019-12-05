# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests to assure the CorpType Class.

Test-Suite to ensure that the CorpType Class is working as expected.
"""

import pytest

from pay_api.services.base_payment_system import PaymentSystemService
from pay_api.services.internal_pay_service import InternalPayService
from pay_api.services.paybc_service import PaybcService
from pay_api.utils.enums import PaymentSystem, Role
from pay_api.utils.errors import Error


def test_paybc_system_factory(session):
    """Assert a paybc service is returned."""
    from pay_api.factory.payment_system_factory import PaymentSystemFactory  # noqa I001; errors out the test case

    # Test for CC and CP
    instance = PaymentSystemFactory.create(payment_method='CC', corp_type='CP')
    assert isinstance(instance, PaybcService)
    assert isinstance(instance, PaymentSystemService)

    # Test for CC and CP with staff role
    token_info = {'realm_access': {'roles': [Role.STAFF.value]}}
    instance = PaymentSystemFactory.create(token_info, payment_method='CC', corp_type='CP')
    assert isinstance(instance, InternalPayService)
    assert isinstance(instance, PaymentSystemService)

    # Test for CC and CP with zero fees role
    instance = PaymentSystemFactory.create(fees=0, payment_method='CC', corp_type='CP')
    assert isinstance(instance, InternalPayService)
    assert isinstance(instance, PaymentSystemService)

    # Test for PAYBC Service
    instance = PaymentSystemFactory.create_from_system_code(PaymentSystem.PAYBC.value)
    assert isinstance(instance, PaybcService)
    assert isinstance(instance, PaymentSystemService)

    # Test for Internal Service
    instance = PaymentSystemFactory.create_from_system_code(PaymentSystem.INTERNAL.value)
    assert isinstance(instance, InternalPayService)
    assert isinstance(instance, PaymentSystemService)


def test_invalid_pay_system(session):
    """Test invalid data."""
    from pay_api.factory.payment_system_factory import PaymentSystemFactory  # noqa I001; errors out the test case

    from pay_api.exceptions import BusinessException

    with pytest.raises(BusinessException) as excinfo:
        PaymentSystemFactory.create(payment_method=None, corp_type=None)
    assert excinfo.value.status == Error.PAY003.status
    assert excinfo.value.message == Error.PAY003.message
    assert excinfo.value.code == Error.PAY003.name

    with pytest.raises(BusinessException) as excinfo:
        PaymentSystemFactory.create(payment_method='XXX', corp_type='XXX')
    assert excinfo.value.status == Error.PAY003.status
    assert excinfo.value.message == Error.PAY003.message
    assert excinfo.value.code == Error.PAY003.name

    with pytest.raises(BusinessException) as excinfo:
        PaymentSystemFactory.create_from_system_code('XXX')
    assert excinfo.value.status == Error.PAY003.status
    assert excinfo.value.message == Error.PAY003.message
    assert excinfo.value.code == Error.PAY003.name
