# SPDX-License-Identifier: MIT
import json
from typing import Any, Dict, List

import pytest

from odxtools.database import Database
from odxtools.diaglayers.diaglayertype import DiagLayerType
from odxtools.diaglayers.ecuvariant import EcuVariant
from odxtools.diaglayers.ecuvariantraw import EcuVariantRaw
from odxtools.diagservice import DiagService
from odxtools.ecuvariantmatcher import EcuVariantMatcher
from odxtools.ecuvariantpattern import EcuVariantPattern
from odxtools.exceptions import OdxError
from odxtools.matchingparameter import MatchingParameter
from odxtools.nameditemlist import NamedItemList
from odxtools.odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId, OdxLinkRef
from odxtools.request import Request
from odxtools.response import Response, ResponseType

doc_frags = [OdxDocFragment(doc_name="pytest", doc_type="WinneThePoh")]

odxlinks = OdxLinkDatabase()


@pytest.fixture
def dummy_response(monkeypatch: pytest.MonkeyPatch) -> Response:
    resp = Response(
        odx_id=OdxLinkId(local_id="dummy_resp", doc_fragments=doc_frags),
        oid=None,
        short_name="dummy_resp",
        long_name=None,
        description=None,
        admin_data=None,
        sdgs=[],
        parameters=NamedItemList(),
        response_type=ResponseType.POSITIVE,
    )
    odxlinks.update({resp.odx_id: resp})

    def decode(message: bytes) -> Dict[str, Any]:
        msg_str = message.decode(encoding="utf-8")
        msg_dict = json.loads(msg_str)
        assert isinstance(msg_dict, dict)
        return msg_dict

    monkeypatch.setattr(resp, "decode", decode)
    return resp


@pytest.fixture()
def ident_service(monkeypatch: pytest.MonkeyPatch, dummy_response: Response) -> DiagService:
    dummy_req = Request(
        odx_id=OdxLinkId(local_id="dummy_req", doc_fragments=doc_frags),
        oid=None,
        short_name="dummy_req",
        long_name=None,
        description=None,
        admin_data=None,
        sdgs=[],
        parameters=NamedItemList(),
    )
    odxlinks.update({dummy_req.odx_id: dummy_req})

    diagService = DiagService(
        odx_id=OdxLinkId(local_id="identService", doc_fragments=doc_frags),
        oid=None,
        short_name="identService",
        long_name=None,
        description=None,
        semantic=None,
        admin_data=None,
        protocol_snrefs=[],
        related_diag_comm_refs=[],
        diagnostic_class=None,
        is_mandatory_raw=None,
        is_executable_raw=None,
        is_final_raw=None,
        comparam_refs=[],
        is_cyclic_raw=None,
        is_multiple_raw=None,
        addressing_raw=None,
        transmission_mode_raw=None,
        audience=None,
        functional_class_refs=[],
        pre_condition_state_refs=[],
        state_transition_refs=[],
        request_ref=OdxLinkRef.from_id(dummy_req.odx_id),
        pos_response_refs=[OdxLinkRef.from_id(dummy_response.odx_id)],
        neg_response_refs=[],
        sdgs=[],
    )

    def encode_request() -> bytes:
        return b"\x22\x10\x00"

    monkeypatch.setattr(diagService, "encode_request", encode_request)
    return diagService


@pytest.fixture
def supplier_service(monkeypatch: pytest.MonkeyPatch, dummy_response: Response) -> DiagService:
    dummy_req = Request(
        odx_id=OdxLinkId(local_id="dummy_req", doc_fragments=doc_frags),
        oid=None,
        short_name="dummy_req",
        long_name=None,
        description=None,
        admin_data=None,
        sdgs=[],
        parameters=NamedItemList(),
    )
    odxlinks.update({dummy_req.odx_id: dummy_req})

    diagService = DiagService(
        odx_id=OdxLinkId(local_id="supplierService", doc_fragments=doc_frags),
        oid=None,
        short_name="supplierService",
        long_name=None,
        description=None,
        semantic=None,
        admin_data=None,
        protocol_snrefs=[],
        related_diag_comm_refs=[],
        diagnostic_class=None,
        is_mandatory_raw=None,
        is_executable_raw=None,
        is_final_raw=None,
        comparam_refs=[],
        is_cyclic_raw=None,
        is_multiple_raw=None,
        addressing_raw=None,
        transmission_mode_raw=None,
        audience=None,
        functional_class_refs=[],
        pre_condition_state_refs=[],
        state_transition_refs=[],
        request_ref=OdxLinkRef.from_id(dummy_req.odx_id),
        pos_response_refs=[OdxLinkRef.from_id(dummy_response.odx_id)],
        neg_response_refs=[],
        sdgs=[],
    )

    def encode_request() -> bytes:
        return b"\x22\x20\x00"

    monkeypatch.setattr(diagService, "encode_request", encode_request)
    return diagService


@pytest.fixture
def ecu_variant_pattern1() -> EcuVariantPattern:
    return EcuVariantPattern(matching_parameters=[
        MatchingParameter(
            diag_comm_snref="identService",
            expected_value="1000",
            out_param_if="id",
        ),
        MatchingParameter(
            diag_comm_snref="supplierService",
            expected_value="supplier_A",
            out_param_if="name.english",
        ),
    ])


@pytest.fixture
def ecu_variant_pattern2() -> EcuVariantPattern:
    return EcuVariantPattern(matching_parameters=[
        MatchingParameter(
            diag_comm_snref="identService",
            expected_value="2000",
            out_param_if="id",
        ),
        MatchingParameter(
            diag_comm_snref="supplierService",
            expected_value="supplier_B",
            out_param_if="name.english",
        ),
    ])


@pytest.fixture
def ecu_variant_pattern3() -> EcuVariantPattern:
    return EcuVariantPattern(matching_parameters=[
        MatchingParameter(
            diag_comm_snref="supplierService",
            expected_value="supplier_C",
            out_param_if="name.english",
        )
    ])


@pytest.fixture
def ecu_variant_1(
    ident_service: DiagService,
    supplier_service: DiagService,
    ecu_variant_pattern1: EcuVariantPattern,
) -> EcuVariant:
    raw_layer = EcuVariantRaw(
        variant_type=DiagLayerType.ECU_VARIANT,
        odx_id=OdxLinkId(local_id="ecu_variant1", doc_fragments=doc_frags),
        oid=None,
        short_name="ecu_variant1",
        long_name=None,
        description=None,
        admin_data=None,
        company_datas=NamedItemList(),
        functional_classes=NamedItemList(),
        diag_data_dictionary_spec=None,
        diag_comms_raw=[ident_service, supplier_service],
        requests=NamedItemList(),
        positive_responses=NamedItemList(),
        negative_responses=NamedItemList(),
        global_negative_responses=NamedItemList(),
        import_refs=[],
        state_charts=NamedItemList(),
        additional_audiences=NamedItemList(),
        sdgs=[],
        parent_refs=[],
        comparam_refs=[],
        ecu_variant_patterns=[ecu_variant_pattern1],
        diag_variables_raw=[],
        variable_groups=NamedItemList(),
        libraries=NamedItemList(),
        dyn_defined_spec=None,
        sub_components=NamedItemList(),
    )
    result = EcuVariant(diag_layer_raw=raw_layer)
    odxlinks.update(result._build_odxlinks())
    db = Database()
    result._resolve_odxlinks(odxlinks)
    result._finalize_init(db, odxlinks)
    return result


@pytest.fixture
def ecu_variant_2(
    ident_service: DiagService,
    supplier_service: DiagService,
    ecu_variant_pattern2: EcuVariantPattern,
) -> EcuVariant:
    raw_layer = EcuVariantRaw(
        variant_type=DiagLayerType.ECU_VARIANT,
        odx_id=OdxLinkId(local_id="ecu_variant2", doc_fragments=doc_frags),
        oid=None,
        short_name="ecu_variant2",
        long_name=None,
        description=None,
        admin_data=None,
        company_datas=NamedItemList(),
        functional_classes=NamedItemList(),
        diag_data_dictionary_spec=None,
        diag_comms_raw=[ident_service, supplier_service],
        requests=NamedItemList(),
        positive_responses=NamedItemList(),
        negative_responses=NamedItemList(),
        global_negative_responses=NamedItemList(),
        import_refs=[],
        state_charts=NamedItemList(),
        additional_audiences=NamedItemList(),
        sdgs=[],
        parent_refs=[],
        comparam_refs=[],
        ecu_variant_patterns=[ecu_variant_pattern2],
        diag_variables_raw=[],
        variable_groups=NamedItemList(),
        libraries=NamedItemList(),
        dyn_defined_spec=None,
        sub_components=NamedItemList(),
    )
    result = EcuVariant(diag_layer_raw=raw_layer)
    odxlinks.update(result._build_odxlinks())
    db = Database()
    result._resolve_odxlinks(odxlinks)
    result._finalize_init(db, odxlinks)
    return result


@pytest.fixture
def ecu_variant_3(
    ident_service: DiagService,
    supplier_service: DiagService,
    ecu_variant_pattern1: EcuVariantPattern,
    ecu_variant_pattern3: EcuVariantPattern,
) -> EcuVariant:
    raw_layer = EcuVariantRaw(
        variant_type=DiagLayerType.ECU_VARIANT,
        odx_id=OdxLinkId(local_id="ecu_variant3", doc_fragments=doc_frags),
        oid=None,
        short_name="ecu_variant3",
        long_name=None,
        description=None,
        admin_data=None,
        company_datas=NamedItemList(),
        functional_classes=NamedItemList(),
        diag_data_dictionary_spec=None,
        diag_comms_raw=[ident_service, supplier_service],
        requests=NamedItemList(),
        positive_responses=NamedItemList(),
        negative_responses=NamedItemList(),
        global_negative_responses=NamedItemList(),
        import_refs=[],
        state_charts=NamedItemList(),
        additional_audiences=NamedItemList(),
        sdgs=[],
        parent_refs=[],
        comparam_refs=[],
        ecu_variant_patterns=[ecu_variant_pattern1, ecu_variant_pattern3],
        diag_variables_raw=[],
        variable_groups=NamedItemList(),
        libraries=NamedItemList(),
        dyn_defined_spec=None,
        sub_components=NamedItemList(),
    )
    result = EcuVariant(diag_layer_raw=raw_layer)
    odxlinks.update(result._build_odxlinks())
    db = Database()
    result._resolve_odxlinks(odxlinks)
    result._finalize_init(db, odxlinks)
    return result


@pytest.fixture
def ecu_variants(ecu_variant_1: EcuVariant, ecu_variant_2: EcuVariant,
                 ecu_variant_3: EcuVariant) -> List[EcuVariant]:
    return [ecu_variant_1, ecu_variant_2, ecu_variant_3]


def as_bytes(dikt: Dict[str, Any]) -> bytes:
    return bytes(json.dumps(dikt), "utf-8")


@pytest.mark.parametrize("use_cache", [True, False])
# the req_resp_mapping maps request to responses for the ecu-under-test
@pytest.mark.parametrize(
    "req_resp_mapping, expected_variant",
    [
        # test if full match of matching parameters is accepted
        (
            {
                b"\x22\x10\00": as_bytes({"id": 2000}),
                b"\x22\x20\00": as_bytes({"name": {
                    "english": "supplier_B"
                }}),
            },
            "ecu_variant2",
        ),
        # test if partial match of matching parameters is rejected
        (
            {
                b"\x22\x10\00": as_bytes({"id": 2000}),
                b"\x22\x20\00": as_bytes({"name": {
                    "english": "supplier_C"
                }}),
            },
            "ecu_variant3",
        ),
        # test if first full match is preferred over second match
        (
            {
                b"\x22\x10\00": as_bytes({"id": 1000}),
                b"\x22\x20\00": as_bytes({"name": {
                    "english": "supplier_A"
                }}),
            },
            "ecu_variant1",
        ),
    ],
)
def test_ecu_variant_matching(
    ecu_variants: List[EcuVariant],
    use_cache: bool,
    req_resp_mapping: Dict[bytes, bytes],
    expected_variant: str,
) -> None:
    matcher = EcuVariantMatcher(
        ecu_variant_candidates=ecu_variants,
        use_cache=use_cache,
    )
    for req in matcher.request_loop():
        resp = req_resp_mapping[req]
        matcher.evaluate(resp)
    assert matcher.has_match()
    assert matcher.get_active_ecu_variant().short_name == expected_variant


@pytest.mark.parametrize("use_cache", [True, False])
def test_no_match(ecu_variants: List[EcuVariant], use_cache: bool) -> None:
    # stores the responses for each request for the ecu-under-test
    req_resp_mapping = {
        b"\x22\x10\00": as_bytes({"id": 1000}),
        b"\x22\x20\00": as_bytes({"name": {
            "english": "supplier_D"
        }}),
    }

    matcher = EcuVariantMatcher(
        ecu_variant_candidates=ecu_variants,
        use_cache=use_cache,
    )
    for req in matcher.request_loop():
        resp = req_resp_mapping[req]
        matcher.evaluate(resp)
    assert not matcher.has_match()
    with pytest.raises(OdxError):
        matcher.get_active_ecu_variant()


@pytest.mark.parametrize("use_cache", [True, False])
# test if pending matchers reject the has_match() or active variant query
def test_no_request_loop(ecu_variants: List[EcuVariant], use_cache: bool) -> None:
    matcher = EcuVariantMatcher(
        ecu_variant_candidates=ecu_variants,
        use_cache=use_cache,
    )
    with pytest.raises(RuntimeError):
        matcher.has_match()
    with pytest.raises(RuntimeError):
        matcher.get_active_ecu_variant()


@pytest.mark.parametrize("use_cache", [True, False])
# test if runs of the request loop without calling `evaluate(...)` are rejected
def test_request_loop_misuse(ecu_variants: List[EcuVariant], use_cache: bool) -> None:
    matcher = EcuVariantMatcher(
        ecu_variant_candidates=ecu_variants,
        use_cache=use_cache,
    )
    with pytest.raises(RuntimeError):
        for _ in matcher.request_loop():
            pass


@pytest.mark.parametrize("use_cache", [True, False])
# test if request loop is idempotent, i.e., the matching is the same regardless of how often the request loop is run
def test_request_loop_idempotency(ecu_variants: List[EcuVariant], use_cache: bool) -> None:
    req_resp_mapping = {
        b"\x22\x10\00": as_bytes({"id": 2000}),
        b"\x22\x20\00": as_bytes({"name": {
            "english": "supplier_B"
        }}),
    }

    matcher = EcuVariantMatcher(
        ecu_variant_candidates=ecu_variants,
        use_cache=use_cache,
    )

    for req in matcher.request_loop():
        resp = req_resp_mapping[req]
        matcher.evaluate(resp)
    assert matcher.has_match()
    assert matcher.get_active_ecu_variant().short_name == "ecu_variant2"

    # second run with arbitrary input
    for _ in matcher.request_loop():
        matcher.evaluate(b"")

    # idempotency criterion
    assert matcher.has_match()
    assert matcher.get_active_ecu_variant().short_name == "ecu_variant2"


@pytest.mark.parametrize("use_cache", [True, False])
def test_unresolvable_snpathref(ecu_variants: List[EcuVariant], use_cache: bool) -> None:
    # stores the responses for each request for the ecu-under-test
    req_resp_mapping = {
        b"\x22\x10\00": as_bytes({"id": 1000}),
        # the snpathref cannot be resolved, because name is not a struct
        b"\x22\x20\00": as_bytes({"name": "supplier_C"}),
    }

    matcher = EcuVariantMatcher(
        ecu_variant_candidates=ecu_variants,
        use_cache=use_cache,
    )

    with pytest.raises(OdxError):
        for req in matcher.request_loop():
            resp = req_resp_mapping[req]
            matcher.evaluate(resp)
