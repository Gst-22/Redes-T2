
def config_machine (machine_number):
    config = open("config.txt", "r")

    cnfg_txt = config.readlines()
    PORT_RCV = int(cnfg_txt[machine_number * 2 - 2]) 
    PORT_SND = int(cnfg_txt[machine_number * 2 - 1])

    return (PORT_RCV, PORT_SND)