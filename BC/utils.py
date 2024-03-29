def adresse_gen(nodes):
    import uuid
    
    add = "RVx{0}".format(uuid.uuid4().hex)
    if add in nodes:
        adresse_gen(nodes)
    return add

def adress_checkVadility_Avaibality(add, nodes):
    if add.startswith("RVx"):
        if add not in nodes:
            return True
    return False

def init_logging(file_name="logger.log"):
    import logging
    logger = logging.getLogger('FTP Client Logs')
    logging.basicConfig(
        filename=file_name,
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )