Socket Programming: Data Transmission with Error Detection Methods
This project is a practical implementation of various error detection methods used in data communication, utilizing a socket programming architecture. It simulates the process of sending data, introducing artificial corruption during transmission, and verifying data integrity at the receiver side.
System Architecture
The project consists of three primary components that interact over a network:

Client 1 (Data Sender): Accepts text input from the user and generates specific control information (redundancy bits) for error detection.



Server (Intermediate Node + Data Corruptor): Acts as an agent that receives the packet, applies intentional data corruption, and forwards it to the final destination.




Client 2 (Receiver + Error Checker): Receives the potentially corrupted data, recalculates the control information, and compares it with the original to detect errors.




Error Detection Methods
Client 1 supports several algorithms to generate control information:

Parity Bit: Calculates a bit based on whether the number of 1s in the ASCII representation is even or odd.

2D Parity (Matrix Parity): Organizes text into a row-column matrix (e.g., 8×8) and generates parity bits for every row and column.

CRC (Cyclic Redundancy Check): Performs polynomial division (CRC-8, CRC-16, or CRC-32) to produce a remainder used as the control code.

Hamming Code: Calculates redundancy bits for 4-bit or 8-bit blocks, allowing for single-bit error detection.

Internet Checksum: Implements the standard IP checksum calculation.

Error Injection (Server Tasks)
The Server simulates real-world transmission issues by applying one or more of the following "Data Corruptor" methods:

Bit Flip: Fips a random bit (1→0 or 0→1).

Character Substitution: Replaces a character with a random one (e.g., HELLO → HEZLO).

Character Deletion: Removes a random character from the text (e.g., HELLO → HELO).

Random Character Insertion: Inserts a random character into the data stream (e.g., HELLO → HEALLO).

Character Swapping: Swaps two adjacent characters (e.g., HELLO → HLELO).

Multiple Bit Flips: Flips multiple random bits simultaneously.

Burst Error: Corrupts a sequence of 3 to 8 consecutive characters.

Data Workflow & Packet Structure
Transmission: Client 1 sends a packet in the format: DATA METHOD CONTROL_INFORMATION (e.g., HELLO CRC16|87AF).

Reception: Client 2 receives the packet and splits it into data, method, and incoming_control.

Verification: Client 2 recalculates the control information based on the received data and the specified method.


Reporting: The status is printed to the screen:

If bits match: Status: DATA CORRECT.

If bits differ: Status: DATA CORRUPTED.

Execution Order
To run the simulation, start the components in the following order:

Server (to listen for connections).

Client 2 (to be ready to receive data).

Client 1 (to send the initial data).
