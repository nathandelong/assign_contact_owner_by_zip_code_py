import os
import requests
from hubspot import HubSpot
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException

#Created 5/17/2023 by Nathan De Long at HubSpot (with help from ChatGPT). The below code is provided as-is, with no guarantees. Please test before implementing in a live environment!

def main(event):
    contact_record_id = event.get('inputFields').get('contact_record_id')
    zip_code = event.get('inputFields').get('zip_code')
    base_url = 'https://api.hubapi.com'
    #insert the name of your private app access token below.
    bearer_token = os.getenv('hstoken')
    
    client = hubspot.Client.create(access_token=f"{bearer_token}")
    
    def assign_sales_rep(zip_code):
        # NOTE: replace IDs below and comments with IDs / names of contact owners from your portal.
        sales_rep_map = {
            "49555": "176076815",  # Nathan De Long
            "90002": "182666829",  # Edward Seller
            "90003": "187827890"  # Liz Rosso
            # Add more zip code - sales rep mappings as needed
        }
    
        # Check if the zip code exists in the mapping
        if zip_code in sales_rep_map:
            sales_rep = sales_rep_map[zip_code]
            print(f'The zip code for contact ID {contact_record_id} is {zip_code}. The correct contact owner to assign is {sales_rep}.')
            return sales_rep
        else:
            return None

    def assign_sales_rep_to_contact(contact_record_id, sales_rep):
      hubspot = HubSpot(access_token=bearer_token)
      
      properties = {
          "hubspot_owner_id": f"{sales_rep}"
        }
      
      simple_public_object_input = SimplePublicObjectInput(properties=properties)
      
      try:
        
        response = client.crm.contacts.basic_api.update(contact_id=f"{contact_record_id}", simple_public_object_input=simple_public_object_input)
        
        if response:
          print(f"Sales rep ID '{sales_rep}' assigned to contact with ID {contact_record_id}")
        else:
          print(f"Failed to assign sales representative to contact.")
          
      except ApiException as e:
                print(f"Exception when calling HubSpot API: {e}")

	# Assign sales rep to the contact
    sales_rep = assign_sales_rep(zip_code)
    if sales_rep:
      assign_sales_rep_to_contact(contact_record_id, sales_rep)

        # Return the output data that can be used in later actions in your workflow.
    return {
        "outputFields": {}
    }
