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

OPC_ACK = ord(b'\x00')
OPC_NAK = ord(b'\x01')
OPC_HLT = ord(b'\x02')
OPC_BON = ord(b'\x03')
OPC_TOF = ord(b'\x04')
OPC_TON = ord(b'\x05')
OPC_ESTOP = ord(b'\x06')
OPC_ARST = ord(b'\x07')
OPC_RTOF = ord(b'\x08')
OPC_RTON = ord(b'\x09')
OPC_RESTP = ord(b'\x0a')
OPC_RSTAT = ord(b'\x0c')
OPC_QNN = ord(b'\x0d')
OPC_RQNP = ord(b'\x10')
OPC_RQMN = ord(b'\x11')
OPC_KLOC = ord(b'\x21')
OPC_QLOC = ord(b'\x22')
OPC_DKEEP = ord(b'\x23')
OPC_DBG1 = ord(b'\x30')
OPC_EXTC = ord(b'\x3F')
OPC_RLOC = ord(b'\x40')
OPC_QCON = ord(b'\x41')
OPC_SNN = ord(b'\x42')
OPC_STMOD = ord(b'\x44')
OPC_PCON = ord(b'\x45')
OPC_KCON = ord(b'\x46')
OPC_DSPD = ord(b'\x47')
OPC_DFLG = ord(b'\x48')
OPC_DFNON = ord(b'\x49')
OPC_DFNOF = ord(b'\x4A')
OPC_SSTAT = ord(b'\x4C')
OPC_RQNN = ord(b'\x50')
OPC_NNREL = ord(b'\x51')
OPC_NNACK = ord(b'\x52')
OPC_NNLRN = ord(b'\x53')
OPC_NNULN = ord(b'\x54')
OPC_NNCLR = ord(b'\x55')
OPC_NNEVN = ord(b'\x56')
OPC_NERD = ord(b'\x57')
OPC_RQEVN = ord(b'\x58')
OPC_WRACK = ord(b'\x59')
OPC_RQDAT = ord(b'\x5A')
OPC_RQDDS = ord(b'\x5B')
OPC_BOOT = ord(b'\x5C')
OPC_ENUM = ord(b'\x5D')
OPC_RST = ''
OPC_EXTC1 = ord(b'\x5F')
OPC_DFUN = ord(b'\x60')
OPC_GLOC = ord(b'\x61')
OPC_ERR = ord(b'\x63')
OPC_CMDERR = ord(b'\x6F')
OPC_EVNLF = ord(b'\x70')
OPC_NVRD = ord(b'\x71')
OPC_NENRD = ord(b'\x72')
OPC_RQNPN = ord(b'\x73')
OPC_NUMEV = ord(b'\x74')
OPC_CANID = ord(b'\x75')
OPC_EXTC2 = ord(b'\x7F')
OPC_RDCC3 = ord(b'\x80')
OPC_WCVO = ord(b'\x82')
OPC_WCVB = ord(b'\x83')
OPC_QCVS = ord(b'\x84')
OPC_PCVS = ord(b'\x85')
OPC_ACON = ord(b'\x90')
OPC_ACOF = ord(b'\x91')
OPC_AREQ = ord(b'\x92')
OPC_ARON = ord(b'\x93')
OPC_AROF = ord(b'\x94')
OPC_EVULN = ord(b'\x95')
OPC_NVSET = ord(b'\x96')
OPC_NVANS = ord(b'\x97')
OPC_ASON = ord(b'\x98')
OPC_ASOF = ord(b'\x99')
OPC_ASRQ = ord(b'\x9A')
OPC_PARAN = ord(b'\x9B')
OPC_REVAL = ord(b'\x9C')
OPC_ARSON = ord(b'\x9D')
OPC_ARSOF = ord(b'\x9E')
OPC_EXTC3 = ord(b'\x9F')
OPC_RDCC4 = ord(b'\xA0')
OPC_WCVS = ord(b'\xA2')
OPC_ACON1 = ord(b'\xB0')
OPC_ACOF1 = ord(b'\xB1')
OPC_REQEV = ord(b'\xB2')
OPC_ARON1 = ord(b'\xB3')
OPC_AROF1 = ord(b'\xB4')
OPC_NEVAL = ord(b'\xB5')
OPC_PNN = ord(b'\xB6')
OPC_ASON1 = ord(b'\xB8')
OPC_ASOF1 = ord(b'\xB9')
OPC_ARSON1 = ord(b'\xBD')
OPC_ARSOF1 = ord(b'\xBE')
OPC_EXTC4 = ord(b'\xBF')
OPC_RDCC5 = ord(b'\xC0')
OPC_WCVOA = ord(b'\xC1')
OPC_FCLK = ord(b'\xCF')
OPC_ACON2 = ord(b'\xD0')
OPC_ACOF2 = ord(b'\xD1')
OPC_EVLRN = ord(b'\xd2')
OPC_EVANS = ord(b'\xd3')
OPC_ARON2 = ord(b'\xD4')
OPC_AROF2 = ord(b'\xD5')
OPC_ASON2 = ord(b'\xD8')
OPC_ASOF2 = ord(b'\xD9')
OPC_ARSON2 = ord(b'\xDD')
OPC_ARSOF2 = ord(b'\xDE')
OPC_EXTC5 = ord(b'\xDF')
OPC_RDCC6 = ord(b'\xE0')
OPC_PLOC = ord(b'\xE1')
OPC_NAME = ord(b'\xE2')
OPC_STAT = ord(b'\xE3')
OPC_PARAMS = ord(b'\xEF')
OPC_ACON3 = ord(b'\xF0')
OPC_ACOF3 = ord(b'\xF1')
OPC_ENRSP = ord(b'\xF2')
OPC_ARON3 = ord(b'\xF3')
OPC_AROF3 = ord(b'\xF4')
OPC_EVLRNI = ord(b'\xF5')
OPC_ACDAT = ord(b'\xF6')
OPC_ARDAT = ord(b'\xF7')
OPC_ASON3 = ord(b'\xF8')
OPC_ASOF3 = ord(b'\xF9')
OPC_DDES = ord(b'\xFA')
OPC_DDRS = ord(b'\xFB')
OPC_ARSON3 = ord(b'\xFD')
OPC_ARSOF3 = ord(b'\xFE')
OPC_EXTC6 = ord(b'\xFF')

OPCNAMES = {
ord(b'\x00'):'OPC_ACK',
ord(b'\x01'):'OPC_NAK',
ord(b'\x02'):'OPC_HLT',
ord(b'\x03'):'OPC_BON',
ord(b'\x04'):'OPC_TOF',
ord(b'\x05'):'OPC_TON',
ord(b'\x06'):'OPC_ESTOP',
ord(b'\x07'):'OPC_ARST',
ord(b'\x08'):'OPC_RTOF',
ord(b'\x09'):'OPC_RTON',
ord(b'\x0a'):'OPC_RESTP',
ord(b'\x0c'):'OPC_RSTAT',
ord(b'\x0d'):'OPC_QNN',
ord(b'\x10'):'OPC_RQNP',
ord(b'\x11'):'OPC_RQMN',
ord(b'\x21'):'OPC_KLOC',
ord(b'\x22'):'OPC_QLOC',
ord(b'\x23'):'OPC_DKEEP',
ord(b'\x30'):'OPC_DBG1',
ord(b'\x3F'):'OPC_EXTC',
ord(b'\x40'):'OPC_RLOC',
ord(b'\x41'):'OPC_QCON',
ord(b'\x42'):'OPC_SNN',
ord(b'\x44'):'OPC_STMOD',
ord(b'\x45'):'OPC_PCON',
ord(b'\x46'):'OPC_KCON',
ord(b'\x47'):'OPC_DSPD',
ord(b'\x48'):'OPC_DFLG',
ord(b'\x49'):'OPC_DFNON',
ord(b'\x4A'):'OPC_DFNOF',
ord(b'\x4C'):'OPC_SSTAT',
ord(b'\x50'):'OPC_RQNN',
ord(b'\x51'):'OPC_NNREL',
ord(b'\x52'):'OPC_NNACK',
ord(b'\x53'):'OPC_NNLRN',
ord(b'\x54'):'OPC_NNULN',
ord(b'\x55'):'OPC_NNCLR',
ord(b'\x56'):'OPC_NNEVN',
ord(b'\x57'):'OPC_NERD',
ord(b'\x58'):'OPC_RQEVN',
ord(b'\x59'):'OPC_WRACK',
ord(b'\x5A'):'OPC_RQDAT',
ord(b'\x5B'):'OPC_RQDDS',
ord(b'\x5C'):'OPC_BOOT',
ord(b'\x5D'):'OPC_ENUM',
ord(b'\x5F'):'OPC_EXTC1',
ord(b'\x60'):'OPC_DFUN',
ord(b'\x61'):'OPC_GLOC',
ord(b'\x63'):'OPC_ERR',
ord(b'\x6F'):'OPC_CMDERR',
ord(b'\x70'):'OPC_EVNLF',
ord(b'\x71'):'OPC_NVRD',
ord(b'\x72'):'OPC_NENRD',
ord(b'\x73'):'OPC_RQNPN',
ord(b'\x74'):'OPC_NUMEV',
ord(b'\x75'):'OPC_CANID',
ord(b'\x7F'):'OPC_EXTC2',
ord(b'\x80'):'OPC_RDCC3',
ord(b'\x82'):'OPC_WCVO',
ord(b'\x83'):'OPC_WCVB',
ord(b'\x84'):'OPC_QCVS',
ord(b'\x85'):'OPC_PCVS',
ord(b'\x90'):'OPC_ACON',
ord(b'\x91'):'OPC_ACOF',
ord(b'\x92'):'OPC_AREQ',
ord(b'\x93'):'OPC_ARON',
ord(b'\x94'):'OPC_AROF',
ord(b'\x95'):'OPC_EVULN',
ord(b'\x96'):'OPC_NVSET',
ord(b'\x97'):'OPC_NVANS',
ord(b'\x98'):'OPC_ASON',
ord(b'\x99'):'OPC_ASOF',
ord(b'\x9A'):'OPC_ASRQ',
ord(b'\x9B'):'OPC_PARAN',
ord(b'\x9C'):'OPC_REVAL',
ord(b'\x9D'):'OPC_ARSON',
ord(b'\x9E'):'OPC_ARSOF',
ord(b'\x9F'):'OPC_EXTC3',
ord(b'\xA0'):'OPC_RDCC4',
ord(b'\xA2'):'OPC_WCVS',
ord(b'\xB0'):'OPC_ACON1',
ord(b'\xB1'):'OPC_ACOF1',
ord(b'\xB2'):'OPC_REQEV',
ord(b'\xB3'):'OPC_ARON1',
ord(b'\xB4'):'OPC_AROF1',
ord(b'\xB5'):'OPC_NEVAL',
ord(b'\xB6'):'OPC_PNN',
ord(b'\xB8'):'OPC_ASON1',
ord(b'\xB9'):'OPC_ASOF1',
ord(b'\xBD'):'OPC_ARSON1',
ord(b'\xBE'):'OPC_ARSOF1',
ord(b'\xBF'):'OPC_EXTC4',
ord(b'\xC0'):'OPC_RDCC5',
ord(b'\xC1'):'OPC_WCVOA',
ord(b'\xCF'):'OPC_FCLK',
ord(b'\xD0'):'OPC_ACON2',
ord(b'\xD1'):'OPC_ACOF2',
ord(b'\xd2'):'OPC_EVLRN',
ord(b'\xd3'):'OPC_EVANS',
ord(b'\xD4'):'OPC_ARON2',
ord(b'\xD5'):'OPC_AROF2',
ord(b'\xD8'):'OPC_ASON2',
ord(b'\xD9'):'OPC_ASOF2',
ord(b'\xDD'):'OPC_ARSON2',
ord(b'\xDE'):'OPC_ARSOF2',
ord(b'\xDF'):'OPC_EXTC5',
ord(b'\xE0'):'OPC_RDCC6',
ord(b'\xE1'):'OPC_PLOC',
ord(b'\xE2'):'OPC_NAME',
ord(b'\xE3'):'OPC_STAT',
ord(b'\xEF'):'OPC_PARAMS',
ord(b'\xF0'):'OPC_ACON3',
ord(b'\xF1'):'OPC_ACOF3',
ord(b'\xF2'):'OPC_ENRSP',
ord(b'\xF3'):'OPC_ARON3',
ord(b'\xF4'):'OPC_AROF3',
ord(b'\xF5'):'OPC_EVLRNI',
ord(b'\xF6'):'OPC_ACDAT',
ord(b'\xF7'):'OPC_ARDAT',
ord(b'\xF8'):'OPC_ASON3',
ord(b'\xF9'):'OPC_ASOF3',
ord(b'\xFA'):'OPC_DDES',
ord(b'\xFB'):'OPC_DDRS',
ord(b'\xFD'):'OPC_ARSON3',
ord(b'\xFE'):'OPC_ARSOF3',
ord(b'\xFF'):'OPC_EXTC6'
}