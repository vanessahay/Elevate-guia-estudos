# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from app.agent import search_travel_policy, get_regional_annex, get_full_travel_policy


def test_search_travel_policy_flights() -> None:
    result = search_travel_policy("flights economy")
    assert "AIR TRAVEL GUIDELINES" in result or "Economy" in result


def test_get_regional_annex_r1001() -> None:
    result = get_regional_annex("R-1001")
    assert "ANNEX 1" in result
    assert "CC-201" in result
    assert "$151 USD" in result


def test_get_full_travel_policy() -> None:
    result = get_full_travel_policy()
    assert "CYMBAL GROUP CORPORATE TRAVEL & EXPENSE POLICY HANDBOOK" in result
