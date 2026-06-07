import socket
import numpy as np


class TcpClientModel:
    """
    Simple TCP client model for receiving EMG data.

    Expected server data:
    - 32 channels
    - 18 samples per packet
    - float64 values
    - raw bytes sent with current_window.tobytes()

    The model stores a rolling 10-second buffer.
    Older samples are removed when new samples arrive.
    """

    def __init__(
        self,
        host,
        port,
        sampling_rate,
        channels,
        samples_per_packet,
        window_seconds,
        selected_channel,
    ):
        self.host = host
        self.port = port
        self.sampling_rate = sampling_rate
        self.channels = channels
        self.samples_per_packet = samples_per_packet
        self.window_seconds = window_seconds
        self.selected_channel = selected_channel

        # IMPORTANT:
        # This must match the dtype used by the server before calling .tobytes().
        self.dtype = np.float64

        self.socket = None
        self.is_connected = False

        self.packet_size = self.channels * self.samples_per_packet
        self.packet_size_bytes = self.packet_size * np.dtype(self.dtype).itemsize

        self.window_size = int(self.sampling_rate * self.window_seconds)

        self.byte_buffer = bytearray() #we ccollect all received bytes here
        self.data_buffer = np.empty((self.channels, 0), dtype=self.dtype)

        self.total_samples_received = 0

    def connect(self):
        """
        Connect to the TCP server.

        TODO:
        1. If the client is already connected, return immediately.
        2. Create a TCP socket.
        3. Connect the socket to self.host and self.port.
        4. Set the socket to non-blocking mode.
        5. Set self.is_connected to True.
        """
        if self.is_connected:
            return
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.host, self.port)
        self.socket.setblocking(False)
        self.is_connected = True

    def disconnect(self):
        """
        Close the TCP connection.

        TODO:
        1. Set self.is_connected to False.
        2. If self.socket is not None:
           - close the socket
           - set self.socket to None
        """
        self.is_connected = False
        if self.socket is not None:
            self.socket.close()
            self.socket = None


    def receive_data(self):
        """
        Receive all currently available TCP data.

        TCP is a byte stream. This means one recv() call does not necessarily
        contain exactly one packet.

        Therefore:
        1. receive raw bytes
        2. add them to self.byte_buffer
        3. extract complete packets from self.byte_buffer
        """
        if not self.is_connected or self.socket is None:
            return

        while True:
            try:
                # TODO:
                # Receive up to one packet of bytes from the socket.
                # One packet contains:
                # channels * samples_per_packet * bytes_per_value bytes.
                # for this exercise:
                # self.packet_size_bytes = 4608
                # because one EMG packet contains 4608 bytes.
                new_bytes = self.socket.recv(self.packet_size_bytes)

                if not new_bytes: #this means if recv returned empty bytes
                    self.disconnect()
                    return
                # Why would recv() return empty bytes?
                # For a TCP socket, this usually means:the other side closed the connection
                # So if the server disconnects, your client may receive:
                # new_bytes = b"" --> and then this if code runs
                # MEANING: The server closed the connection.
                # So the client should clean up too.
            

                # TODO:
                # Add the newly received bytes to self.byte_buffer.
                self.byte_buffer.extend(new_bytes)

            except BlockingIOError:
                # No more data is available right now.
                break

        self._extract_packets_from_buffer()

    def _extract_packets_from_buffer(self):
        """
        Convert complete byte packets into NumPy arrays.


        One complete packet contains:

            channels * samples_per_packet

        values.

        For this exercise:

            32 * 18 = 576 values

        Since the values are float64, one value needs 8 bytes:

            576 * 8 = 4608 bytes per packet
        """
        #he full idea is:
        #bytes -> NumPy array -> reshape to 32 x 18 -> add to packet list
        packets = []

        while len(self.byte_buffer) >= self.packet_size_bytes:
            # TODO:
            # Take one complete packet from the beginning of self.byte_buffer.
            packet_bytes = self.byte_buffer[:self.packet_size_bytes]

            # TODO:
            # Delete those bytes from self.byte_buffer,
            # because they are now being processed.
            del self.byte_buffer[:self.packet_size_bytes]

            # TODO:
            # Convert packet_bytes into a NumPy array.
            # Hint:
            # np.frombuffer(..., dtype=self.dtype)
            packet = np.frombuffer(packet_bytes,dtype=self.dtype)

            # TODO:
            # Reshape the packet into:
            # channels x samples_per_packet
            packet = packet.reshape(self.channels, self.samples_per_packet)

            # TODO:
            # Add the packet to the list of packets.
            packet.append(packet)

        if len(packets) == 0:
            return

        # Combine all new packets into one larger data block.
        new_data = np.concatenate(packets, axis=1)

        # Add the new data to the existing data buffer.
        self.data_buffer = np.concatenate(
            (self.data_buffer, new_data),
            axis=1,
        )

        # Count all received samples.
        # new_data.shape[1] is the number of new samples per channel.
        self.total_samples_received += new_data.shape[1]

        # Keep only the newest 10 seconds for plotting.
        if self.data_buffer.shape[1] > self.window_size:
            self.data_buffer = self.data_buffer[:, -self.window_size:]

    def has_data(self):
        """Return True if enough data is available for plotting."""
        return self.data_buffer.shape[1] >= 2

    def get_window(self):
        """
        Return x and y data for plotting.

        x is a relative time axis for the visible rolling window.
        y is one selected EMG channel.
        """
        y = self.data_buffer[self.selected_channel, :]

        number_of_samples = y.shape[0]
        x = np.arange(number_of_samples) / self.sampling_rate

        return x, y

    def get_signal_time_seconds(self):
        """
        Return the signal time in seconds.

        Formula:
            signal_time = total_samples_received / sampling_rate
        """
        return self.total_samples_received / self.sampling_rate