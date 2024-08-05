
def set_configs (machine_number):
    config = open("config.txt", "r")

    cnfg_txt = config.readlines()
    UDP_IP = cnfg_txt[machine_number * 3 - 3].strip()
    PORT_RCV = int(cnfg_txt[machine_number * 3 - 2]) 
    PORT_SND = int(cnfg_txt[machine_number * 3 - 1])

    return (PORT_RCV, PORT_SND, UDP_IP)