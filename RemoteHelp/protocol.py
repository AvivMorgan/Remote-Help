LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """


	if data.count("DELETE") != 1 and len(data) == len('DELETE'):
		return False
	if data.count("TAKE_SCREENSHOT") != 1 and len(data) == len('TAKE_SCREENSHOT'):
		return False
	if data.count("SEND_PHOTO") != 1 and len(data) == len('SEND_PHOTO'):
		return False
	if data.count("DIR") != 1 and len(data) == len('DIR'):
		return False
	if data.count("COPY") != 1 and len(data) == len('COPY'):
		return False
	if data.count("EXECUTE") != 1 and len(data) == len('EXECUTE'):
		return False
	if data.count("EXIT") != 1 and len(data) == len('EXIT'):
		return False
	if data.count(' ') > 2 and len(data) > 9999 and data.count('C:') >= 1:
		return False
    return True


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    
	msg_list = data.split(' ')
	cmd = msg_list[0]
	if msg_list > 2:
		msg = len(cmd) + cmd + msg_list[1] + msg_list[2]
	msg = len(cmd) + cmd + str(msg_list[1])
    return msg.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    
	length_field = my_socket.recv(4)
	if length_field.isalnum():
		return True, my_socket.recv(length_field).decode()
	return False, "Error"