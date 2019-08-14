from cryptography.fernet import Fernet


key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdQZdycFF6eSnjVgU-Efs6_10yLOED6H7O6zqtzPEXopHqKLQp-LV5Po6FC-' \
          b'YLHrfXDmRXxhnqieH72cHjpEKcEi_XYkxzEVI95wichcMPi0mP36M3ugG9Ot9vieldB' \
          b'L3RgammXHZ9u4z4B7t9I_rffW546JRfvhwFNlqwQbp0eqkIutI='


def main():
    f = Fernet(key)
    # display the str of the decoded byte
    print(f.decrypt(message).decode("utf-8"))


if __name__ == "__main__":
    main()
