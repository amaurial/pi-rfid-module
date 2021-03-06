FLIM = 1
SLIM = 0
#Modes for STMOD
TMOD_SPD_MASK = 3
TMOD_SPD_128 = 0
TMOD_SPD_14 = 1
TMOD_SPD_28I = 2
TMOD_SPD_28 = 3
# Error codes for OPC_ERR
ERR_LOCO_STACK_FULL = 1
ERR_LOCO_ADDR_TAKEN = 2
ERR_SESSION_NOT_PRESENT = 3
ERR_CONSIST_EMPTY = 4
ERR_LOCO_NOT_FOUND = 5
ERR_CMD_RX_BUF_OFLOW = 6
ERR_INVALID_REQUEST = 7
ERR_SESSION_CANCELLED = 8
# Status codes for OPC_SSTAT
SSTAT_NO_ACK = 1
SSTAT_OVLD = 2
SSTAT_WR_ACK = 3
SSTAT_BUSY = 4
SSTAT_CV_ERROR = 5
#Error codes for OPC_CMDERR
CMDERR_INV_CMD = 1
CMDERR_NOT_LRN = 2
CMDERR_NOT_SETUP = 3
CMDERR_TOO_MANY_EVENTS = 4
# CMDERR_NO_EV 5 now reserved
CMDERR_INV_EV_IDX = 6
CMDERR_INVALID_EVENT = 7
#CMDERR_INV_EN_IDX 8 now reserved
CMDERR_INV_PARAM_IDX = 9
CMDERR_INV_NV_IDX = 10
CMDERR_INV_EV_VALUE = 11
CMDERR_INV_NV_VALUE = 12
# Parameter index numbers (readable by OPC_RQNPN, returned in OPC_PARAN)
# Index numbers count from 1, subtract 1 for offset into parameter block
# Note that RQNPN with index 0 returns the parameter count
PAR_MANU = 1 # Manufacturer id
PAR_MINVER = 2 # Minor version letter
PAR_MTYP = 3 # Module type code
PAR_EVTNUM = 4 # Number of events supported
PAR_EVNUM = 5 # Event variables per event
PAR_NVNUM = 6 # Number of Node variables
PAR_MAJVER = 7 # Major version number
PAR_FLAGS = 8 # Node flags
PAR_CPUID = 9 # Processor type
PAR_BUSTYPE = 10 # Bus type
PAR_LOAD = 11 # load address, 4 bytes
CAN_SFF_MASK = 0x000007ff

OPC_ACK = b'\x00'
OPC_NAK = b'\x01'
OPC_HLT = b'\x02'
OPC_BON = b'\x03'
OPC_TOF = b'\x04'
OPC_TON = b'\x05'
OPC_ESTOP = b'\x06'
OPC_ARST = b'\x07'
OPC_RTOF = b'\x08'
OPC_RTON = b'\x09'
OPC_RESTP = b'\x0a'
OPC_RSTAT = b'\x0c'
OPC_QNN = b'\x0d'
OPC_RQNP = b'\x10'
OPC_RQMN = b'\x11'
OPC_KLOC = b'\x21'
OPC_QLOC = b'\x22'
OPC_DKEEP = b'\x23'
OPC_DBG1 = b'\x30'
OPC_EXTC = b'\x3F'
OPC_RLOC = b'\x40'
OPC_QCON = b'\x41'
OPC_SNN = b'\x42'
OPC_STMOD = b'\x44'
OPC_PCON = b'\x45'
OPC_KCON = b'\x46'
OPC_DSPD = b'\x47'
OPC_DFLG = b'\x48'
OPC_DFNON = b'\x49'
OPC_DFNOF = b'\x4A'
OPC_SSTAT = b'\x4C'
OPC_RQNN = b'\x50'
OPC_NNREL = b'\x51'
OPC_NNACK = b'\x52'
OPC_NNLRN = b'\x53'
OPC_NNULN = b'\x54'
OPC_NNCLR = b'\x55'
OPC_NNEVN = b'\x56'
OPC_NERD = b'\x57'
OPC_RQEVN = b'\x58'
OPC_WRACK = b'\x59'
OPC_RQDAT = b'\x5A'
OPC_RQDDS = b'\x5B'
OPC_BOOT = b'\x5C'
OPC_ENUM = b'\x5D'
OPC_RST = ''
OPC_EXTC1 = b'\x5F'
OPC_DFUN = b'\x60'
OPC_GLOC = b'\x61'
OPC_ERR = b'\x63'
OPC_CMDERR = b'\x6F'
OPC_EVNLF = b'\x70'
OPC_NVRD = b'\x71'
OPC_NENRD = b'\x72'
OPC_RQNPN = b'\x73'
OPC_NUMEV = b'\x74'
OPC_CANID = b'\x75'
OPC_EXTC2 = b'\x7F'
OPC_RDCC3 = b'\x80'
OPC_WCVO = b'\x82'
OPC_WCVB = b'\x83'
OPC_QCVS = b'\x84'
OPC_PCVS = b'\x85'
OPC_ACON = b'\x90'
OPC_ACOF = b'\x91'
OPC_AREQ = b'\x92'
OPC_ARON = b'\x93'
OPC_AROF = b'\x94'
OPC_EVULN = b'\x95'
OPC_NVSET = b'\x96'
OPC_NVANS = b'\x97'
OPC_ASON = b'\x98'
OPC_ASOF = b'\x99'
OPC_ASRQ = b'\x9A'
OPC_PARAN = b'\x9B'
OPC_REVAL = b'\x9C'
OPC_ARSON = b'\x9D'
OPC_ARSOF = b'\x9E'
OPC_EXTC3 = b'\x9F'
OPC_RDCC4 = b'\xA0'
OPC_WCVS = b'\xA2'
OPC_ACON1 = b'\xB0'
OPC_ACOF1 = b'\xB1'
OPC_REQEV = b'\xB2'
OPC_ARON1 = b'\xB3'
OPC_AROF1 = b'\xB4'
OPC_NEVAL = b'\xB5'
OPC_PNN = b'\xB6'
OPC_ASON1 = b'\xB8'
OPC_ASOF1 = b'\xB9'
OPC_ARSON1 = b'\xBD'
OPC_ARSOF1 = b'\xBE'
OPC_EXTC4 = b'\xBF'
OPC_RDCC5 = b'\xC0'
OPC_WCVOA = b'\xC1'
OPC_FCLK = b'\xCF'
OPC_ACON2 = b'\xD0'
OPC_ACOF2 = b'\xD1'
OPC_EVLRN = b'\xd2'
OPC_EVANS = b'\xd3'
OPC_ARON2 = b'\xD4'
OPC_AROF2 = b'\xD5'
OPC_ASON2 = b'\xD8'
OPC_ASOF2 = b'\xD9'
OPC_ARSON2 = b'\xDD'
OPC_ARSOF2 = b'\xDE'
OPC_EXTC5 = b'\xDF'
OPC_RDCC6 = b'\xE0'
OPC_PLOC = b'\xE1'
OPC_NAME = b'\xE2'
OPC_STAT = b'\xE3'
OPC_PARAMS = b'\xEF'
OPC_ACON3 = b'\xF0'
OPC_ACOF3 = b'\xF1'
OPC_ENRSP = b'\xF2'
OPC_ARON3 = b'\xF3'
OPC_AROF3 = b'\xF4'
OPC_EVLRNI = b'\xF5'
OPC_ACDAT = b'\xF6'
OPC_ARDAT = b'\xF7'
OPC_ASON3 = b'\xF8'
OPC_ASOF3 = b'\xF9'
OPC_DDES = b'\xFA'
OPC_DDRS = b'\xFB'
OPC_ARSON3 = b'\xFD'
OPC_ARSOF3 = b'\xFE'
OPC_EXTC6 = b'\xFF'
