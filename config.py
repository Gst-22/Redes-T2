
def set_configs (machine_number):
    config = open("config.txt", "r")

    cnfg_txt = config.readlines()
    UDP_IP = cnfg_txt[machine_number * 4 - 4].strip()
    MDP_IP = cnfg_txt[machine_number * 4 - 3].strip()
    PORT_RCV = int(cnfg_txt[machine_number * 4 - 2]) 
    PORT_SND = int(cnfg_txt[machine_number * 4 - 1])

    return (PORT_RCV, PORT_SND, UDP_IP, MDP_IP)