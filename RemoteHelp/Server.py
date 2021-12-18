import socket
import protocol
import glob, os, shutil, subprocess, pyautogui



IP = "0.0.0.0"
PHOTO_PATH = r"C:\Users\131\Desktop\Screen_shots\screen.jpg" # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
	ERROR = (False, "", [])
	if protocol.check_cmd(cmd):
		msg_list = cmd.split(' ')
		if len(msg_list) > 3:
			return ERROR
		elif len(msg_list) == 3:
			return True, msg_list[0], msg_list[1] + msg_list[2]
		else:
			return True, msg_list[0], msg_list[1]
	else:
		return ERROR
	

def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
	
    response = 'OK'
	if command == "DIR":
		return glob.glob(params)
	if command == "DELETE":
		os.remove(params)
	if command == "COPY":
		shutil.copy(params)
	if command == "EXECUTE":
		try:
			subprocess.call(params)
		except:
			response = "Execute has failed"
	if command == "TAKE_SCREENSHOT":
		try:
			image = pyautogui.screenshot()
			image.save(PHOTO_PATH)	
		except:
			response = "Screen shot has failed"
    return response


def main():
    # open socket with client

	new_socket = socket.socket()
	new_socket.bind((IP, 8820))
	client_socket.list()
	print("Server is up and running...")
	client, client_addr = new_socket.accept()
	print("Client is connected...")
    while True:
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

               

                if command == 'SEND_PHOTO':
					f = open(filename, 'rb')
					client.send(len(f.length()).zfill(4))
					client.send(f.length())
					l = f.read(f.length())
					client.send(l)
					f.close()
                
                elif command == 'EXIT':
                    break
					
				else:
					client.send(protocol.create_msg(handle_client_request(command, params).encode()))
            else:
                response = 'Bad command or parameters'
				client.send(response.encode())

        else:
            response = 'Packet not according to protocol'
			client.send(response.encode())
            client_socket.recv(1024)

    client.close()
    new_socket.close()
    print("Closing connection")


if __name__ == '__main__':
    main()
