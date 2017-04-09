#!/usr/bin/python
import sys
import json
import lldb
import time
import shlex
import struct
import threading

# def DBG_LOG(msg):
#     with open("/Users/bsr/Desktop/log_lldb_output.txt", "a") as _LOG_FILE:
#       _LOG_FILE.write(msg)

def get_registers(frame, kind):
    registerSet = frame.GetRegisters()
    for value in registerSet:
        if kind.lower() in value.GetName().lower():
            return value
    return None

def build_reg_value_string(reg):
    value = ""
    if reg.MightHaveChildren():
        c_count = reg.GetNumChildren()
        offset = 0
        i_value = 0
        for child in reg:
            err = lldb.SBError()
            i_value += child.GetValueAsUnsigned(err) << offset
            offset += child.GetByteSize() << 3
        fmt = "0x%%0%dx" % (reg.GetByteSize() << 1)
        value = fmt % i_value
    else:
        value = reg.GetValue()
    return value

def get_GPRs(frame):
    return get_registers(frame, "general purpose")

def get_FPRs(frame):
    return get_registers(frame, "floating point")

def get_ESRs(frame):
    return get_registers(frame, "exception state")

def findRegister(frame,name):
    registerSet = frame.GetRegisters()
    for regSet in registerSet:
        for value in regSet:
            if value.GetName() == name:
                return value
    return None

class Handler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.target = None
        self.workingDirectory = None
        self.arguments = None
        self.executable = None
        self.is64Bits = True
        self.debugger = lldb.SBDebugger.Create()
        self.debugger.SetAsync(True)
        self.process = None
        self.target = None
        self.transport_lock = threading.Lock()
        listener = lldb.SBListener("Hopper listener")
        event = lldb.SBEvent()
        
        class EventThread(threading.Thread):
            def run(self):
                states = ["eStateInvalid", "eStateUnloaded", "eStateConnected", "eStateAttaching", "eStateLaunching", "eStateStopped", "eStateRunning", "eStateStepping", "eStateCrashed", "eStateDetached", "eStateExited", "eStateSuspended"]

                processBroadcaster = self.handler.process.GetBroadcaster()
                processBroadcaster.AddListener(listener, lldb.SBProcess.eBroadcastBitStateChanged | lldb.SBProcess.eBroadcastBitSTDOUT | lldb.SBProcess.eBroadcastBitSTDERR)

                targetBroadcaster = self.handler.target.GetBroadcaster()
                targetBroadcaster.AddListener(listener, lldb.SBTarget.eBroadcastBitModulesLoaded | lldb.SBTarget.eBroadcastBitModulesUnloaded)

                self.stopRequest = False
                while not self.stopRequest:
                    if listener.WaitForEvent(1, event):
                        eBroadcaster = event.GetBroadcaster()
                        eType = event.GetType()
                        # DBG_LOG("[EVENT] type %d (%s)\n" % (eType, str(event)))

                        if eBroadcaster == processBroadcaster:
                            if eType == lldb.SBProcess.eBroadcastBitStateChanged:
                                state = lldb.SBProcess.GetStateFromEvent(event)
                                resp = {"status":"event", "type":"state", "inferior_state":state, "state_desc": states[state]}
                                if state == 10:
                                    resp["exit_status"] = self.handler.process.GetExitStatus()
                                self.handler.sendJSON(resp)
                            elif eType == lldb.SBProcess.eBroadcastBitSTDOUT:
                                data=self.handler.process.GetSTDOUT(256)
                                self.handler.sendJSON({"status":"event", "type":"stdout", "output": "".join(["%02x" % ord(c) for c in data])})
                            elif eType == lldb.SBProcess.eBroadcastBitSTDERR:
                                data=self.handler.process.GetSTDERR(256)
                                self.handler.sendJSON({"status":"event", "type":"stderr", "output": "".join(["%02x" % ord(c) for c in data])})

                        elif eBroadcaster == targetBroadcaster:
                            if eType == lldb.SBTarget.eBroadcastBitModulesLoaded:
                                # data=self.handler.process.GetSTDERR(256)
                                self.handler.sendJSON({"status":"event", "type":"moduleLoaded"})
                            elif eType == lldb.SBTarget.eBroadcastBitModulesUnloaded:
                                # data=self.handler.process.GetSTDERR(256)
                                self.handler.sendJSON({"status":"event", "type":"moduleUnloaded"})
                return
        
        self.eventThread = EventThread()
        self.eventThread.handler = self

    def transportRead(self):
        try:
            length_str = sys.stdin.read(4)
            if len(length_str) < 4:
                return None
            length = struct.unpack('i', length_str)[0]

            line = ""
            while len(line) != length:
                rem = length - len(line)
                part = sys.stdin.read(rem)
                if part == None or len(part) == 0:
                    return None
                line += part

            if len(line) < length:
                return None

            # DBG_LOG("[READ] " + line + "\n")
            return line
        except BaseException as e:
            raise
            return None

    def transportWrite(self,s):
        # DBG_LOG("[WRITE] " + s + "\n")
        length = struct.pack('i', len(s))
        self.transport_lock.acquire()
        sys.stdout.write(length)
        sys.stdout.write(s)
        sys.stdout.flush()
        self.transport_lock.release()

    def buildError(self,msg):
        return {'status':'error', 'message':msg}

    def buildOK(self,msg=None):
        if msg == None:
            return {'status':'ok'}
        else:
            return {'status':'ok', 'message':msg}

    def sendJSON(self,j):
        s = json.dumps(j)
        self.transportWrite(s)

    def sendError(self,msg):
        self.sendJSON(self.buildError(msg))

    def sendOK(self,msg=None):
        self.sendJSON(self.buildOK(msg))

    def prepareExecutable(self,execPath,is64Bits,cwd,args):
        self.executable = execPath
        self.is64Bits = is64Bits
        self.workingDirectory = cwd
        self.arguments = shlex.split(args.encode("utf-8"))
        return self.buildOK()

    def createProcess(self):
        if self.process == None:
            err = lldb.SBError()
            self.target = self.debugger.CreateTarget(self.executable.encode("utf-8"), "x86_64" if self.is64Bits else "i386", None, True, err)
            if self.target == None or not self.target.IsValid():
                return self.buildError("cannot build target")
            launchInfo = lldb.SBLaunchInfo(self.arguments if self.arguments != None else [])
            launchInfo.SetWorkingDirectory(self.workingDirectory.encode("utf-8") if self.workingDirectory != None else "")
            launchInfo.SetLaunchFlags(lldb.eLaunchFlagDisableASLR + lldb.eLaunchFlagStopAtEntry)
            self.process = self.target.Launch(launchInfo, err)
            if self.process != None:
                self.eventThread.start()
                while self.process.GetState() == lldb.eStateAttaching:
                    time.sleep(0.1)
                return self.buildOK()
            else:
                self.target = None
                return self.buildError("cannot create process")
        return self.buildError("process already exists")

    def attachToProcess(self,pid,executable,is64Bits):
        if self.process == None:
            err = lldb.SBError()
            self.is64Bits = is64Bits
            self.executable = executable
            self.target = self.debugger.CreateTarget(self.executable.encode("utf-8"), "x86_64" if self.is64Bits else "i386", None, True, err)
            if self.target == None or not self.target.IsValid():
                return self.buildError("cannot build target")
            self.process = self.target.AttachToProcessWithID(self.debugger.GetListener(),pid,err)
            if self.process != None:
                self.eventThread.start()
                while self.process.GetState() == lldb.eStateAttaching:
                    time.sleep(0.1)
                result = self.buildOK()
                if self.target.GetNumModules() > 0:
                    executableFileSpec = self.target.GetExecutable()
                    module = self.target.FindModule(executableFileSpec)
                    if module != None and module.GetNumSections() > 1:
                        section = module.GetSectionAtIndex(1)
                        fileAddr = section.GetFileAddress()
                        loadAddr = section.GetLoadAddress(self.target)
                        aslrSlide = loadAddr - fileAddr
                        result['sectionName'] = section.GetName()
                        result['fileAddr'] = fileAddr
                        result['loadAddr'] = loadAddr
                        result['aslrSlide'] = aslrSlide
                return result
            else:
                self.target = None
                return self.buildError("cannot attach to process")
        return self.buildError("process already exists")

    def moduleCount(self):
        if self.process == None:
            return self.buildError("no process")
        result = self.buildOK()
        result['count'] = self.target.GetNumModules()
        return result

    def moduleDesc(self,module):
        desc = {}
        desc['uuid'] = module.GetUUIDString()
        fileSpec = module.GetFileSpec()
        if fileSpec != None:
            filename = fileSpec.GetFilename()
            desc['filename'] = filename
        sections = []
        gotBase = False
        for section in module.section_iter():
            loadAddr = section.GetLoadAddress(self.target)
            if loadAddr != lldb.LLDB_INVALID_ADDRESS:
                gotBase = True
            section_desc = {}
            section_desc['name'] = section.GetName()
            section_desc['fileAddr'] = section.GetFileAddress()
            section_desc['loadAddr'] = loadAddr
            section_desc['byteSize'] = section.GetByteSize()
            section_desc['fileByteSize'] = section.GetFileByteSize()
            sections.append(section_desc)
        desc['sections'] = sections
        return desc

    def moduleAtIndex(self,index):
        if self.process == None:
            return self.buildError("no process")
        if index < 0 or index >= self.moduleCount():
            return self.buildError("index out of range")
        module = self.target.GetModuleAtIndex(index)
        if module == None:
            return self.buildError("cannot get module")
        result = self.buildOK()
        result['module'] = self.moduleDesc(module)
        return result

    def moduleForFile(self,filename):
        if self.process == None:
            return self.buildError("no process")
        file_spec = lldb.SBFileSpec(filename.encode("utf-8"), True)
        module = self.target.FindModule(file_spec)
        if module == None:
            return self.buildError("can't find module")
        if not module.IsValid():
            return self.buildError("invalid module")
        result = self.buildOK()
        result['module'] = self.moduleDesc(module)
        return result

    def connectRemote(self,is64Bits,url,plugin):
        if self.process != None:
            return self.buildError("already have a process")
        err = lldb.SBError()
        self.is64Bits = is64Bits
        self.target = self.debugger.CreateTarget(None, "x86_64" if self.is64Bits else "i386", None, True, err)
        self.process = self.target.ConnectRemote(self.debugger.GetListener(), url.encode("utf-8"), plugin.encode("utf-8"), err)
        if self.process == None:
            return self.buildError("cannot connect to remote")
        else:
            self.eventThread.start()
            return self.buildOK()

    def moduleList(self):
        if self.process == None:
            return self.buildError("no process")
        cnt = self.target.GetNumModules()
        return [self.moduleDesc(self.target.GetModuleAtIndex(i)) for i in xrange(cnt)]

    def detach(self):
        if self.process == None:
            return self.buildError("no process")
        self.process.Detach()
        return self.buildOK()

    def deleteProcess(self):
        if self.process == None:
            return self.buildError("no process")
        if self.eventThread != None:
            self.eventThread.stopRequest = True
            self.eventThread.join()
            self.eventThread = None
        self.process.Destroy()
        self.process = None
        self.target = None
        return self.buildOK()

    def hasProcess(self):
        if self.process != None:
            return self.buildOK()
        else:
            return self.buildError("no process")

    def getProcessState(self):
        if self.process != None:
            states = ["eStateInvalid", "eStateUnloaded", "eStateConnected", "eStateAttaching", "eStateLaunching", "eStateStopped", "eStateRunning", "eStateStepping", "eStateCrashed", "eStateDetached", "eStateExited", "eStateSuspended"]
            state = self.process.GetState()
            result = self.buildOK()
            result["state"] = state
            result["state-string"] = states[state] if state >= 0 and state < len(states) else "invalid state (%d)" % state
        else:
            result = self.buildError("no process")
        return result

    def continueExecution(self):
        self.process.Continue()
        return self.buildOK()

    def stopReasonToString(self,reason):
        if reason == 0: return 'Invalid'
        if reason == 1: return 'None'
        if reason == 2: return 'Trace'
        if reason == 3: return 'Breakpoint'
        if reason == 4: return 'Watchpoint'
        if reason == 5: return 'Signal'
        if reason == 6: return 'Exception'
        if reason == 7: return 'Exec'
        if reason == 8: return 'Plan Complete'
        if reason == 9: return 'Thread Exiting'
        return 'Unknown Reason'

    def getThreadIDList(self):
        if self.process == None:
            return self.buildError("no process")
        lst = [{"thread-id":thread.GetThreadID(), "state":self.stopReasonToString(thread.GetStopReason())} for thread in self.process]
        result = self.buildOK()
        result["threads"] = lst
        return result

    def selectThreadID(self,tid):
        if self.process == None:
            return self.buildError("no process")
        thread = self.process.GetThreadByID(tid)
        if thread == None:
            return self.buildError("no thread %d" % tid)
        self.process.SetSelectedThread(thread)
        return self.buildOK()

    def breakExecution(self):
        process = self.process
        if process != None:
            process.SendAsyncInterrupt()
        return self.buildOK()

    def stopExecution(self):
        process = self.process
        if process == None:
            return self.buildError("no process")
        process.Kill()
        
        return self.buildOK()
    
    def getRegisters(self):
        process = self.process
        if process == None:
            return self.buildError("no process")
        thread = process.GetSelectedThread()
        frame = thread.GetSelectedFrame()
        lst = {}
        r_gprs = get_GPRs(frame)
        r_fprs = get_FPRs(frame)
        r_esrs = get_ESRs(frame)
        if r_gprs != None:
            for reg in r_gprs:
                lst[reg.GetName()] = reg.GetValue()
        if r_fprs != None:
            for reg in r_fprs:
                lst[reg.GetName()] = build_reg_value_string(reg)
        if r_esrs != None:
            for reg in r_esrs:
                lst[reg.GetName()] = reg.GetValue()
        result = self.buildOK()
        result["registers"] = lst
        return result

    def setBreakpointAtVirtualAddress(self,addr):
        target = self.target
        if target == None:
            return self.buildError("no target")
        breakpoint = target.BreakpointCreateByAddress(addr)
        if breakpoint == None:
            return self.buildError("cannot create breakpoint")
        result = self.buildOK()
        result['bkpt_id'] = breakpoint.GetID()
        bli = 0
        for bl in breakpoint:
            result['bl%d' % bli] = "load addr: %s" % hex(bl.GetLoadAddress())
            bli = bli + 1
        return result

    def removeBreakpoint(self,bkpt_id):
        target = self.target
        if target == None:
            return self.buildError("no target")
        target.BreakpointDelete(bkpt_id)
        return self.buildOK()

    def removeAllBreakpoints(self):
        target = self.target
        if target == None:
            return self.buildError("no target")
        if target.DeleteAllBreakpoints():
            return self.buildOK()
        else:
            return self.buildError("cannot remove all breakpoints")

    def stepInstruction(self):
        if self.process == None:
            return self.buildError("no process")
        thread = self.process.GetSelectedThread()
        thread.StepInstruction(False)

    def stepOver(self):
        if self.process == None:
            return self.buildError("no process")
        thread = self.process.GetSelectedThread()
        thread.StepInstruction(True)

    def stepOut(self):
        if self.process == None:
            return self.buildError("no process")
        thread = self.process.GetSelectedThread()
        thread.StepOut()

    def readMemory(self,addr,len):
        if self.process == None:
            return self.buildError("no process")
        err = lldb.SBError()
        mem = self.process.ReadMemory(addr,len,err)
        if not err.Success():
            return self.buildError("unable to read memory")
        result = self.buildOK()
        result["memory"] = struct.unpack('B' * len, mem)
        return result

    def writeByte(self,addr,value):
        if self.process == None:
            return self.buildError("no process")
        mem = struct.pack('B', value)
        err = lldb.SBError()
        self.process.WriteMemory(addr,mem,err)
        if not err.Success():
            return self.buildError("unable to write memory: " + err.GetCString() + ("(%d)" % self.process.GetState()))
        result = self.buildOK()
        return result

    def getFrameDesc(self,frame):
        module_name = None
        module_uuid = None
        module = frame.GetModule()
        if module != None:
            module_uuid = module.GetUUIDString()
            file = module.GetFileSpec()
            if file != None:
                module_name = file.GetFilename()
        return {"pc": frame.GetPC(), "function": frame.GetFunctionName(), "filename": module_name, "uuid": module_uuid}

    def getCallstack(self):
        if self.process == None:
            return self.buildError("no process")
        thread = self.process.GetSelectedThread()
        callstack = [self.getFrameDesc(frame) for frame in thread]
        result = self.buildOK()
        result["callstack"] = callstack
        return result

    def selectFrame(self,index):
        if self.process == None:
            return self.buildError("no process")
        thread = self.process.GetSelectedThread()
        thread.SetSelectedFrame(index)
        return self.buildOK()

    def setRegister(self,name,value):
        if self.process == None:
            return self.buildError("no process")
        thread = self.process.GetSelectedThread()
        frame = thread.GetSelectedFrame()
        regValue = findRegister(frame, name)
        if regValue == None:
            return self.buildError("register not found")
        err = lldb.SBError()
        if not regValue.SetValueFromCString(value.encode("utf-8"), err):
            return self.buildError("cannot set the register value: %s" % err.GetCString())
        return self.buildOK()

    def executeCommand(self,cmd):
        ci = self.debugger.GetCommandInterpreter()
        cmd_result = lldb.SBCommandReturnObject()
        ci.HandleCommand(cmd.encode("utf-8"), cmd_result)
        result = self.buildOK()
        result['output'] = cmd_result.GetOutput()
        result['error'] = cmd_result.GetError()
        result['succeeded'] = cmd_result.Succeeded()
        return result

    def sendToApplication(self,data):
        result = self.buildOK()
        try:
            str = reduce(lambda x,y: x+y, map(lambda x: chr(x), data))
            self.process.PutSTDIN(str)
        except Exception as e:
            result = self.buildError("cannot build string to send")
        return result

    def handleRequest(self,req):
        command = req['command'];
        result = None
        if command == 'ping':
            result = self.buildOK()
        elif command == 'prepareExecutable':
            result = self.prepareExecutable(req['path'], req['is64Bits'], req['cwd'], req['args'])
        elif command == 'createProcess':
            result = self.createProcess()
        elif command == 'attachToProcess':
            result = self.attachToProcess(req['pid'], req['executable'], req['is64Bits'])
        elif command == 'detach':
            result = self.detach()
        elif command == 'deleteProcess':
            result = self.deleteProcess()
        elif command == 'hasProcess':
            result = self.hasProcess()
        elif command == 'getProcessState':
            result = self.getProcessState()
        elif command == 'continueExecution':
            result = self.continueExecution()
        elif command == 'stopExecution':
            result = self.stopExecution()
        elif command == 'breakExecution':
            result = self.breakExecution()
        elif command == 'getThreadIDList':
            result = self.getThreadIDList()
        elif command == 'selectThreadID':
            result = self.selectThreadID(req['tid'])
        elif command == 'getRegisters':
            result = self.getRegisters()
        elif command == 'setBreakpointAtVirtualAddress':
            result = self.setBreakpointAtVirtualAddress(req['address'])
        elif command == 'removeBreakpoint':
            result = self.removeBreakpoint(req['bkpt_id'])
        elif command == 'removeAllBreakpoints':
            result = self.removeAllBreakpoints()
        elif command == 'stepInstruction':
            result = self.stepInstruction()
        elif command == 'stepOver':
            result = self.stepOver()
        elif command == 'stepOut':
            result = self.stepOut()
        elif command == 'readMemory':
            result = self.readMemory(req['address'], req['length'])
        elif command == 'writeByte':
            result = self.writeByte(req['address'], req['value'])
        elif command == 'getCallstack':
            result = self.getCallstack()
        elif command == 'selectFrame':
            result = self.selectFrame(req['index'])
        elif command == 'setRegister':
            result = self.setRegister(req['register'], req['value'])
        elif command == 'executeCommand':
            result = self.executeCommand(req['cli'])
        elif command == 'sendToApplication':
            result = self.sendToApplication(req['data'])
        elif command == 'moduleCount':
            return self.moduleCount()
        elif command == 'moduleAtIndex':
            return self.moduleAtIndex(req['index'])
        elif command == 'moduleForFile':
            return self.moduleForFile(req['file'])
        elif command == 'connectRemote':
            return self.connectRemote(req['is64Bits'], req['url'], req['plugin'])
        if result == None:
            result = self.buildError("unknown command '" + command + "'")
        return result

    def work(self):
        while True:
            try:
                # Get a command
                line = self.transportRead()
                if line == None:
                    break

                # Decode JSON
                try:
                    req = json.loads(line)
                except ValueError:
                    req = None

                if req == None:
                    self.sendError("cannot decode JSON")
                    continue

                result = None
                try:
                    result = self.handleRequest(req)
                except Exception as e:
                    result = self.buildError("bad request: " + str(e))

                if result == None:
                    result = self.buildError("empty response")

                if req.has_key("id"):
                    result["id"] = req["id"]
                self.sendJSON(result)

            except EOFError:
                self.sendOK("EOF")
                break
        self.stopRequest = True
        self.join()

if __name__ == "__main__":
    # DBG_LOG("\n\n-------------- STARTING --------------\n")
    handler = Handler()
    handler.work()
