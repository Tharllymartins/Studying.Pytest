import requests
import pytest
from model.deck import DeckModel


url = "https://www.deckofcardsapi.com"


@pytest.fixture(scope="session")
def deck_data():
    response = requests.post(f"{url}/api/deck/new/shuffle/?deck_count=1")
    response_json = response.json()
    deck = DeckModel(
        deck_id= response_json["deck_id"],
        remaining= response_json["remaining"],
        shuffled= response_json["shuffled"],
        success= response_json["success"]
    )
    
    return deck


def test_draw_a_cart_from_a_deck(deck_data: DeckModel):
    deck_id = deck_data.deck_id
    
    # Recebe o valor da propriedade remaining antes de realizar a requisição que remove uma carta
    remaining_cards_before_request = deck_data.remaining
    
    response = requests.post(f"{url}/api/deck/{deck_id}/draw/?count=1")
    
    # Recebe o valor da propriedade remaining depois de realizar a requisição que remove uma carta
    remaining_cards_after_request = response.json()["remaining"]
    
    #Compara se o valor da propriedade remaining diminiu
    remaining_cards_has_decreased = remaining_cards_after_request == (remaining_cards_before_request - 1)
    
    status_code_is_ok = response.status_code in [200, 201]
    
    print("\nDraw a cart from the deck")
    
    assert status_code_is_ok
    if status_code_is_ok: print("\nStatus code is ok")
    assert remaining_cards_has_decreased
    if remaining_cards_has_decreased: print("Remainig cards has decreased")
    
    
def test_reshuffle_cards_from_a_deck(deck_data: DeckModel):
    deck_id = deck_data.deck_id

    response = requests.post(f"{url}/api/deck/{deck_id}/shuffle/")
    
    deck_shuffled = response.json()["shuffled"]
        
    status_code_is_ok = response.status_code in [200, 201]
    
    print("Reshuffle cards from the deck")
    
    if status_code_is_ok: print("\nStatus code is ok")
    assert status_code_is_ok
    if deck_shuffled: print("Deck reshuffled!")
    assert deck_shuffled
    

def test_get_a_brand_new_deck(deck_data: DeckModel):
    old_deck_id = deck_data.deck_id
    
    response = requests.post(f"{url}/api/deck/new/")
    
    new_deck_id = response.json()["deck_id"]
    
    new_deck_created = old_deck_id != new_deck_id
    
    status_code_is_ok = response.status_code in [200, 201]
    
    print("Get a brand new deck")
    
    if new_deck_created: print("\nNew deck created")
    assert new_deck_created
    if status_code_is_ok: print("Status code is ok")
    assert status_code_is_ok
    

# def test_create_a_pile(deck_data):
#     deck_id = deck_data["deck_id"]
    
#     pile_name = "teste"
    
#     response = requests.post(f"{url}/api/deck/{deck_id}/pile/{pile_name}/add/?cards=AS")
    
#     status_code_is_ok = response.status_code in [200, 201]
    
#     print(response.json())
