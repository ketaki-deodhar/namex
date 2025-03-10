# Copyright © 2025 Province of British Columbia
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
"""The Unit Tests for the pick up template."""
import base64
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

from flask import request

from namex_emailer.email_processors import get_main_template


@pytest.mark.parametrize(
    ["test_name", "request_action", "status", "template_name", "expected_resource"],
    [
        ("get_main_template", "AML", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "AML", "approved", "approved-colin.md", "main"),
        ("get_main_template", "AML", "approved", "approved-so.md", "main"),
        ("get_main_template", "AML", "approved", "approved.md", "main"),
        ("get_main_template", "AML", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "AML", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "AML", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "AML", "conditional", "conditional.md", "main"),
        ("get_main_template", "AML", "consent", "consent-colin.md", "main"),
        ("get_main_template", "AML", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "AML", "consent", "consent-so.md", "main"),
        ("get_main_template", "AML", "consent", "consent.md", "main"),
        ("get_main_template", "AML", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "AML", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "AML", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "AML", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "AML", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "AML", None, "NR-PAID.html", "main"),
        ("get_main_template", "AML", None, "NR-REFUND.html", "main"),
        ("get_main_template", "AML", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "AML", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "AML", None, "rejected.md", "main"),

        ("get_main_template", "ASSUMED", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "ASSUMED", "approved", "approved-colin.md", "main"),
        ("get_main_template", "ASSUMED", "approved", "approved-so.md", "main"),
        ("get_main_template", "ASSUMED", "approved", "approved.md", "main"),
        ("get_main_template", "ASSUMED", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "ASSUMED", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "ASSUMED", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "ASSUMED", "conditional", "conditional.md", "main"),
        ("get_main_template", "ASSUMED", "consent", "consent-colin.md", "main"),
        ("get_main_template", "ASSUMED", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "ASSUMED", "consent", "consent-so.md", "main"),
        ("get_main_template", "ASSUMED", "consent", "consent.md", "main"),
        ("get_main_template", "ASSUMED", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "ASSUMED", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "ASSUMED", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "ASSUMED", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "ASSUMED", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "ASSUMED", None, "NR-PAID.html", "main"),
        ("get_main_template", "ASSUMED", None, "NR-REFUND.html", "main"),
        ("get_main_template", "ASSUMED", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "ASSUMED", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "ASSUMED", None, "rejected.md", "main"),

        ("get_main_template", "CHG", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "CHG", "approved", "approved-colin.md", "main"),
        ("get_main_template", "CHG", "approved", "approved-so.md", "main"),
        ("get_main_template", "CHG", "approved", "approved.md", "main"),
        ("get_main_template", "CHG", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "CHG", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "CHG", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "CHG", "conditional", "conditional.md", "main"),
        ("get_main_template", "CHG", "consent", "consent-colin.md", "main"),
        ("get_main_template", "CHG", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "CHG", "consent", "consent-so.md", "main"),
        ("get_main_template", "CHG", "consent", "consent.md", "main"),
        ("get_main_template", "CHG", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "CHG", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "CHG", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "CHG", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "CHG", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "CHG", None, "NR-PAID.html", "main"),
        ("get_main_template", "CHG", None, "NR-REFUND.html", "main"),
        ("get_main_template", "CHG", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "CHG", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "CHG", None, "rejected.md", "main"),

        ("get_main_template", "CHG-ASSUM", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "CHG-ASSUM", "approved", "approved-colin.md", "main"),
        ("get_main_template", "CHG-ASSUM", "approved", "approved-so.md", "main"),
        ("get_main_template", "CHG-ASSUM", "approved", "approved.md", "main"),
        ("get_main_template", "CHG-ASSUM", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "CHG-ASSUM", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "CHG-ASSUM", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "CHG-ASSUM", "conditional", "conditional.md", "main"),
        ("get_main_template", "CHG-ASSUM", "consent", "consent-colin.md", "main"),
        ("get_main_template", "CHG-ASSUM", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "CHG-ASSUM", "consent", "consent-so.md", "main"),
        ("get_main_template", "CHG-ASSUM", "consent", "consent.md", "main"),
        ("get_main_template", "CHG-ASSUM", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "CHG-ASSUM", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "CHG-ASSUM", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "CHG-ASSUM", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "CHG-ASSUM", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "CHG-ASSUM", None, "NR-PAID.html", "main"),
        ("get_main_template", "CHG-ASSUM", None, "NR-REFUND.html", "main"),
        ("get_main_template", "CHG-ASSUM", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "CHG-ASSUM", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "CHG-ASSUM", None, "rejected.md", "main"),

        ("get_main_template", "CNV", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "CNV", "approved", "approved-colin.md", "main"),
        ("get_main_template", "CNV", "approved", "approved-so.md", "main"),
        ("get_main_template", "CNV", "approved", "approved.md", "main"),
        ("get_main_template", "CNV", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "CNV", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "CNV", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "CNV", "conditional", "conditional.md", "main"),
        ("get_main_template", "CNV", "consent", "consent-colin.md", "main"),
        ("get_main_template", "CNV", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "CNV", "consent", "consent-so.md", "main"),
        ("get_main_template", "CNV", "consent", "consent.md", "main"),
        ("get_main_template", "CNV", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "CNV", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "CNV", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "CNV", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "CNV", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "CNV", None, "NR-PAID.html", "main"),
        ("get_main_template", "CNV", None, "NR-REFUND.html", "main"),
        ("get_main_template", "CNV", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "CNV", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "CNV", None, "rejected.md", "main"),

        ("get_main_template", "DBA", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "DBA", "approved", "approved-colin.md", "main"),
        ("get_main_template", "DBA", "approved", "approved-so.md", "main"),
        ("get_main_template", "DBA", "approved", "approved.md", "main"),
        ("get_main_template", "DBA", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "DBA", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "DBA", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "DBA", "conditional", "conditional.md", "main"),
        ("get_main_template", "DBA", "consent", "consent-colin.md", "main"),
        ("get_main_template", "DBA", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "DBA", "consent", "consent-so.md", "main"),
        ("get_main_template", "DBA", "consent", "consent.md", "main"),
        ("get_main_template", "DBA", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "DBA", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "DBA", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "DBA", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "DBA", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "DBA", None, "NR-PAID.html", "main"),
        ("get_main_template", "DBA", None, "NR-REFUND.html", "main"),
        ("get_main_template", "DBA", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "DBA", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "DBA", None, "rejected.md", "main"),

        ("get_main_template", "MVE", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "MVE", "approved", "approved-colin.md", "main"),
        ("get_main_template", "MVE", "approved", "approved-so.md", "main"),
        ("get_main_template", "MVE", "approved", "approved.md", "main"),
        ("get_main_template", "MVE", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "MVE", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "MVE", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "MVE", "conditional", "conditional.md", "main"),
        ("get_main_template", "MVE", "consent", "consent-colin.md", "main"),
        ("get_main_template", "MVE", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "MVE", "consent", "consent-so.md", "main"),
        ("get_main_template", "MVE", "consent", "consent.md", "main"),
        ("get_main_template", "MVE", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "MVE", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "MVE", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "MVE", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "MVE", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "MVE", None, "NR-PAID.html", "main"),
        ("get_main_template", "MVE", None, "NR-REFUND.html", "main"),
        ("get_main_template", "MVE", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "MVE", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "MVE", None, "rejected.md", "main"),

        ("get_main_template", "NEW", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "NEW", "approved", "approved-colin.md", "main"),
        ("get_main_template", "NEW", "approved", "approved-so.md", "main"),
        ("get_main_template", "NEW", "approved", "approved.md", "main"),
        ("get_main_template", "NEW", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "NEW", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "NEW", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "NEW", "conditional", "conditional.md", "main"),
        ("get_main_template", "NEW", "consent", "consent-colin.md", "main"),
        ("get_main_template", "NEW", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "NEW", "consent", "consent-so.md", "main"),
        ("get_main_template", "NEW", "consent", "consent.md", "main"),
        ("get_main_template", "NEW", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "NEW", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "NEW", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "NEW", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "NEW", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "NEW", None, "NR-PAID.html", "main"),
        ("get_main_template", "NEW", None, "NR-REFUND.html", "main"),
        ("get_main_template", "NEW", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "NEW", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "NEW", None, "rejected.md", "main"),

        ("get_main_template", "NRO-NEWAML", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "NRO-NEWAML", "approved", "approved-colin.md", "main"),
        ("get_main_template", "NRO-NEWAML", "approved", "approved-so.md", "main"),
        ("get_main_template", "NRO-NEWAML", "approved", "approved.md", "main"),
        ("get_main_template", "NRO-NEWAML", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "NRO-NEWAML", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "NRO-NEWAML", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "NRO-NEWAML", "conditional", "conditional.md", "main"),
        ("get_main_template", "NRO-NEWAML", "consent", "consent-colin.md", "main"),
        ("get_main_template", "NRO-NEWAML", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "NRO-NEWAML", "consent", "consent-so.md", "main"),
        ("get_main_template", "NRO-NEWAML", "consent", "consent.md", "main"),
        ("get_main_template", "NRO-NEWAML", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "NRO-NEWAML", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "NRO-NEWAML", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "NRO-NEWAML", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "NRO-NEWAML", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "NRO-NEWAML", None, "NR-PAID.html", "main"),
        ("get_main_template", "NRO-NEWAML", None, "NR-REFUND.html", "main"),
        ("get_main_template", "NRO-NEWAML", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "NRO-NEWAML", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "NRO-NEWAML", None, "rejected.md", "main"),

        ("get_main_template", "NRO-REST", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "NRO-REST", "approved", "approved-colin.md", "main"),
        ("get_main_template", "NRO-REST", "approved", "approved-so.md", "main"),
        ("get_main_template", "NRO-REST", "approved", "approved.md", "main"),
        ("get_main_template", "NRO-REST", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "NRO-REST", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "NRO-REST", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "NRO-REST", "conditional", "conditional.md", "main"),
        ("get_main_template", "NRO-REST", "consent", "consent-colin.md", "main"),
        ("get_main_template", "NRO-REST", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "NRO-REST", "consent", "consent-so.md", "main"),
        ("get_main_template", "NRO-REST", "consent", "consent.md", "main"),
        ("get_main_template", "NRO-REST", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "NRO-REST", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "NRO-REST", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "NRO-REST", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "NRO-REST", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "NRO-REST", None, "NR-PAID.html", "main"),
        ("get_main_template", "NRO-REST", None, "NR-REFUND.html", "main"),
        ("get_main_template", "NRO-REST", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "NRO-REST", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "NRO-REST", None, "rejected.md", "main"),

        ("get_main_template", "REH", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "REH", "approved", "approved-colin.md", "main"),
        ("get_main_template", "REH", "approved", "approved-so.md", "main"),
        ("get_main_template", "REH", "approved", "approved.md", "main"),
        ("get_main_template", "REH", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "REH", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "REH", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "REH", "conditional", "conditional.md", "main"),
        ("get_main_template", "REH", "consent", "consent-colin.md", "main"),
        ("get_main_template", "REH", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "REH", "consent", "consent-so.md", "main"),
        ("get_main_template", "REH", "consent", "consent.md", "main"),
        ("get_main_template", "REH", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "REH", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "REH", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "REH", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "REH", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "REH", None, "NR-PAID.html", "main"),
        ("get_main_template", "REH", None, "NR-REFUND.html", "main"),
        ("get_main_template", "REH", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "REH", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "REH", None, "rejected.md", "main"),

        ("get_main_template", "REN", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "REN", "approved", "approved-colin.md", "main"),
        ("get_main_template", "REN", "approved", "approved-so.md", "main"),
        ("get_main_template", "REN", "approved", "approved.md", "main"),
        ("get_main_template", "REN", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "REN", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "REN", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "REN", "conditional", "conditional.md", "main"),
        ("get_main_template", "REN", "consent", "consent-colin.md", "main"),
        ("get_main_template", "REN", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "REN", "consent", "consent-so.md", "main"),
        ("get_main_template", "REN", "consent", "consent.md", "main"),
        ("get_main_template", "REN", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "REN", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "REN", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "REN", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "REN", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "REN", None, "NR-PAID.html", "main"),
        ("get_main_template", "REN", None, "NR-REFUND.html", "main"),
        ("get_main_template", "REN", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "REN", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "REN", None, "rejected.md", "main"),

        ("get_main_template", "RESUBMIT", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "RESUBMIT", "approved", "approved-colin.md", "main"),
        ("get_main_template", "RESUBMIT", "approved", "approved-so.md", "main"),
        ("get_main_template", "RESUBMIT", "approved", "approved.md", "main"),
        ("get_main_template", "RESUBMIT", "conditional", "conditional-colin.md", "main"),
        ("get_main_template", "RESUBMIT", "conditional", "conditional-modernized.md", "main"),
        ("get_main_template", "RESUBMIT", "conditional", "conditional-so.md", "main"),
        ("get_main_template", "RESUBMIT", "conditional", "conditional.md", "main"),
        ("get_main_template", "RESUBMIT", "consent", "consent-colin.md", "main"),
        ("get_main_template", "RESUBMIT", "consent", "consent-modernized.md", "main"),
        ("get_main_template", "RESUBMIT", "consent", "consent-so.md", "main"),
        ("get_main_template", "RESUBMIT", "consent", "consent.md", "main"),
        ("get_main_template", "RESUBMIT", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "main"),
        ("get_main_template", "RESUBMIT", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "main"),
        ("get_main_template", "RESUBMIT", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "main"),
        ("get_main_template", "RESUBMIT", "before-expiry", "NR-BEFORE-EXPIRY.html", "main"),
        ("get_main_template", "RESUBMIT", None, "NR-EXPIRED.html", "main"),
        ("get_main_template", "RESUBMIT", None, "NR-PAID.html", "main"),
        ("get_main_template", "RESUBMIT", None, "NR-REFUND.html", "main"),
        ("get_main_template", "RESUBMIT", None, "NR-RENEWAL.html", "main"),
        ("get_main_template", "RESUBMIT", None, "NR-UPGRADE.html", "main"),
        ("get_main_template", "RESUBMIT", None, "rejected.md", "main"),

        ("get_main_template_from_common", "INVALID", "approved", "approved-modernized.md", "common"),
        ("get_main_template_from_common", "INVALID", "approved", "approved-colin.md", "common"),
        ("get_main_template_from_common", "INVALID", "approved", "approved-so.md", "common"),
        ("get_main_template_from_common", "INVALID", "approved", "approved.md", "common"),
        ("get_main_template_from_common", "INVALID", "conditional", "conditional-colin.md", "common"),
        ("get_main_template_from_common", "INVALID", "conditional", "conditional-modernized.md", "common"),
        ("get_main_template_from_common", "INVALID", "conditional", "conditional-so.md", "common"),
        ("get_main_template_from_common", "INVALID", "conditional", "conditional.md", "common"),
        ("get_main_template_from_common", "INVALID", "consent", "consent-colin.md", "common"),
        ("get_main_template_from_common", "INVALID", "consent", "consent-modernized.md", "common"),
        ("get_main_template_from_common", "INVALID", "consent", "consent-so.md", "common"),
        ("get_main_template_from_common", "INVALID", "consent", "consent.md", "common"),
        ("get_main_template_from_common", "INVALID", "before-expiry", "NR-BEFORE-EXPIRY-COLIN.html", "common"),
        ("get_main_template_from_common", "INVALID", "before-expiry", "NR-BEFORE-EXPIRY-modernized.html", "common"),
        ("get_main_template_from_common", "INVALID", "before-expiry", "NR-BEFORE-EXPIRY-so.html", "common"),
        ("get_main_template_from_common", "INVALID", "before-expiry", "NR-BEFORE-EXPIRY.html", "common"),
        ("get_main_template_from_common", "INVALID", None, "NR-EXPIRED.html", "common"),
        ("get_main_template_from_common", "INVALID", None, "NR-PAID.html", "common"),
        ("get_main_template_from_common", "INVALID", None, "NR-REFUND.html", "common"),
        ("get_main_template_from_common", "INVALID", None, "NR-RENEWAL.html", "common"),
        ("get_main_template_from_common", "INVALID", None, "NR-UPGRADE.html", "common"),
        ("get_main_template_from_common", "INVALID", None, "rejected.md", "common"),

        ("no_template_with_valid_request_action", "AML", None, "invalid_name.md", None),
        ("no_template_with_valid_with_request_action", "AML", "approved", "invalid_name.md", None),
        ("no_template", "INVALID", None, "invalid_name.md", None),
    ],
)
def test_nr_notification(
    app, mocker, test_name, request_action, status, template_name, expected_resource
):
    """Assert that get the main template function."""
    mock_log = mocker.patch("namex_emailer.email_processors.structured_log")
    result = get_main_template(request_action, template_name, status)
    if not expected_resource:
        assert result is None
        mock_log.assert_any_call(
            request, "ERROR", f"Failed to get {request_action}, {status}, {template_name} email template"
        )
    else:
        assert isinstance(result, str)
        if expected_resource == "common":
            mock_log.assert_called_once_with(
                request, "DEBUG", f"Not Found the template from {request_action}/{status}/{template_name}"
            )
