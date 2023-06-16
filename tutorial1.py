import requests
import json
import psycopg2

conn = psycopg2.connect(
    database="your_database",
    user="your_user",
    password="your_password",
    host="your_host",
    port="your_port"
)
cursor = conn.cursor()

headers = {
    'Authorization': 'Bearer ATATT3xFfGF00A61eFbkerWbkKGUo2MrWD_sm7WCzjzLh0MljgPJJR-PYz0mO9cOC3iubH-wvW1nsy_0QzdRUQGxoiglrZk2ooMDKGhs_xTxFLo7DqF5uMPkwhtcvz5z4vaCUOFe-xQ4co5wWghXNlTy4rpxAms571hekMBWuQ2ylsQhr2nSJmg=E68A9F9E',
    'Content-Type': 'application/json'
}

ticket_key = 'YOUR_TICKET_KEY'
response = requests.get(f'https://jabotics.atlassian.net/rest/api/2/issue/{ticket_key}', headers=headers)

page_size = 100;
start_at = 0;
total_tickets = 0;

while True:
    response = requests.get(f'https://jabotics.atlassian.net/rest/api/2/search?jql=project=HRM_FRONTEND&startAt={start_at}&maxResults={page_size}', headers=headers)

    if response.status_code != 200:
        print(f"Error occurred: {response.json()}")
        break
    data, ticket_data = response.json()
    tickets = data['issues']
    total_tickets = data['total']

    # Parse the ticket details
    ticket_id = ticket_data['id']
    current_status = ticket_data['fields']['status']['name']

    if current_status == 'Open':
        transition_id = 'YOUR_TRANSITION_ID'
        payload = {
            'transition': {'id': transition_id}
        }
        response = requests.post(f'https://jabotics.atlassian.net/rest/api/2/issue/{ticket_key}/transitions', headers=headers, json=payload)

        # Check for errors
        if response.status_code != 204:
            print(f"Error occurred: {response.json()}")
            exit()
        else:
            print("Ticket status updated successfully.")

    comment = "Closing the ticket."
    payload = {
        'body': comment
    }
    response = requests.post(f'https://jabotics.atlassian.net/rest/api/2/issue/{ticket_key}/comment', headers=headers, json=payload)

    # Check for errors
    if response.status_code != 201:
        print(f"Error occurred: {response.json()}")
        exit()
    else:
        print("Comment added successfully.")

    for ticket in tickets:
        ticket_id = ticket['id']
        key = ticket['key']
        summary = ticket['fields']['summary']
        assignee = ticket['fields']['assignee']['name']

        cursor.execute("INSERT INTO tickets (id, key, summary, assignee) VALUES (%s, %s, %s, %s)", (ticket_id, key, summary, assignee))

        conn.commit()

    start_at += page_size
    if start_at >= total_tickets:
        break

cursor.close()
conn.close()
