import sys
import os
import struct

_tcioLibFileName = "tcio_stdcall.dll"
DLL_SUCCESS = 0
DLL_FAIL = -1
comPortStart = 1
comPortEnd = 10
comPortFound = 0
dllState = 0
dllError = 0

import ctypes as C

class TopCon():
    """
    Driver for Regatron TopCon compatible Power Supplies
    """
    version = '0.1'
    deviceType = 'Regatron_TopCon'
    # Load DLL into memory.
    tcio_dll_obj = C.cdll.LoadLibrary(_tcioLibFileName)
    print(tcio_dll_obj)

    def __init__(self):
        result = self.tcio_dll_obj.DllInit()
        if (result != DLL_SUCCESS):
            print("DllInit failed")
            connected = False


    def close(self):
        result = self.tcio_dll_obj.DllClose()
        if (result != DLL_SUCCESS):
            print("DllClose failed")
            connected = False
        return result

    def get_status(self):
        state = C.c_int()
        errorno  = C.c_int()
        result = self.tcio_dll_obj.DllGetStatus(C.byref(state), C.byref(errorno))
        if (result != DLL_SUCCESS):
            print("DllClose failed")
            state = DLL_SUCCESS
        return state

    def get_device_type(self):
        '''
        Parameters:
        [out]	p_devtype	device type identifier
        Note:
        DllSearchDevice must be called before
        see enum T_DeviceType
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        '''
        devtype = C.c_int()
        result = self.tcio_dll_obj.DllGetDeviceType(C.byref(devtype))
        if (result != DLL_SUCCESS):
            print("DllClose failed")
            devtype = DLL_SUCCESS
        return devtype

    def read_version(self):
        version = C.c_int()
        build = C.c_int()
        version_string = C.create_string_buffer(64)
        result = self.tcio_dll_obj.DllReadVersion(C.byref(version), C.byref(build), version_string)
        if (result != DLL_SUCCESS):
            print("DllClose failed")
            connected = False
        return version, build, version_string

    def search_devices(self,fromport, toport):
        p_portnrfound = C.create_string_buffer(10)
        result = self.tcio_dll_obj.DllSearchDevice(fromport, toport, C.byref(p_portnrfound))
        if (result != DLL_SUCCESS):
            print("DllClose failed")
            portnrfound = None
        return portnrfound

    def connect(self, port):
        p_portnrfound = C.create_string_buffer(1)
        result = self.tcio_dll_obj.DllSearchDevice(port, port, p_portnrfound)
        if (result != DLL_SUCCESS):
            print("DllClose failed")
            connected = False
        return result

    # def get_PhysicalValuesIncrement(p_vinc, p_iinc, p_pinc, p_rinc, v_sinc, isinc, p_sinc, rsinc):
    #     # TODO
    #     pass

    # def TC4SetModuleSelector(selector):
    #     # TODO
    #     pass

    # # actual values getters
    # def get_SystemPhysicalLimitMax(voltagePhysMax, currentPhysMax, powerPhysMax, resistancePhysMax):
    #     # TODO
    #     pass

    # def get_SystemPhysicalLimitMin(voltagePhysMin, currentPhysMin, powerPhysMin, resistancePhysMin):
    #     # TODO
    #     pass

    # def get_VoltageAct( p_Voltage):
    #     # TODO
    #     pass

    # def get_CurrentAct( p_Current):
    #     # TODO
    #     pass

    # def get_PowerAct( p_Power):
    #     # TODO
    #     pass

    def get_Q4_limit_current(self):
        """     
        Get Q4 controller current limit (parameter will be negative)
        Parameters:
        [out]	pCurrent	PhysicalCurrent [A]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs 
        """
        current = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetQ4LimitCurrent(C.byref(current))
        if (result != DLL_SUCCESS):
            print("DllClose failed")
            current = None
        return current

    def get_Q4_limit_power(self):
        """     
        Get Q4 controller power limit (parameter will be negative)
        Parameters:
        [out]	pPower	PhysicalPower [kW]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs 
        """
        power = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetQ4LimitPower(C.byref(power))
        if (result != DLL_SUCCESS):
            print("TC4GetQ4LimitPower failed")
            power = None
        return power

    # reference values getters and setters
    def get_voltage_ref(self):
        """     
        Parameters:
        [out]	vref	PhysicalVoltage [V]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        voltage = C.c_double
        foo=C.create_string_buffer(8)
        result = self.tcio_dll_obj.TC4GetVoltageRef(foo)
        result = self.tcio_dll_obj.TC4GetCurrentRef(foo)
        value = struct.unpack('d', foo.raw)[0]
        foo.raw
        #result = self.tcio_dll_obj.TC4GetVoltageRef(C.byref(voltage))
        if (result != DLL_SUCCESS):
            print("TC4GetVoltageRef failed")
            voltage = None
        return voltage.value

    def get_current_ref(self):
        """     
        Parameters:
        [out]	iref	PhysicalCurrent [A]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        current = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetCurrentRef(C.byref(current))
        if (result != DLL_SUCCESS):
            print("TC4GetCurrentRef failed")
            current = None
        return current.value

    def get_power_ref(self):
        """     
        """
        power = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetPowerRef(C.byref(power))
        if (result != DLL_SUCCESS):
            print("TC4GetPowerRef failed")
            power = None
        return power.value

    def get_resistance_ref(self):
        """
        Parameters:
        [out]	rref	PhysicalResistance [mOhm]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs   
        """
        resistance = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetResistanceRef(C.byref(resistance))
        if (result != DLL_SUCCESS):
            print("TC4GetResistanceRef failed")
            resistance = None
        return resistance.value

    def set_voltage_ref(self, vref):
        """     
        Parameters:
        [in]	vref	PhysicalVoltage [V]
        Precondition:
        Remote control input must be set to RS232
        Note:
        Calling these functions on a TopCon Slave will have no effect.
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        vref_double = C.c_longdouble()
        vref_double.value = float(vref) 
        result = self.tcio_dll_obj.TC4SetVoltageRef(vref_double)
        if (result != DLL_SUCCESS):
            print("TC4SetVoltageRef failed")
        return vref_double.value

    def set_current_ref(self, iref):
        """     
        Parameters:
        [out]	iref	PhysicalCurrent [A]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        iref_double = C.c_longdouble()
        iref_double.value = float(iref) 
        result = self.tcio_dll_obj.TC4GetCurrentRef(C.byref(current))
        if (result != DLL_SUCCESS):
            print("TC4GetCurrentRef failed")
            current = None
        return current.value

    def set_power_ref(self, pref):
        """     
        Parameters:
        [out]	rref	PhysicalResistance [mOhm]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        pref_double = C.c_longdouble()
        pref_double.value = float(pref) 
        result = self.tcio_dll_obj.TC4GetPowerRef(C.byref(pref_double))
        if (result != DLL_SUCCESS):
            print("TC4GetPowerRef failed")
            pref_double = None
        return pref_double.value

    def set_resistance_ref(self, rref):
        """     
        Parameters:
        [in]	rref	PhysicalResistance [mOhm]
        Precondition:
        Remote control input must be set to RS232
        Note:
        Calling these functions on a TopCon Slave will have no effect.
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        rref_double = C.c_longdouble()
        rref_double.value = rref 
        result = self.tcio_dll_obj.TC4SetResistanceRef(rref_double)
        if (result != DLL_SUCCESS):
            print("TC4SetResistanceRef failed")
        return result.value

    # reference values getters and setters
    def get_voltage_act(self):
        """     
        Parameters:
        [out]	p_vact	Actual voltage value [V]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        vact = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetVoltageAct(C.byref(vact))
        if (result != DLL_SUCCESS):
            print("TC4GetVoltageAct failed")
            vact = None
        return vact.value

    def get_current_act(self):
        """     
        Parameters:
        [out]	p_iact	Actual current value [A]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        iact = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetCurrentAct(C.byref(iact))
        if (result != DLL_SUCCESS):
            print("TC4GetCurrentAct failed")
            iact = None
        return iact.value

    def get_power_act(self):
        """     
        Parameters:
        [out]	p_pact	Actual power value [kW]
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        pact = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetPowerAct(C.byref(pact))
        if (result != DLL_SUCCESS):
            print("TC4GetPowerAct failed")
            pact = None
        return pact.value

    def get_resistance_act(self):
        """     
        Parameters:
        [out]	p_ract	Actual simulated resistance value
        Note:
        resistance is not measured - this will just read the set value
        Returns:
        DLL_SUCCESS for success or DLL_FAIL or other value if an error occurs
        """
        ract = C.c_longdouble()
        result = self.tcio_dll_obj.TC4GetResistanceAct(C.byref(ract))
        if (result != DLL_SUCCESS):
            print("TC4GetResistanceAct failed")
            ract = None
        return ract.value


if __name__ == "__main__":
    # execute only if run as a script
    com_port_source = 7
    com_port_sink = 4
    source_TopCon = TopCon()
    source_TopCon.connect(com_port_source)
    # print(source_TopCon.get_status())
    # print(source_TopCon.get_device_type())
    # result = TC4GetPhysicalValuesIncrement(ref p_vinc, ref p_iinc, ref p_pinc, ref p_rinc, ref vsinc, ref isinc, ref psinc, ref rsinc);
    # result = TC4GetSystemPhysicalLimitMax(ref voltagePhysMax, ref currentPhysMax, ref powerPhysMax, ref resistancePhysMax);
    # result = TC4GetSystemPhysicalLimitMin(ref voltagePhysMin, ref currentPhysMin, ref powerPhysMin, ref resistancePhysMin);
    # result = TC4SetModuleSelector(64);
    # result = DllGetStatus(ref dllState, ref dllError);
    print("Q4 Values")
    print(source_TopCon.get_Q4_limit_current())
    print("Reference Values")
    print(source_TopCon.get_voltage_ref())
    print(source_TopCon.get_current_ref())
    print(source_TopCon.get_power_ref())
    # print("set Reference Values")
    # source_TopCon.set_voltage_ref(10.0)
    # print(source_TopCon.get_voltage_ref())
    # print("Actual Values")
    # print(source_TopCon.get_voltage_act())
    # print(source_TopCon.get_current_act())
    # print(source_TopCon.get_power_act())
    source_TopCon.close()

#myTopCon.SetPowerOn()
#dVolt = 120
#myTopCon.SeterenceVoltage(dVolt)
#myTopCon.SetPowerOff()
#print("Press any key to  DisConnect from TopCon Device")
#
#myTopCon.Disconnect()


# def display_TopCon_System_State_Info(myTopCon As Ch.Regatron.HPPS.Device.TopCon)
#    Console.WriteLine(NL & SPACE1 & "--------  TopCon System status  --------")
#
#    'Display TopCon System Power On/Off Info.
#    if (myTopCon.IsPowerON()) Then
#      Console.WriteLine(SPACE1 & "Power is ON")
#    else
#      Console.WriteLine(SPACE1 & "Power is OFF")
#
#    'Display TopCon System State Code Nr.
#    Console.WriteLine(SPACE1 & "System State: [" & myTopCon.GetSystemState() & "]")
#
#    'Display TopCon System State String.
#    Console.WriteLine(SPACE1 & "System State string: [" & myTopCon.GetSystemStateAsString() & "]")
#
#    'Display TopCon System State Error Boolean with Text.
#    if (myTopCon.IsInErrorState()) Then
#      Console.WriteLine(SPACE1 & "System IS in Error state.")
#    else
#      Console.WriteLine(SPACE1 & "System is NOT in Error state.")


