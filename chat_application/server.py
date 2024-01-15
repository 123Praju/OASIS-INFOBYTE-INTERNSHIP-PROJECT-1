import socket
import threading

HOST = '127.0.0.1'
PORT = 123
LISTENER_LIMIT = 5
active_clients=[]

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(300).decode('utf-8')
            if message != '':
                final_msg = username + '~' + message
                send_message_to_all(final_msg)
            else:
                print(f"Message sent from client {username} is empty")
        except Exception as e:
            print(f"Error in listen_for_messages: {e}")
            break

def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error in send_message_to_client: {e}")

def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client):
    while True:
        try:
            username = client.recv(300).decode('utf-8')
            if username != '':
                active_clients.append((username, client))
                prompt_message = "SERVER~" + f"{username} added to the chat."
                send_message_to_all(prompt_message)
                break
            else:
                print("Client username is empty")
        except Exception as e:
            print(f"Error in client_handler: {e}")
            break

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind host {HOST} and port {PORT}: {e}")

    server.listen(LISTENER_LIMIT)

    while True:
        try:
            client, address = server.accept()
            print(f"Successfully connected to client {address[0]} {address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()
        except Exception as e:
            print(f"Error in main: {e}")

if __name__ == '__main__':
    main()
