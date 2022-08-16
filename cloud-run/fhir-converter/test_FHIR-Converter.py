# flake8: noqa
from unittest import mock
from fastapi.testclient import TestClient

from main import api

client = TestClient(api)

valid_request = {
    "input_data": "VALID_INPUT_DATA",
    "input_type": "hl7v2",
    "root_template": "ADT_A01",
}

valid_response = {
    "Status": "OK",
    "FhirResource": {
        "resourceType": "Bundle",
        "type": "batch",
        "timestamp": "1989-08-18T11:26:00+02:15",
        "identifier": {"value": "MSG00001"},
        "id": "513a3d06-5e87-6fbc-ad1b-170ab430499f",
        "entry": [{"resource": "FHIR_RESOURCE"}],
    },
}

missing_input_data_request = {"input_type": "hl7v2", "root_template": "ADT_A01"}

missing_input_data_response = {
    "detail": [
        {
            "loc": ["body", "input_data"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}

invalid_input_type_request = {
    "input_data": "VALID_INPUT_DATA",
    "input_type": "hl7v3",
    "root_template": "ADT_A01",
}

invalid_input_type_response = {
    "detail": [
        {
            "loc": ["body", "input_type"],
            "msg": "value is not a valid enumeration member; permitted: 'hl7v2', 'ccda'",
            "type": "type_error.enum",
            "ctx": {"enum_values": ["hl7v2", "ccda"]},
        }
    ]
}

invalid_root_template_request = {
    "input_data": "VALID_INPUT_DATA",
    "input_type": "hl7v2",
    "root_template": "INVALID_ROOT_TEMPLATE",
}

invalid_root_template_response = {
    "detail": [
        {
            "loc": ["body", "root_template"],
            "msg": "value is not a valid enumeration member; permitted: 'ADT_A01', 'ADT_A02', 'ADT_A03', 'ADT_A04', 'ADT_A05', 'ADT_A06', 'ADT_A07', 'ADT_A08', 'ADT_A09', 'ADT_A10', 'ADT_A11', 'ADT_A13', 'ADT_A14', 'ADT_A15', 'ADT_A16', 'ADT_A25', 'ADT_A26', 'ADT_A27', 'ADT_A28', 'ADT_A29', 'ADT_A31', 'ADT_A40', 'ADT_A41', 'ADT_A45', 'ADT_A47', 'ADT_A60', 'BAR_P01', 'BAR_P02', 'BAR_P12', 'DFT_P03', 'DFT_P11', 'MDM_T01', 'MDM_T02', 'MDM_T05', 'MDM_T06', 'MDM_T09', 'MDM_T10', 'OMG_O19', 'OML_O21', 'ORM_O01', 'ORU_R01', 'OUL_R22', 'OUL_R23', 'OUL_R24', 'RDE_O11', 'RDE_O25', 'RDS_O13', 'REF_I12', 'REF_I14', 'SIU_S12', 'SIU_S13', 'SIU_S14', 'SIU_S15', 'SIU_S16', 'SIU_S17', 'SIU_S26', 'VXU_V04', 'CCD', 'ConsultationNote', 'DischargeSummary', 'Header', 'HistoryandPhysical', 'OperativeNote', 'ProcedureNote', 'ProgressNote', 'ReferralNote', 'TransferSummary'",
            "type": "type_error.enum",
            "ctx": {
                "enum_values": [
                    "ADT_A01",
                    "ADT_A02",
                    "ADT_A03",
                    "ADT_A04",
                    "ADT_A05",
                    "ADT_A06",
                    "ADT_A07",
                    "ADT_A08",
                    "ADT_A09",
                    "ADT_A10",
                    "ADT_A11",
                    "ADT_A13",
                    "ADT_A14",
                    "ADT_A15",
                    "ADT_A16",
                    "ADT_A25",
                    "ADT_A26",
                    "ADT_A27",
                    "ADT_A28",
                    "ADT_A29",
                    "ADT_A31",
                    "ADT_A40",
                    "ADT_A41",
                    "ADT_A45",
                    "ADT_A47",
                    "ADT_A60",
                    "BAR_P01",
                    "BAR_P02",
                    "BAR_P12",
                    "DFT_P03",
                    "DFT_P11",
                    "MDM_T01",
                    "MDM_T02",
                    "MDM_T05",
                    "MDM_T06",
                    "MDM_T09",
                    "MDM_T10",
                    "OMG_O19",
                    "OML_O21",
                    "ORM_O01",
                    "ORU_R01",
                    "OUL_R22",
                    "OUL_R23",
                    "OUL_R24",
                    "RDE_O11",
                    "RDE_O25",
                    "RDS_O13",
                    "REF_I12",
                    "REF_I14",
                    "SIU_S12",
                    "SIU_S13",
                    "SIU_S14",
                    "SIU_S15",
                    "SIU_S16",
                    "SIU_S17",
                    "SIU_S26",
                    "VXU_V04",
                    "CCD",
                    "ConsultationNote",
                    "DischargeSummary",
                    "Header",
                    "HistoryandPhysical",
                    "OperativeNote",
                    "ProcedureNote",
                    "ProgressNote",
                    "ReferralNote",
                    "TransferSummary",
                ]
            },
        }
    ]
}


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


@mock.patch("main.json.load")
@mock.patch("main.open")
@mock.patch("main.subprocess.run")
def test_convert_valid_request(patched_subprocess_run, patched_open, patched_json_load):
    patched_subprocess_run.return_value = mock.Mock(returncode=0)
    patched_json_load.return_value = valid_response
    response = client.post(
        "/convert-to-fhir",
        json=valid_request,
    )
    assert response.status_code == 200
    assert response.json() == valid_response


@mock.patch("main.subprocess.run")
def test_convert_missing_input_data(patched_subprocess_run):
    patched_subprocess_run.return_value = mock.Mock(returncode=1)
    response = client.post(
        "/convert-to-fhir",
        json=missing_input_data_request,
    )
    assert response.status_code == 422
    assert response.json() == missing_input_data_response


@mock.patch("main.subprocess.run")
def test_convert_invalid_input_type(patched_subprocess_run):
    patched_subprocess_run.return_value = mock.Mock(returncode=1)
    response = client.post(
        "/convert-to-fhir",
        json=invalid_input_type_request,
    )
    assert response.status_code == 422
    assert response.json() == invalid_input_type_response


@mock.patch("main.subprocess.run")
def test_convert_invalid_root_template(patched_subprocess_run):
    patched_subprocess_run.return_value = mock.Mock(returncode=1)
    response = client.post(
        "/convert-to-fhir",
        json=invalid_root_template_request,
    )
    assert response.status_code == 422
    assert response.json() == invalid_root_template_response