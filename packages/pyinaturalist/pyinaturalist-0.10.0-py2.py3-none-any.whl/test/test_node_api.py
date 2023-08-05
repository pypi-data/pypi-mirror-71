import pytest
from urllib.parse import urlencode, urljoin
from unittest.mock import patch

import pyinaturalist
from pyinaturalist.constants import INAT_NODE_API_BASE_URL
from pyinaturalist.node_api import (
    get_observation,
    get_geojson_observations,
    get_taxa,
    get_taxa_by_id,
    get_taxa_autocomplete,
)
from pyinaturalist.exceptions import ObservationNotFound
from pyinaturalist.rest_api import get_access_token
from test.conftest import load_sample_data

PAGE_1_JSON_RESPONSE = load_sample_data("get_observation_fields_page1.json")
PAGE_2_JSON_RESPONSE = load_sample_data("get_observation_fields_page2.json")


def get_observations_response(response_format):
    response_format = response_format.replace("widget", "js")
    return str(load_sample_data("get_observations.{}".format(response_format)))


def test_get_observation(requests_mock):
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "observations"),
        json=load_sample_data("get_observation.json"),
        status_code=200,
    )

    obs_data = get_observation(observation_id=16227955)
    assert obs_data["quality_grade"] == "research"
    assert obs_data["id"] == 16227955
    assert obs_data["user"]["login"] == "niconoe"
    assert len(obs_data["photos"]) == 2


def test_get_geojson_observations(requests_mock):
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "observations"),
        json=load_sample_data("get_observation.json"),
        status_code=200,
    )

    geojson = get_geojson_observations(observation_id=16227955)
    feature = geojson["features"][0]
    assert feature["geometry"]["coordinates"] == [4.360086, 50.646894]
    assert feature["properties"]["id"] == 16227955
    assert feature["properties"]["taxon_id"] == 493595


def test_get_geojson_observations__custom_properties(requests_mock):
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "observations"),
        json=load_sample_data("get_observation.json"),
        status_code=200,
    )

    properties = ["taxon_name", "taxon_rank"]
    geojson = get_geojson_observations(observation_id=16227955, properties=properties)
    print(geojson)
    feature = geojson["features"][0]
    assert feature["properties"]["taxon_name"] == "Lixus bardanae"
    assert feature["properties"]["taxon_rank"] == "species"
    assert "id" not in feature["properties"] and "taxon_id" not in feature["properties"]


def test_get_non_existent_observation(requests_mock):
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "observations"),
        json=load_sample_data("get_nonexistent_observation.json"),
        status_code=200,
    )
    with pytest.raises(ObservationNotFound):
        get_observation(observation_id=99999999)


def test_get_taxa(requests_mock):
    params = urlencode({"q": "vespi", "rank": "genus,subgenus,species"})
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "taxa?" + params),
        json=load_sample_data("get_taxa.json"),
        status_code=200,
    )

    response = get_taxa(q="vespi", rank=["genus", "subgenus", "species"])
    first_result = response["results"][0]

    assert len(response["results"]) == 30
    assert response["total_results"] == 35
    assert first_result["id"] == 70118
    assert first_result["name"] == "Nicrophorus vespilloides"
    assert first_result["rank"] == "species"
    assert first_result["is_active"] is True
    assert len(first_result["ancestor_ids"]) == 14


CLASS_AND_HIGHER = ["class", "superclass", "subphylum", "phylum", "kingdom"]
SPECIES_AND_LOWER = ["form", "variety", "subspecies", "hybrid", "species"]
CLASS_THOUGH_PHYLUM = ["class", "superclass", "subphylum", "phylum"]


@pytest.mark.parametrize(
    "params, expected_ranks",
    [
        ({"rank": "genus"}, "genus"),
        ({"min_rank": "class"}, CLASS_AND_HIGHER),
        ({"max_rank": "species"}, SPECIES_AND_LOWER),
        ({"min_rank": "class", "max_rank": "phylum"}, CLASS_THOUGH_PHYLUM),
        ({"max_rank": "species", "rank": "override_me"}, SPECIES_AND_LOWER),
    ],
)
@patch("pyinaturalist.node_api.make_inaturalist_api_get_call")
def test_get_taxa_by_rank_range(
    mock_inaturalist_api_get_call, params, expected_ranks,
):
    # Make sure custom rank params result in the correct 'rank' param value
    get_taxa(**params)
    mock_inaturalist_api_get_call.assert_called_with(
        "taxa", {"rank": expected_ranks}, user_agent=None
    )


# This is just a spot test of a case in which boolean params should be converted
@patch("pyinaturalist.api_requests.requests.request")
def test_get_taxa_by_name_and_is_active(request):
    get_taxa(q="Lixus bardanae", is_active=False)
    request_kwargs = request.call_args[1]
    assert request_kwargs["params"] == {"q": "Lixus bardanae", "is_active": "false"}


def test_get_taxa_by_id(requests_mock):
    taxon_id = 70118
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "taxa/" + str(taxon_id)),
        json=load_sample_data("get_taxa_by_id.json"),
        status_code=200,
    )

    response = get_taxa_by_id(taxon_id)
    result = response["results"][0]
    assert len(response["results"]) == 1
    assert result["id"] == taxon_id
    assert result["name"] == "Nicrophorus vespilloides"
    assert result["rank"] == "species"
    assert result["is_active"] is True
    assert len(result["ancestors"]) == 12

    with pytest.raises(ValueError):
        get_taxa_by_id([1, 2])


def test_get_taxa_autocomplete(requests_mock):
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "taxa/autocomplete"),
        json=load_sample_data("get_taxa_autocomplete.json"),
        status_code=200,
    )

    response = get_taxa_autocomplete(q="vespi")
    first_result = response["results"][0]

    assert len(response["results"]) == 10
    assert response["total_results"] == 44
    assert first_result["matched_term"] == "Vespidae"
    assert first_result["id"] == 52747
    assert first_result["name"] == "Vespidae"
    assert first_result["rank"] == "family"
    assert first_result["is_active"] is True
    assert len(first_result["ancestor_ids"]) == 11


# Test usage of format_taxon() with get_taxa_autocomplete()
def test_get_taxa_autocomplete_minified(requests_mock):
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "taxa/autocomplete"),
        json=load_sample_data("get_taxa_autocomplete.json"),
        status_code=200,
    )

    expected_results = [
        "   52747:       Family Vespidae (Hornets, Paper Wasps, Potter Wasps, and Allies)",
        "   84738:    Subfamily Vespinae (Hornets and Yellowjackets)",
        "  131878:      Species Nicrophorus vespillo (Vespillo Burying Beetle)",
        "  495392:      Species Vespidae st1",
        "   70118:      Species Nicrophorus vespilloides (Lesser Vespillo Burying Beetle)",
        "   84737:        Genus Vespina",
        "  621584:      Species Vespicula cypho",
        "  621585:      Species Vespicula trachinoides",
        "  621586:      Species Vespicula zollingeri",
        "  299443:      Species Vespita woolleyi",
    ]

    response = get_taxa_autocomplete(q="vespi", minify=True)
    assert response["results"] == expected_results


def test_user_agent(requests_mock):
    # TODO: test for all functions that access the inaturalist API?
    requests_mock.get(
        urljoin(INAT_NODE_API_BASE_URL, "observations"),
        json=load_sample_data("get_observation.json"),
        status_code=200,
    )
    accepted_json = {
        "access_token": "604e5df329b98eecd22bb0a84f88b68a075a023ac437f2317b02f3a9ba414a08",
        "token_type": "Bearer",
        "scope": "write",
        "created_at": 1539352135,
    }
    requests_mock.post(
        "https://www.inaturalist.org/oauth/token", json=accepted_json, status_code=200,
    )

    default_ua = "Pyinaturalist/{v}".format(v=pyinaturalist.__version__)

    # By default, we have a 'Pyinaturalist' user agent:
    get_observation(observation_id=16227955)
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == default_ua
    get_access_token("valid_username", "valid_password", "valid_app_id", "valid_app_secret")
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == default_ua

    # But if the user sets a custom one, it is indeed used:
    get_observation(observation_id=16227955, user_agent="CustomUA")
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "CustomUA"
    get_access_token(
        "valid_username",
        "valid_password",
        "valid_app_id",
        "valid_app_secret",
        user_agent="CustomUA",
    )
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "CustomUA"

    # We can also set it globally:
    pyinaturalist.user_agent = "GlobalUA"
    get_observation(observation_id=16227955)
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "GlobalUA"
    get_access_token("valid_username", "valid_password", "valid_app_id", "valid_app_secret")
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "GlobalUA"

    # And it persists across requests:
    get_observation(observation_id=16227955)
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "GlobalUA"
    get_access_token("valid_username", "valid_password", "valid_app_id", "valid_app_secret")
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "GlobalUA"

    # But if we have a global and local one, the local has priority
    get_observation(observation_id=16227955, user_agent="CustomUA 2")
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "CustomUA 2"
    get_access_token(
        "valid_username",
        "valid_password",
        "valid_app_id",
        "valid_app_secret",
        user_agent="CustomUA 2",
    )
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == "CustomUA 2"

    # We can reset the global settings to the default:
    pyinaturalist.user_agent = pyinaturalist.DEFAULT_USER_AGENT
    get_observation(observation_id=16227955)
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == default_ua
    get_access_token("valid_username", "valid_password", "valid_app_id", "valid_app_secret")
    assert requests_mock._adapter.last_request._request.headers["User-Agent"] == default_ua
