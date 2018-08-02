"""
    Tektronix library, written by james bynes <bynes@hawaii.edu>
    taken from tektronix programmers manual
"""
from collections import *
from link import *
import numpy as np
#from tex_channel import *


class tektronix(object):

    def __init__(self, addr=None, port=None):
        addr = addr.upper()
        #self.channel = defaultdict(int)

        # Set up link connection. Either RS232 via USB or GPIO via Eth
        if(addr == 'RS232') or (addr == 'RS-232'):
            self.link = RS232()
        elif(addr != None) and (port == None):
            self.link = Ethernet(addr)
        elif(addr != None) and (port != None):
            self.link = Ethernet_Controller(addr, port)
        else:
            print("Invalid address: " + str(addr))
        # for i in range(4):
            #self.channel[i+1]=channel(link=self.link, name="CH"+str(i+1))

    def scope_name(self):
        '''Input: None
                Output: Return the model number of the instrument '''
        name = self.identification
        comma1 = name.find(",")
        comma2 = name.find(",", comma1+1)
        self.scope_name = name[comma1+1:comma2]
        return self.scope_name

    def __binary_cmd(self, cmd):
        if isinstance(cmd, str):
            cmd = cmd.upper()
        try:
            cmd = {1: '1', '1': '1', 0: '0', '0': '0',
                   'ON': 'ON', 'OFF': 'OFF'}[cmd]
        except KeyError:
            print("Invalid operation: "+cmd)
        else:
            return cmd

    @property
    def esr(self):
        ''' Input: 
            Output: '''
        return self.link.ask("*ESR?")

    @property
    def reset(self):
        ''' Input: None
                Output: Returns nothing, but resets settings'''
        self.link.cmd("*RST")

    @property
    def identification(self):
        ''' Input: None
                Output: Return identification of instrument '''
        return self.link.ask("*IDN?")

    @property
    def self_test_query(self):
        ''' Input: None
                Output: Return test query '''
        return self.link.ask("*TST?")

    @property
    def header(self):
        ''' Input: None
                Output: Return header status '''
        return self.link.ask("HEADER?")

    @header.setter
    def header(self, cmd):
        ''' Input: ON or OFF, sets header
                Output: Nothing '''
        self.link.cmd("HEADER " + self.__binary_cmd(cmd))

    @property
    def data_encoding(self):
        ''' Input:
                Output: '''
        return self.link.ask("DAT:ENC?")

    @data_encoding.setter
    def data_encoding(self, cmd):
        ''' Input: ASCI, ...
                Output: '''
        self.link.cmd("DAT:ENC "+format(cmd))

    @property
    def acq_state(self):
        ''' Input: None
                Output: checks state, run or stop '''
        return int(self.link.ask("ACQ:STATE?").rstrip('\n'))

    @acq_state.setter
    def acq_state(self, cmd):
        ''' Input: 0 ('OFF') or 1 ("ON")
                Output: Outputs state '''
        self.link.cmd("ACQ:STATE " + self.__binary_cmd(cmd))

    @property
    def acq_stop_after(self):
        return self.link.ask("ACQ:STOPA?")

    @acq_stop_after.setter
    def acq_stop_after(self, cmd):
        cmd = cmd.upper()
        try:
            cmd = {'RUNSTOP': 'RUNSTop', 'SEQUENCE': 'SEQuence'}[cmd]

            self.link.cmd('ACQ:STOPA '+format(cmd))
        except KeyError:
            print("Invalid operation: " + cmd)

    @property
    def filename(self):
        ''' Input: none
                Output: displays current filepath '''
        return self.link.ask("EXP:FILEN?")

    @filename.setter
    def filename(self, cmd):
        ''' Input: Name of file w/.png ext, file automatically
                        saves at C:/TekScope/Images/
                Output: nothing '''
        return self.link.cmd('EXP:FILEN '+'"C:/TekScope/Images/'+format(cmd)+'"')

    @property
    def horiz_record_len(self):
        ''' Input: 
                Output: '''
        return self.link.ask("HOR:RECO?")

    @horiz_record_len.setter
    def horiz_record_len(self, cmd):
        ''' Input:
                Output: '''
        self.link.cmd("HOR:RECO "+format(cmd))

    @property
    def horiz_scale(self):
        return self.link.ask("HOR:SCA?")

    @horiz_scale.setter
    def horiz_scale(self, cmd):
        self.link.cmd("HOR:SCA "+format(cmd))

    @property
    def horiz_sample(self):
        return self.link.ask("HOR:MAI:SAMPLER?")

    @horiz_sample.setter
    def horiz_sample(self, cmd):
        self.link.cmd("HOR:MAI:SAMPLER "+format(cmd))

    @property
    def horiz_position(self):
        return self.link.ask("HOR:MAI:POS?")

    @horiz_position.setter
    def horiz_position(self, cmd):
        self.link.cmd("HOR:MAI:POS "+format(cmd))

    @property
    def data_source(self):
        ''' Input:
                Output: '''
        return self.link.ask("DAT:SOU?")

    @data_source.setter
    def data_source(self, cmd):
        ''' Input: {1, 2, 3, 4}
                Output: '''
        self.link.cmd("DAT:SOU CH"+format(cmd))

    @property
    def data_start(self):
        return self.link.ask("DAT:STAR?")

    @data_start.setter
    def data_start(self, cmd):
        self.link.cmd("DAT:STAR "+format(cmd))

    @property
    def data_stop(self):
        return self.link.ask("DAT:STOP?")

    @data_stop.setter
    def data_stop(self, cmd):
        self.link.cmd("DAT:STOP "+format(cmd))

    @property
    def preamble(self):
        ''' Input:
                Output: '''
        return self.link.ask("WFMO?")

    @property
    def curve(self):
        ''' Input: None
                Outputs: Curve data '''
        return self.link.ask("CURV?")

    @property
    def wave_file_format(self):
        ''' Input: none
                Output: displays format for saved waveform '''
        return self.link.ask("SAVE:WAVE:FILEF?")

    @wave_file_format.setter
    def wave_file_format(self, cmd):
        ''' Input: INTERN, MATL, or SPREADSHEETCsv
                Output: not sure yet '''
        return self.link.cmd('SAVE:WAVE:FILEF '+format(cmd))

    @property
    def wave_save(self):
        ''' Input: None
                Output: Channel of wave '''
        return str(self.channel)

    @wave_save.setter
    def wave_save(self, cmd):
        ''' Input: 1 - 4 (this is channel)
                Output: '''
        return self.link.cmd('SAVE:WAVE CH'+self.channel+', "C:/TekScope/Images/bman69.wfm"')

    @property
    def meas_min(self):
        ''' Input: 
            Output: '''
        return self.link.ask("MEASU:MEAS1:VAL?")

    @property
    def meas_source(self):
        ''' Input:
            Output: '''
        return self.link.ask("MEASU:MEAS1:SOURCE?")

    @meas_source.setter
    def meas_source(self, cmd):
        ''' Input:
            Output: '''
        self.link.cmd("MEASU:MEAS1:SOURCE "+format(cmd))

    @property
    def meas_typ(self):
        ''' Input: 
            Output: '''
        return self.link.ask("MEASU:MEAS1:TYP?")

    @meas_typ.setter
    def meas_typ(self, cmd):
        ''' Input:
            Output: '''
        self.link.cmd("MEASU:MEAS1:TYP "+format(cmd))

    # MEASUrement:MEAS<x>:STATE, pg 560
    # State can be either on or off, when on, enables calculation
    @property
    def meas_state(self):
        '''Input:
            Output: '''
        return self.link.ask("MEASU:MEAS1:STATE?")

    @meas_state.setter
    def meas_state(self, cmd):
        self.link.cmd("MEASU:MEAS1:STATE "+format(cmd))

    @property
    def ch1_scale(self):
        return self.link.ask("CH1:SCA?")

    @ch1_scale.setter
    def ch1_scale(self, cmd):
        self.link.cmd("CH1:SCA "+format(cmd))

    @property
    def ch2_scale(self):
        return self.link.ask("CH2:SCA?")

    @ch2_scale.setter
    def ch2_scale(self, cmd):
        self.link.cmd("CH2:SCA "+format(cmd))

    @property
    def ch3_scale(self):
        return self.link.ask("CH3:SCA?")

    @ch3_scale.setter
    def ch3_scale(self, cmd):
        self.link.cmd("CH3:SCA "+format(cmd))

    @property
    def ch4_scale(self):
        return self.link.ask("CH4:SCA?")

    @ch4_scale.setter
    def ch4_scale(self, cmd):
        self.link.cmd("CH4:SCA "+format(cmd))

    @property
    def waveform_out_encoding(self):
        return self.link.ask("WFMO:ENC?")

    @waveform_out_encoding.setter
    def waveform_out_encoding(self, cmd):
        # valid = Set(['BIN','ASC'])
        # if cmd in valid:
        self.link.cmd('WFMO:ENC ' + format(cmd))

    @property
    def waveform_out_byte_number(self):
        return self.link.ask('WFMO:BYT_N?')

    @waveform_out_byte_number.setter
    def waveform_out_byte_number(self, num):
        self.link.cmd('WFMO:BYT_N ' + format(num))

    @property
    def CH1_impedance(self):
        return self.link.ask("CH1:TER?")

    @CH1_impedance.setter
    def CH1_impedance(self, cmd):
        self.link.cmd("CH1:TER "+format(cmd))

    @property
    def CH2_impedance(self):
        return self.link.ask("CH2:TER?")

    @CH2_impedance.setter
    def CH2_impedance(self, cmd):
        self.link.cmd("CH2:TER "+format(cmd))

    @property
    def CH3_impedance(self):
        return self.link.ask("CH3:TER?")

    @CH3_impedance.setter
    def CH3_impedance(self, cmd):
        self.link.cmd("CH3:TER "+format(cmd))

    @property
    def CH4_impedance(self):
        return self.link.ask("CH4:TER?")

    @CH4_impedance.setter
    def CH4_impedance(self, cmd):
        self.link.cmd("CH4:TER "+format(cmd))

    @property
    def CH1_bandwidth(self):
        return self.link.ask("CH1:BAN?")

    @CH1_bandwidth.setter
    def CH1_bandwidth(self, cmd):
        self.link.cmd("CH1:BAN "+format(cmd))

    @property
    def CH2_bandwidth(self):
        return self.link.ask("CH2:BAN?")

    @CH2_bandwidth.setter
    def CH2_bandwidth(self, cmd):
        self.link.cmd("CH2:BAN "+format(cmd))

    @property
    def CH3_bandwidth(self):
        return self.link.ask("CH3:BAN?")

    @CH3_bandwidth.setter
    def CH3_bandwidth(self, cmd):
        self.link.cmd("CH3:BAN "+format(cmd))

    @property
    def CH4_bandwidth(self):
        return self.link.ask("CH4:BAN?")

    @CH4_bandwidth.setter
    def CH4_bandwidth(self, cmd):
        self.link.cmd("CH4:BAN "+format(cmd))

    @property
    def trig_edge_source(self):
        return self.link.ask("TRIG:A:EDGE:SOU?")

    @trig_edge_source.setter
    def trig_edge_source(self, cmd):
        self.link.cmd("TRIG:A:EDGE:SOU "+format(cmd))
