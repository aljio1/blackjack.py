import json
import requests

# Ask for inputs such as name and deck count.
name = input("Please enter your name:")
dc = input("How many decks would you like?")

print("Welcome " + name + " lets play blackjack, we will be playing with " + dc + " decks.")

# Shuffle the deck
url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=" + str(dc)

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

deckJson = response.json()

id = deckJson['deck_id']

print("The cards have been shuffled for you " + name + ", and your deck id is: " + id)

# Deal two cards to the player
url = "https://deckofcardsapi.com/api/deck/" + str(id) + "/draw/?count=2"

payload = {}
headers = {}

drawresponse = requests.request("GET", url, headers=headers, data=payload)

handJson = drawresponse.json()

cards = handJson['cards']

print("Your cards are: " + str(cards))

# Calculate the value of the player's hand
value = 0

for card in cards:
  if card['value'].isdigit():
    value += int(card['value'])
  else:
    if card['value'] == 'JACK':
      value += 10
    elif card['value'] == 'QUEEN':
      value += 10
    elif card['value'] == 'KING':
      value += 10
    else:
      value += 11

def card_value(card):
   """Returns the value of a card"""
   if card['value'] == 'ACE':
     return 11
   elif card['value'] in ['kING', 'QUEEN', 'JACK']:
     return 10
   else:
     return int(card['value'])

print("The value of your hand is " + str(value))

# Ask the player if they want to hit or stand

while True:
  choice = input("Do you want to [H]it or [S]tand? ").lower()

  if choice == "h":
    # Deal another card to the player
    url = "https://deckofcardsapi.com/api/deck/" + str(id) + "/draw/?count=1"

    payload = {}
    headers = {}

    drawresponse = requests.request("GET", url, headers=headers, data=payload)

    handJson = drawresponse.json()

    card = handJson['cards'][0]

    print("You drew a " + str(card))

    value += card_value(card)

    #Update the players hand with the hit card
    cards.append(card)

    print("The value of your hand is now " + str(value))

  elif choice == "s":
    break

  else:
    print("Invalid choice. Please enter H or S.")

# Check if the player has won or lost

if value > 21:
  print("You bust! Sorry better luck next time.")
elif value == 21:
  print("Blackjack! You win!")
else:
  print("You lose.")
