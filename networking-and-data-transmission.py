import socket
import threading


class Frame:
    def __init__(self, source_mac, dest_mac, payload):
        self.source_mac = source_mac
        self.dest_mac = dest_mac
        self.payload = payload

    def __str__(self):
        return f"Frame(Source MAC: {self.source_mac}, Dest MAC: {self.dest_mac}, Payload: {self.payload})"


class OSILayer:
    def __init__(self, layer_name, role=""):
        self.layer_name = layer_name
        self.upper_layer = None
        self.lower_layer = None
        self.role = role  # Indicates whether it's client or server

    def set_upper_layer(self, layer):
        self.upper_layer = layer

    def set_lower_layer(self, layer):
        self.lower_layer = layer

    def send_data(self, data):
        print(f"{self.layer_name} ({self.role}): Sending data -> {data}")
        if self.lower_layer:
            self.lower_layer.send_data(data)

    def receive_data(self, data):
        print(f"{self.layer_name} ({self.role}): Receiving data -> {data}")
        if self.upper_layer:
            self.upper_layer.receive_data(data)


class PhysicalLayer(OSILayer):
    def send_data(self, data):
        # Real-world application: Converts digital data into electrical, radio, or optical signals for transmission.
        print(f"{self.layer_name} ({self.role}): Converting data to physical signal.")
        super().send_data(data)


class DataLinkLayer(OSILayer):
    def send_data(self, data):
        # Real-world application: Responsible for physical addressing (MAC addresses) and error detection in frames.
        source_mac = "00:11:22:33:44:55"
        dest_mac = "66:77:88:99:AA:BB"
        frame = Frame(source_mac, dest_mac, data)
        print(f"{self.layer_name} ({self.role}): Creating frame -> {frame}")
        super().send_data(frame)

    def receive_data(self, frame):
        # Real-world application: Receives frames, checks for errors, and forwards the payload to the Network Layer.
        print(f"{self.layer_name} ({self.role}): Receiving frame -> {frame}")
        if isinstance(frame, Frame):
            print(f"{self.layer_name} ({self.role}): Extracting payload -> {frame.payload}")
            super().receive_data(frame.payload)
        else:
            super().receive_data(frame)


class NetworkLayer(OSILayer):
    def send_data(self, data):
        # Real-world application: Adds IP addresses and handles routing to determine the best path for data.
        print(f"{self.layer_name} ({self.role}): Adding IP address and routing data.")
        super().send_data(data)


class TransportLayer(OSILayer):
    def send_data(self, data):
        # Real-world application: Breaks data into segments, adds port numbers, and ensures reliable delivery (e.g., TCP).
        print(f"{self.layer_name} ({self.role}): Creating segments and adding port numbers.")
        super().send_data(data)


class SessionLayer(OSILayer):
    def send_data(self, data):
        # Real-world application: Manages sessions or connections between applications (e.g., maintaining a user's session in a web app).
        print(f"{self.layer_name} ({self.role}): Managing session.")
        super().send_data(data)


class PresentationLayer(OSILayer):
    def send_data(self, data):
        # Real-world application: Translates data between the application layer and the network format, including encryption and data compression.
        print(f"{self.layer_name} ({self.role}): Encoding data for transmission.")
        super().send_data(data)


class ApplicationLayer(OSILayer):
    def send_data(self, data, protocol="HTTP"):
        # Simulating different network protocols
        if protocol == "HTTP":
            # Real-world application: HTTP is used for web browsing. This simulates an HTTP GET request.
            print(f"{self.layer_name} ({self.role}) (HTTP): Sending HTTP GET request -> {data}")
        elif protocol == "FTP":
            # Real-world application: FTP is used for transferring files. This simulates an FTP file upload.
            print(f"{self.layer_name} ({self.role}) (FTP): Uploading file -> {data}")
        elif protocol == "DNS":
            # Real-world application: DNS resolves domain names to IP addresses. This simulates a DNS query.
            print(f"{self.layer_name} ({self.role}) (DNS): Resolving domain name -> {data}")
        else:
            # Default behavior for other protocols
            print(f"{self.layer_name} ({self.role}): Sending data from application -> {data}")
        super().send_data(data)


def simulate_osi_model(data, protocol="HTTP", role="Client"):
    application_layer = ApplicationLayer("Application Layer", role=role)
    presentation_layer = PresentationLayer("Presentation Layer", role=role)
    session_layer = SessionLayer("Session Layer", role=role)
    transport_layer = TransportLayer("Transport Layer", role=role)
    network_layer = NetworkLayer("Network Layer", role=role)
    data_link_layer = DataLinkLayer("Data Link Layer", role=role)
    physical_layer = PhysicalLayer("Physical Layer", role=role)

    application_layer.set_lower_layer(presentation_layer)
    presentation_layer.set_lower_layer(session_layer)
    session_layer.set_lower_layer(transport_layer)
    transport_layer.set_lower_layer(network_layer)
    network_layer.set_lower_layer(data_link_layer)
    data_link_layer.set_lower_layer(physical_layer)

    physical_layer.set_upper_layer(data_link_layer)
    data_link_layer.set_upper_layer(network_layer)
    network_layer.set_upper_layer(transport_layer)
    transport_layer.set_upper_layer(session_layer)
    session_layer.set_upper_layer(presentation_layer)
    presentation_layer.set_upper_layer(application_layer)

    application_layer.send_data(data, protocol)


# Integrating TCP/IP and protocols into the OSI model
def tcp_ip_with_osi_and_protocol_demo():
    def start_server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8080))
        server_socket.listen(1)
        print("Server is listening on port 8080...")

        conn, addr = server_socket.accept()
        print(f"Server: Connection established with {addr}")

        # Simulate receiving data through OSI layers
        received_data = conn.recv(1024).decode()
        print(f"Server: Received from client: {received_data}")
        simulate_osi_model(received_data, protocol="HTTP", role="Server")  # Simulate OSI layers processing the data

        # Respond back using a different protocol for demonstration
        response = "Hello from the server (via FTP)!"
        conn.sendall(response.encode())

        simulate_osi_model(response, protocol="FTP", role="Server")  # Simulate OSI layers processing the response
        conn.close()

    def start_client():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))

        # Simulate sending data through OSI layers with DNS protocol
        data = "www.example.com"
        simulate_osi_model(data, protocol="DNS", role="Client")  # Simulate OSI layers processing the DNS request
        client_socket.sendall(data.encode())

        # Receive and process the server response through OSI layers
        response = client_socket.recv(1024).decode()
        simulate_osi_model(response, protocol="FTP",
                           role="Client")  # Simulate OSI layers processing the response via FTP

        print(f"Client: Received from server: {response}")
        client_socket.close()

    # Running both server and client to demonstrate TCP/IP with OSI and protocols
    print("Starting TCP/IP with OSI model and protocols demo...")

    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Start client after server starts
    client_thread = threading.Thread(target=start_client)
    client_thread.start()

    # Wait for both threads to finish
    server_thread.join()
    client_thread.join()


# Run the TCP/IP with OSI model and protocols simulation
tcp_ip_with_osi_and_protocol_demo()

