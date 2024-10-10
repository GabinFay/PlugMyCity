import streamlit as st
from web3 import Web3
import json

# Get the user address from the URL parameter
user_address = st.query_params.get("address", [""])[0]

if not user_address:
    st.error("Please connect your MetaMask wallet first.")
    st.markdown("[Connect MetaMask](http://100.115.92.202/index.php)")
    st.stop()

# Connect to your Avalanche L1 blockchain
w3 = Web3(Web3.HTTPProvider("https://upgraded-capybara-jqvrj5vxg9jcqxj7-9650.app.github.dev/ext/bc/finalblockchain/rpc"))

# Load the contract ABI and address
with open("../house-craftsman-platform/artifacts/contracts/HouseCraftsmanPlatform.sol/HouseCraftsmanPlatform.json") as f:
    contract_json = json.load(f)
contract_abi = contract_json["abi"]
contract_address = "0x4Ac1d98D9cEF99EC6546dEd4Bd550b0b287aaD6D"  # Replace with your deployed contract address

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def get_houses(address):
    house_ids = contract.functions.getHousesByOwner(address).call()
    houses = []
    for house_id in house_ids:
        house = contract.functions.houses(house_id).call()
        houses.append({"id": house_id, "details": house[1]})
    return houses

def create_house(details):
    nonce = w3.eth.get_transaction_count(user_address)
    txn = contract.functions.createHouse(details).build_transaction({
        'from': user_address,
        'nonce': nonce,
    })
    # Here you would typically sign the transaction with the user's private key
    # For demo purposes, we'll use a funded account
    private_key = "56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027"
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

# Helper function to send a transaction
def send_transaction(function, *args):
    nonce = w3.eth.get_transaction_count(user_address)
    txn = function(*args).build_transaction({
        'from': user_address,
        'nonce': nonce,
    })
    private_key = "56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027"
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

# Helper function to send a transaction with value
def send_transaction_with_value(function, value, *args):
    nonce = w3.eth.get_transaction_count(user_address)
    txn = function(*args).build_transaction({
        'from': user_address,
        'nonce': nonce,
        'value': value,
    })
    private_key = "56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027"
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

st.title("House Craftsman Platform")

# Display user's address
st.write(f"Connected address: {user_address}")

# Display user's houses
st.header("Your Houses")
houses = get_houses(user_address)
for house in houses:
    st.write(f"House ID: {house['id']}, Details: {house['details']}")

# Add new house form
st.header("Add New House")
with st.form(key="new_house_form"):
    annee_construction = st.number_input("Année de construction", min_value=1800, max_value=2024, step=1)
    superficie_terrain = st.number_input("Superficie terrain (en m²)", min_value=1, step=1)
    nombre_pieces = st.number_input("Nombre de pièces", min_value=1, step=1)
    superficie_habitable = st.number_input("Superficie habitable (en m²)", min_value=1, step=1)
    annee_acquisition = st.number_input("Année d'acquisition", min_value=1800, max_value=2024, step=1)
    montant_acquisition = st.number_input("Montant d'acquisition (€)", min_value=1.0, step=1000.0)
    type_achat = st.selectbox("Type d'achat", ["Neuf", "Ancien", "Investissement", "Résidence principale"])

    submit_button = st.form_submit_button(label="Create House NFT")

if submit_button:
    details = f"Construction: {annee_construction}, Terrain: {superficie_terrain}m², Pièces: {nombre_pieces}, Habitable: {superficie_habitable}m², Acquisition: {annee_acquisition}, Montant: {montant_acquisition}€, Type: {type_achat}"
    tx_receipt = create_house(details)
    st.success(f"House NFT created! Transaction hash: {tx_receipt.transactionHash.hex()}")
    st.experimental_rerun()

# Escrow functionality
st.header("Escrow System")
house_id = st.selectbox("Select House", [house['id'] for house in houses])
craftsman_address = st.text_input("Craftsman Address")
craftsman_field = st.text_input("Craftsman Field")
quotation_amount = st.number_input("Quotation Amount (in wei)", min_value=1, step=1)

if st.button("Request Craftsman"):
    try:
        tx_receipt = send_transaction(contract.functions.requestCraftsman, house_id, craftsman_field)
        st.success(f"Craftsman requested! Transaction hash: {tx_receipt.transactionHash.hex()}")
    except Exception as e:
        st.error(f"Error requesting craftsman: {str(e)}")

if st.button("Make Quotation"):
    try:
        tx_receipt = send_transaction(contract.functions.makeQuotation, house_id, quotation_amount)
        st.success(f"Quotation made! Transaction hash: {tx_receipt.transactionHash.hex()}")
    except Exception as e:
        st.error(f"Error making quotation: {str(e)}")

if st.button("Accept Quotation"):
    try:
        tx_receipt = send_transaction_with_value(contract.functions.acceptQuotation, quotation_amount, house_id)
        st.success(f"Quotation accepted! Transaction hash: {tx_receipt.transactionHash.hex()}")
    except Exception as e:
        st.error(f"Error accepting quotation: {str(e)}")

if st.button("Complete Work"):
    try:
        tx_receipt = send_transaction(contract.functions.completeWork, house_id)
        st.success(f"Work completed! Transaction hash: {tx_receipt.transactionHash.hex()}")
    except Exception as e:
        st.error(f"Error completing work: {str(e)}")

if st.button("Release Payment"):
    try:
        tx_receipt = send_transaction(contract.functions.releasePayment, house_id)
        st.success(f"Payment released! Transaction hash: {tx_receipt.transactionHash.hex()}")
    except Exception as e:
        st.error(f"Error releasing payment: {str(e)}")