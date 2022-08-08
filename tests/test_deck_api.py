import requests
import pytest


@pytest.fixture(scope="session")
def deck_data():
    response = requests.post("http://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    
    return response.json()


def test_draw_a_cart_from_a_deck(deck_data):
    deck_id = deck_data["deck_id"]
    
    # Recebe o valor da propriedade remaining antes de realizar a requisição que remove uma carta
    remaining_cards_before_request = deck_data["remaining"]
    
    response = requests.post(f"http://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")
    
    # Recebe o valor da propriedade remaining depois de realizar a requisição que remove uma carta
    remaining_cards_after_request = response.json()["remaining"]
    
    #Compara se o valor da propriedade remaining diminiu
    remaining_cards_has_decreased = remaining_cards_after_request == (remaining_cards_before_request - 1)
    
    status_code_is_ok = response.status_code in [200, 201]
    
    assert status_code_is_ok
    if status_code_is_ok: print("\nStatus code is ok")
    assert remaining_cards_has_decreased
    if remaining_cards_has_decreased: print("Remainig cards has decreased")
    
    
def test_reshuffle_cards_from_a_deck(deck_data):
    deck_id = deck_data["deck_id"]
    
    response = requests.post(f"http://deckofcardsapi.com/api/deck/{deck_id}/shuffle/")
    
    status_code_is_ok = response.status_code in [200, 201]
    
    if status_code_is_ok: print("\nStatus code is ok")
    assert status_code_is_ok
