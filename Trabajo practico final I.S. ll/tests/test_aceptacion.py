import unittest
import subprocess
import time
import os
import warnings

warnings.filterwarnings("ignore", category=ResourceWarning)

SERVER_CMD = ["python", "server/proxy_server.py", "--port", "5000"]
CLIENT = "python client/singleton_client.py --host 127.0.0.1 --port 5000"

def safe_decode(data):
    return data.decode("utf-8", errors="ignore") if isinstance(data, bytes) else str(data)

def log_step(msg):
    print(f"{msg}")

def log_result(title, success=True):
    status = "OK" if success else "ERROR"
    print(f"[RESULTADO FINAL] {title} ... {status}\n")


class TestTPFI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n Iniciando pruebas automatizadas del TPFI...")
        cls.server = subprocess.Popen(
            SERVER_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(6)
        print("Servidor iniciado correctamente.\n")

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.terminate()
            try:
                cls.server.wait(timeout=3)
            except Exception:
                cls.server.kill()

            if cls.server.stdout:
                cls.server.stdout.close()
            if cls.server.stderr:
                cls.server.stderr.close()
        print("\nServidor detenido.\n")

    def test_01_set_get_list(self):
        title = "test_01_set_get_list"
        print(f"\n{title} ... [EN PROCESO]")
        try:
            log_step("Ejecutando accion: SET")
            set_cmd = f"""{CLIENT} --action set --key test-id-1 --value "{{\\"name\\": \\"Empresa Test\\", \\"metadata\\": {{\\"cores\\": 2}}}}" """
            out = subprocess.check_output(set_cmd, shell=True)
            log_step(f"Respuesta: {safe_decode(out).strip()}")
            self.assertIn('"status": "ok"', safe_decode(out))

            log_step("Ejecutando accion: GET")
            get_cmd = f"{CLIENT} --action get --key test-id-1"
            out = subprocess.check_output(get_cmd, shell=True)
            log_step(f"Respuesta: {safe_decode(out).strip()}")
            self.assertIn('"status": "ok"', safe_decode(out))

            log_step("Ejecutando accion: LIST")
            list_cmd = f"{CLIENT} --action list"
            out = subprocess.check_output(list_cmd, shell=True)
            log_step(f"Respuesta: {safe_decode(out)[:300]}...")
            self.assertIn('"status": "ok"', safe_decode(out))

            log_result(title, True)

        except Exception as e:
            print(f"Error durante {title}: {e}")
            log_result(title, False)
            raise

    def test_02_argumentos_invalidos(self):
        title = "test_02_argumentos_invalidos"
        print(f"\n{title} ... [EN PROCESO]")
        bad_cmd = f"""{CLIENT} --action set --key test-id-2 --value "{{\\"name\\": \\"Test inválido\\"""
        try:
            log_step("Ejecutando cliente con JSON malformado...")
            out = subprocess.check_output(bad_cmd, shell=True, stderr=subprocess.STDOUT)
            out_decoded = safe_decode(out)
            log_step(f"Salida capturada: {out_decoded.strip()}")
            self.assertIn('"status": "error"', out_decoded)
            log_result(title, True)
        except subprocess.CalledProcessError as e:
            out = safe_decode(e.output)
            log_step(f"Salida con error esperada: {out.strip()}")
            self.assertTrue("error" in out.lower() or "invalid" in out.lower())
            log_result(title, True)
        except Exception as e:
            print(f"Error inesperado en {title}: {e}")
            log_result(title, False)
            raise

    def test_03_faltan_parametros(self):
        title = "test_03_faltan_parametros"
        print(f"\n{title} ... [EN PROCESO]")
        try:
            cmd = f"{CLIENT} --action set"
            log_step("Ejecutando cliente sin key ni value...")
            out = subprocess.check_output(cmd, shell=True)
            out_decoded = safe_decode(out)
            log_step(f"Salida: {out_decoded.strip()}")
            self.assertIn('"status": "error"', out_decoded)
            log_result(title, True)
        except Exception as e:
            print(f"Error durante {title}: {e}")
            log_result(title, False)
            raise

    def test_04_server_inaccesible(self):
        title = "test_04_server_inaccesible"
        print(f"\n{title} ... [EN PROCESO]")
        cmd = "python client/singleton_client.py --host 127.0.0.1 --port 5999 --action get --key test-id-1"
        try:
            log_step("Intentando conexion a servidor inexistente (puerto 5999)...")
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            self.fail("El cliente no fallo ante servidor inexistente.")
        except subprocess.CalledProcessError as e:
            msg = safe_decode(e.output).lower()
            log_step(f"Salida capturada: {msg.strip()}")
            self.assertTrue("connection" in msg or "refused" in msg or "error" in msg)
            log_result(title, True)
        except Exception as e:
            print(f"Error inesperado: {e}")
            log_result(title, False)
            raise

    def test_05_doble_server(self):
        title = "test_05_doble_server"
        print(f"\n{title} ... [EN PROCESO]")
        try:
            log_step("Intentando levantar segundo servidor en mismo puerto...")
            second = subprocess.Popen(SERVER_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1.5)
            stderr = safe_decode(second.stderr.read()).lower()
            second.terminate()
            second.wait(timeout=2)
            if second.stdout:
                second.stdout.close()
            if second.stderr:
                second.stderr.close()
            log_step(f"Salida del segundo servidor: {stderr.strip()}")
            self.assertTrue("address already in use" in stderr or "error" in stderr)
            log_result(title, True)
        except Exception as e:
            print(f"Error durante {title}: {e}")
            log_result(title, False)
            raise


if __name__ == "__main__":
    unittest.main(verbosity=0)